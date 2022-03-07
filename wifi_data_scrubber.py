import subprocess
import argparse


''' 
Companion script to https://github.com/Orange-Joe/windows_wifi_password_gatherer.
Quickly remove WiFi SSIDs and passwords stored on a Windows 10 machine. 
Can back up profiles in user-defined directory and exclude profiles from deletion process.  
'''

__author__ = "Orange-Joe"
__version__ =  "1.0"


parser = argparse.ArgumentParser(description="Remove WiFi SSIDs and associated passwords from your system.")
parser.add_argument("-e", "--exclude", type=str, 
                    help="""Choose WiFi profile(s) to exclude from removal process. Separate by comma(s) with no space between. \
If there is a space in the profile name add "quotes". """)
parser.add_argument("-b", "--backup", type=str, 
                    help="Create a directory to store XML backups in. Choose '.' to save in current directory.")
args, unknown = parser.parse_known_args()

print(f"Running {__file__}")

def main():

    # WiFi profiles will be stored in this list.
    profiles = []
    # Counter will add up the number of WiFi profiles removed from system.
    counter = 0
    # Gather list of all WiFi profiles, strip of unnecessary characters, and append to 'profiles' list.
    output = subprocess.getoutput("netsh wlan show profiles").split('\n')

    for i in output:
        if 'All User Profile' in i:
            profiles.append(i[27:])


    # Using the just-gathered profile names, remove them from the system. 
    for i in profiles:
        if args.exclude:
            if i.lower() not in args.exclude:
                output = subprocess.getoutput(f"""netsh wlan delete profile "{i}" """)
                print(f"[+] {output}")
                counter += 1
        else:
            output = subprocess.getoutput(f"""netsh wlan delete profile "{i}" """)
            print(f"[+] {output}")
            counter += 1


    # Display number of WiFi profiles found.
    if counter == 0:
        print(f"No WiFi profiles found.")

    elif counter >= 1:
        print(f"\nRemoved {counter} WiFi profiles.\n")


# Checkpoint
if args.exclude:
    response = input(f"This process will remove all WiFi SSIDs and associated passwords from your system with the exception of {args.exclude}. Continue? Y|n")
else:
    response = input("This process will remove all WiFi SSIDs and associated passwords from your system. Continue? Y|n")

# If user wants to continue, continue.
if response.lower() == 'y':

    # Split args.exclude into a list if a comma is found.
    if type(args.exclude) is str and ',' in args.exclude: 
        args.exclude = args.exclude.lower().split(',')

    # Backup profiles in XML format to user-defined directory.
    if args.backup:
        current_dir = subprocess.getoutput("chdir")

        # If user defined '.' as directory, save all XML files in current directory.
        if args.backup == '.':
            backed_up_file = subprocess.getoutput(f"netsh wlan export profile folder={current_dir} key=clear")
            print(f"files backed up in {current_dir}")

        else:
            subprocess.getoutput(f"mkdir {args.backup}")
            backed_up_file = subprocess.getoutput(f"netsh wlan export profile folder={current_dir}\{args.backup} key=clear")
            print(f"\nFiles backed up in {current_dir}\{args.backup}\n")
    
    # Start main function.
    main()

else:
    pass
    
