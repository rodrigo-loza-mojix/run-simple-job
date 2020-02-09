import subprocess

command = ["nmap", "-sn", "-T5", "--min-parallelism", "122" ,"192.168.254.0/24", "-oG", "output.file.txt;" "grep", "-v", "Down", "output.file.txt"]
status = subprocess.call(command)

