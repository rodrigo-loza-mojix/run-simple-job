import os
import re
import time

PATH_TO_BLACKLISTED_IPS_FILE = os.environ["PATH_TO_BLACKLISTED_IPS_FILE"]

def load_blacklist():
  blacklist = []
  file = open(PATH_TO_BLACKLISTED_IPS_FILE, "r")
  lines = [line for line in file.readlines()]
  file.close()
  return blacklist

def main():
  # Load blacklisted ips.
  blacklist = load_blacklist()
  # Scan the network. 
  os.system("nmap -sn -T5 --min-parallelism 100 192.168.254.0/24 | grep -v \"Down\" | tee /opt/output.file.txt ")
  # Load the ips.
  file = open("/opt/output.file.txt")
  lines = [line for line in file.readlines()]
  file.close()
  ips = []
  for line in lines:
      match = re.findall("(\d+\.\d+\.\d+\.\d+)", line)
      if len(match) > 0:
          if not match[0] in blacklist:
              ips.append(match[0])
  return ips

if __name__ == "__main__":
  main()
