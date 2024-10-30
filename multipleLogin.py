# $language = "python"
# $interface = "1.0"

import os
import configparser

def switch_tab(tab_name):
    for tab in crt.GetScriptTab().Session.ConnectedSessionsIterator():
        if tab.Caption == tab_name:
            tab.Activate()
            return True
    return False

def main():
    # Read the property file
    config = configparser.ConfigParser()
    config.read('servers.ini')

    # Prompt user to launch the script
    if not crt.Dialog.Prompt("Launch servers and capture output?", "Script Confirmation", "Yes", "No") == "Yes":
        return

    # Set up the log file
    log_dir = os.path.expanduser("~/SecureCRT_Logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "server_output.log")

    # Enable synchronous mode
    crt.Screen.Synchronous = True

    with open(log_file, 'w') as f:
        for section in config.sections():
            username = config[section]['username']
            password = config[section]['password']
            tab_name = config[section]['tab_name']
            commands = config[section]['commands'].split(',')

            f.write(f"\n--- Output for {tab_name} ---\n\n")

            # Connect to the server (assuming the session is already configured)
            crt.Session.Connect(f"/S {tab_name}")

            # Switch to the tab
            if not switch_tab(tab_name):
                f.write(f"Failed to switch to tab {tab_name}\n")
                continue

            # Wait for login prompt and enter credentials
            crt.Screen.WaitForString("login:")https://github.com/somu439/securecrt/tree/main
            crt.Screen.Send(username + "\n")
            crt.Screen.WaitForString("Password:")
            crt.Screen.Send(password + "\n")

            # Wait for prompt
            crt.Screen.WaitForString("$")

            # Run commands and capture output
            for command in commands:
                crt.Screen.Send(command.strip() + "\n")
                crt.Screen.WaitForString("$")
                output = crt.Screen.ReadString("$")
                f.write(f"Command: {command}\n{output}\n\n")

            # Logout
            crt.Screen.Send("exit\n")

    # Disable synchronous mode
    crt.Screen.Synchronous = False

    crt.Dialog.MessageBox(f"Log saved to {log_file}")

main()
