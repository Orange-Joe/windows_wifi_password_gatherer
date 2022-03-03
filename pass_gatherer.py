import argparse
import subprocess


''' Quickly print out cleartext WiFi passwords stored on a Windows 10 machine '''
__author__ = "Orange-Joe"
__version__ =  "1.0"


parser = argparse.ArgumentParser(description="Gather cleartext WiFi passwords. Finds passwords for all profiles by default.")
parser.add_argument("-p", "--profile", type=str, help="Choose a WiFi profile.")
parser.add_argument("-f", "--filename", type=str, help="Choose a file name to save results to.")
args, unknown = parser.parse_known_args()

# Stores information from parsed command output.
loot = []

# Function to use if searching for a single WiFi profile using --profile. 
if args.profile:    
    profile_info_to_parse = subprocess.getoutput(f"""netsh wlan show profile name="{args.profile}" key=clear""").split("\n")  
    
    for info in profile_info_to_parse:
        if 'SSID name' in info:
            loot.append(f"SSID name: {info[29:]}")
    
        if 'Key Content' in info:
            loot.append(f"Password: {info[29:]}")
    
    if len(loot) == 0:
        print(f"""[+] No access point with the name "{args.profile}" was found.""")


# Default function. Searches for all WiFi profiles on system.
else: 
    profiles = []
    profile_info_to_parse = []
    # Gather list of all WiFi profiles, strip of unnecessary characters, and append to 'profiles' list.
    output = subprocess.getoutput("netsh wlan show profiles").split('\n')
    
    for i in output:
        if 'All User Profile' in i:
            profiles.append(i[27:])

    # Using the just-gathered profile names, query the system for all information regarding WiFi profiles. 
    for i in profiles:
        query = subprocess.getoutput(f"""netsh wlan show profile name="{i}" key=clear""").split('\n')
        profile_info_to_parse.append(query)

    # Parse through the data and save it in a more human-readable format.
    for profiles in profile_info_to_parse:   
        for info in profiles:
            if 'SSID name' in info:
                loot.append(f"SSID name: {info[29:]}")
    
            if 'Key Content' in info:
                loot.append(f"Password: {info[29:]}")
    

# File name is defined by --filename. Print output to file and terminal. 
if args.filename:
    file = open(f'{args.filename}', 'w')
    
for i in range(len(loot)):
    if loot[i][0:10] == "SSID name:" and loot[i+1][0:10] == "Password: ":
        print(f"{loot[i]}\n{loot[i+1]}\n")
        if args.filename:
            file.write(f"{loot[i]}\n{loot[i+1]}\n\n")
        
    elif loot[i][0:10] == "SSID name:" and loot[i+1][0:10] == "SSID name:":
        print(f"{loot[i]}\nNo Password\n")
        if args.filename:
            file.write(f"{loot[i]}\nNo password saved.\n\n")

if args.filename:
    print(f"[+] File saved in {subprocess.getoutput('chdir')}\{args.filename}")
    file.close()

