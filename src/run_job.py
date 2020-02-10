# !/usr/bin/python
# Author: rodrigo.loza@mojix.com
# Description: Populate options for jenkins.
import os
import sys
import re
import time
import datetime
import requests
import yaml
import base64
import ping_hosts
from requests.compat import urljoin

# Others.
client_environment = os.environ["CLIENT_ENVIRONMENT"]

# Build path to required files where they will be created.
# ../options/hubs_ids_ips/
target_path_hubs_ids_ips = os.environ["TARGET_PATH_HUB_IDS_IPS"] if "TARGET_PATH_HUBS" in os.environ else "/opt/options/hubs_ids_ips/"
target_path_hubs_ids_ips = os.path.join(target_path_hubs_ids_ips, client_environment)
os.system(f"mkdir -p {target_path_hubs_ids_ips}")

# Path to MODES.
path_to_custom_inventory = os.environ["PATH_TO_CUSTOM_INVENTORY"] 
path_to_file_hubs_ids_ips = os.environ["PATH_TO_FILE_HUBS_IDS_IPS"]

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

def create_inventory(ips=None):
    path_to_hosts_ini = os.path.join(path_to_custom_inventory, "hosts.ini")
    # Remove file.
    file = open(path_to_hosts_ini, "w")
    file.write("")
    file.close()
    # Create file.
    head = "[hosts]\n"
    custom_hubs = [f"hub0{index} ansible_ssh_user=ansible_user ansible_ssh_host={ip} ansible_ssh_private_key_file=ssh/hubs/ansible_id_rsa\n" for index, ip in enumerate(ips)]
    file = open(path_to_hosts_ini, "w")
    file.write(head)
    for custom_hub in custom_hubs:
        file.write(custom_hub)
    file.close()
    # Remove path_to_file_hubs_ids_ips.
    file = open(path_to_file_hubs_ids_ips, "w")
    file.write("")
    file.close()

def create_files():
    # Remove files.
    path_to_all_files = os.path.join(target_path_hubs_ids_ips)
    files = [os.path.join(target_path_hubs_ids_ips, file) for file in os.listdir(path_to_all_files)]
    [os.remove(file) for file in files if os.path.isfile(file)]
    # Create files.
    ########################
    ## CREATE HUB_IDS_IPS ##
    ########################
    file = open(path_to_file_hubs_ids_ips, "r") #HUB-ID___IP
    lines = [line[:-1] for line in file.readlines()]
    file.close()
    for line in lines:
        pathfile = os.path.join(target_path_hubs_ids_ips, line)
        create_file(pathfile=pathfile)
        assert os.path.isfile(pathfile) == True, f"File {pathfile} does not exist."

if __name__ == "__main__":
    CREATE_INVENTORY = "CREATE_INVENTORY"
    CREATE_FILES = "CREATE_FILES"
    mode = os.environ["MODE"]
    if mode == CREATE_INVENTORY:
        ips = ping_hosts.main()
        create_inventory(ips=ips)
    elif mode == CREATE_FILES:
        create_files()
    else:
        pass

