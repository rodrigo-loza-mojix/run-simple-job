import subprocess

def main():
  os.system("nmap -sn -T5 --min-parallelism 100 192.168.254.0/24 | grep -v \"Down\" | tee /opt/output.file.txt ")

if __name__ == "__main__":
  main()
