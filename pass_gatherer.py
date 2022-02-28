import subprocess


''' Quickly print out cleartext WiFi passwords stored on a Windows 10 machine '''
__author__ = "Orange-Joe"
__version__ =  "1.0"


# Windows command prints out information on WiFi profiles. Output is stripped of unneccessary characters and put into a list. 
output = subprocess.getoutput("""for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear""")
output = output.replace(' ', '')
output = output.split("\n")


# Print out useful information. 
for i in output:
    if i[0:8] == "SSIDname":
        print(i)
    if i[0:10] == "KeyContent":
        print(i)
        print("\n")
