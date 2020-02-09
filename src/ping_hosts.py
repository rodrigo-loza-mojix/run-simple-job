import subprocess

def main():
  command = ["nmap", "-sn", "-T5", "--min-parallelism", "122" ,"192.168.254.0/24", "-oG", "output.file.txt;" "grep", "-v", "Down", "output.file.txt"]
  status = subprocess.call(command)

if __name__ == "__main__":
  main()