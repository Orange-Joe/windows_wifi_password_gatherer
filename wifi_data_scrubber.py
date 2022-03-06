import subprocess
import argparse


''' 
Companion script to https://github.com/Orange-Joe/windows_wifi_password_gatherer.
Quickly remove WiFi SSIDs and passwords stored on a Windows 10 machine. 
This can also be done with 'netsh wlan delete profile name=* i=*'
This script has the added benefit of being able to exclude a profile from the deletion process. 
'''

# TODO: Add a feature to backup WiFi profiles as xml files using netsh wlan export function.
# TODO: Add a function to split --exclude argument by commas in order to support more than one excluded profile. 

__author__ = "Orange-Joe"
__version__ =  "1.0"


parser = argparse.ArgumentParser(description="Remove WiFi SSIDs and associated passwords from your system.")
parser.add_argument("-e", "--exclude", type=str, help="Choose a WiFi profile to exclude from removal process. Currently supports only 1 exclusion.")
args, unknown = parser.parse_known_args()


def main():

    # WiFi profiles will be stored in this list.
    profiles = []
    # Counter will add up the number of WiFi profiles removed from system.
    counter = 0
    # Gather list of all WiFi profiles, strip of unnecessary characters, and append to 'profiles' list.
    output = subprocess.getoutput("netsh wlan show profiles").split('\n')

    for i in output:
        if args.exclude:
            if 'All User Profile' in i:
                if args.exclude != i[27:]:
                    profiles.append(i[27:])
        else:
            if 'All User Profile' in i:
                profiles.append(i[27:])


    # Using the just-gathered profile names, remove them from the system. 
    for i in profiles:
        output = subprocess.getoutput(f"""netsh wlan delete profile "{i}" """)
        print(f"{output}\n")
        counter += 1

    # Display number of WiFi profiles found.
    if counter == 0:
        print(f"No WiFi profiles found.")

    elif counter >= 1:
        print(f"Removed {counter} WiFi profiles.")


if args.exclude:
    response = input(f"This process will remove all WiFi SSIDs and associated passwords from your system with the exception of '{args.exclude}'. Continue? Y\n")
else:
    response = input("This process will remove all WiFi SSIDs and associated passwords from your system. Continue? Y\n")

if response.lower() == 'y':
    print(f"Running {__file__}")
    main()
else:
    pass
    
