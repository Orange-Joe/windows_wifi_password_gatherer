import subprocess


''' Import all WiFi XML files in the given directory. Useful when experimenting with modification of saved profiles. '''

__author__ = "Orange-Joe"
__version__ =  "1.0"

# Get a list of files in current directory.
output = subprocess.getoutput('dir /b').split('\n')
# List that will contain any found xml files.
xml_files = []

for i in output:   
    if i[-4:] == '.xml':
        xml_files.append(i)

for i in xml_files:  
    subprocess.getoutput(f"""netsh wlan add profile "{i}" """)
    print(f"Imported {i}")
