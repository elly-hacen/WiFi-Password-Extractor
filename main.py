import subprocess
import re

print('''  
      $ > Which operation do you wanna perform : 
      
      type < 0 > Specific Profile
      type < 1 > All Profiles
      ''')
choice = input('Enter your choice : ')
print(sep='\n')
match choice:

    case '0':
        cmd = ('netsh', 'wlan', 'show', 'profiles')
        cmd_output = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True).communicate()[0]
        print(cmd_output)
        usr_profile = input('Enter the user profile name : ')
        cmd2 = ('netsh', 'wlan', 'show', 'profile', f'name={usr_profile}', 'key=clear')
        cmd2_output = subprocess.Popen(cmd2, stdout=subprocess.PIPE, text=True).communicate()[0]
        print('\n')
        output_list = cmd2_output.split('\n')

        # for i, x in enumerate(output_list): print(i, x) if you want to check the index of the entire output then
        # remove the hashtag in front of for loop and what you want to print, print it according to index number
        # 'i.e' print(output_list[index_number_goes_here])

        print(output_list[20])  # It will print profile name of the interface
        print(output_list[32])  # It will print password of that interface

    case '1':
        command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
        profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
        wifi_list = list()
        if len(profile_names) != 0:
            for name in profile_names:
                wifi_profile = dict()
                profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name],
                                              capture_output=True).stdout.decode()
                if re.search("Security key           : Absent", profile_info):
                    continue
                else:
                    wifi_profile["ssid"] = name
                    profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                                       capture_output=True).stdout.decode()
                    password = re.search("Key Content            : (.*)\r", profile_info_pass)
                    if password is None:
                        wifi_profile["password"] = None
                    else:
                        wifi_profile["password"] = password[1]
                    wifi_list.append(wifi_profile)
        for x in range(len(wifi_list)):
            print(wifi_list[x])
