# $language = "python"
# $interface = "1.0"

import os

def main():
    # Define the commands to run
    commands = [
        "show version",
        "show interfaces",
        "show ip route",
        "show running-config"
    ]

    # Set up the log file
    log_dir = os.path.expanduser("~/SecureCRT_Logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "command_output.log")

    # Ensure we're connected
    if not crt.Session.Connected:
        crt.Dialog.MessageBox("Not connected. Please connect to a device first.")
        return

    # Enable synchronous mode
    crt.Screen.Synchronous = True

    # Open the log file
    with open(log_file, 'w') as f:
        # Run each command and capture output
        for command in commands:
            f.write(f"\n--- Output of '{command}' ---\n\n")
            
            # Send the command
            crt.Screen.Send(command + "\n")
            
            # Wait for the command to complete
            crt.Screen.WaitForString(crt.Screen.Prompt)
            
            # Capture the output
            output = crt.Screen.ReadString(crt.Screen.Prompt)
            
            # Write the output to the log file
            f.write(output)

    # Disable synchronous mode
    crt.Screen.Synchronous = False

    crt.Dialog.MessageBox(f"Log saved to {log_file}")

main()
