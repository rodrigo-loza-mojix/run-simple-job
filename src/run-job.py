# !/usr/bin/python
# path_to_client_inventory: A string that contains a path to a client folder whose subfolders are environments.
import os
import sys
import time
import datetime
import requests
import yaml
import base64
from requests.compat import urljoin

schema = os.environ["SCHEMA"] if "SCHEMA" in os.environ else "https://"
delay = int(os.environ["DELAY"]) if "DELAY" in os.environ else int(120)
target_path_hubs = os.environ["TARGET_PATH_HUBS"] if "TARGET_PATH_HUBS" in os.environ else "/opt/options/hubs/"
target_path_premises = os.environ["TARGET_PATH_PREMISES"] if "TARGET_PATH_PREMISES" in os.environ else "/opt/options/premises/"
os.system(f"mkdir -p {target_path_hubs}")
os.system(f"mkdir -p {target_path_premises}")

path_to_inventory = os.environ["CLIENT_INVENTORY_PATH"] # /opt/axians-hub-deployment-tool/inventories/RED/
path_to_environments = [os.path.join(path_to_inventory, folder) for folder in os.listdir(path_to_inventory)] # /opt/axians-hub-deployment-tool/inventories/RED/VIZIX_DEV/
host_file = "group_vars/hosts.yml"
hub_file = "group_vars/hubs.yml"

hubs_uri = "/statemachine-api-configuration/rest/configuration/hub"
premises_uri = "/statemachine-api-configuration/rest/configuration/locations/"

def exec_request(url=None, headers=None, data=None, params=None, method=None):
    try:
        if method == "GET":
            response = requests.get(url=url, headers=headers, data=data, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url=url, headers=headers, data=data, params=params, timeout=30)
        elif method == "PUT":
            response = requests.put(url=url, headers=headers, data=data, params=params, timeout=30)
        else:
            pass
        if response.status_code >= 200 and response.status_code <= 399:
            return response.json()
        else:
            print(f"[ERROR] rc: {response.status_code} text: {response.text}")
            return {}
    except Exception as exception:
        print("Request could not be completed. ", exception)
        return {}

def get_now():
    now = datetime.datetime.now()
    now = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    return "-".join([str(each) for each in now])

def create_file(pathfile=None):
    file = open(pathfile, "w")
    file.close()

def create_folder(pathfolder=None):
    if os.path.isdir(pathfolder):
        pass
    else:
        os.mkdir(pathfolder)

def main():
    while True:
        for path_to_environment in path_to_environments:
            print("Environment: ", path_to_environment)
            _, environment = os.path.split(path_to_environment)
            create_folder(pathfolder=os.path.join(target_path_hubs, environment))
            create_folder(pathfolder=os.path.join(target_path_premises, environment))
            # Load files.
            hosts_path = os.path.join(path_to_environment, host_file)
            hubs_path = os.path.join(path_to_environment, hub_file)
            hosts_file = open(hosts_path, "r")
            hubs_file = open(hubs_path, "r")
            hosts_yaml = yaml.safe_load(hosts_file.read())
            hubs_yaml = yaml.safe_load(hubs_file.read())
            hosts_file.close()
            hubs_file.close()
            # Load variables for request.
            env_dns = hosts_yaml["env_dns_resolution"]
            user = hubs_yaml["digital_plateform_user"]
            password = hubs_yaml["digital_plateform_pass"]
            print(env_dns, user, password)
            ## CREATE HUB FILES ##
            # Remove all files.
            print("Hubs before cleaning: ", len(os.listdir(os.path.join(target_path_hubs, environment))))
            all_files = [os.path.join(target_path_hubs, environment, file) for file in os.listdir(os.path.join(target_path_hubs, environment))]
            [os.remove(file) for file in all_files if os.path.isfile(file)]
            print("Hubs after cleaning: ", len(os.listdir(os.path.join(target_path_hubs, environment))))
            # Prepare request.
            line = str(user)+":"+str(password)
            basic_auth = base64.b64encode(line.encode())
            host = schema + env_dns
            url = urljoin(host, hubs_uri)
            headers = {"Content-Type": "application/json", "Authorization": "Basic "+basic_auth.decode("utf-8"), "ORIGIN": "axians-jenkins"}
            data={}
            params={}
            # Send request.
            response = exec_request(method="GET", url=url, headers=headers, data=data, params=params)
            hub_ids = [obj["id"].replace(" ", "_") for obj in response]
            print(hub_ids)
            for hub_id in hub_ids:
                pathfile=os.path.join(target_path_hubs, environment, hub_id)
                create_file(pathfile=pathfile)
                assert os.path.isfile(pathfile) == True, f"File {pathfile} does not exist."
            print("Hubs after creating: ", len(os.listdir(os.path.join(target_path_hubs, environment))))
            ## CREATE PREMISE FILES ##
            print("premises before cleaning: ", len(os.listdir(os.path.join(target_path_premises, environment))))
            all_files = [os.path.join(target_path_premises, environment, file) for file in os.listdir(os.path.join(target_path_premises, environment))]
            [os.remove(file) for file in all_files if os.path.isfile(file)]
            print("premises after cleaning: ", len(os.listdir(os.path.join(target_path_premises, environment))))
            # Prepare request.
            line = str(user)+":"+str(password)
            basic_auth = base64.b64encode(line.encode())
            host = schema + env_dns 
            url = urljoin(host, premises_uri)
            headers = {"Content-Type": "application/json", "Authorization": "Basic "+basic_auth.decode("utf-8"), "ORIGIN": "axians-jenkins"}
            data={}
            params={"level": "premise", "size": "500"}
            # Send request.
            response = exec_request(method="GET", url=url, headers=headers, data=data, params=params)
            codes = [obj["code"] for obj in response]
            names = [obj["name"].replace(" ", "_") for obj in response]
            print(codes)
            for name, code in zip(names, codes):
                premise = "___".join([name, code])
                pathfile = os.path.join(target_path_premises, environment, premise)
                create_file(pathfile=pathfile)
                assert os.path.isfile(pathfile) == True, f"File {pathfile} does not exist."
            print("premises after creating: ", len(os.listdir(os.path.join(target_path_premises, environment))))
            print("Files created {}.\n\n".format(get_now()))
        time.sleep(delay)

if __name__ == "__main__":
    main()

