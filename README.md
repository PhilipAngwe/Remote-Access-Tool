# Remote-Access-Tool
This Python script enables remote control of a host machine via TCP connection. Features include executing commands, file upload/download, screenshot capture, system info retrieval, process management, and more.
To use the script and listen to port 4444 using netcat, follow these steps:

1. **Run the Script:**
   - Execute the `remote_shell.py` script on the target machine you want to control:
     ```
     python remote_shell.py
     ```

2. **Connect via Netcat:**
   - Open a terminal or command prompt on the machine from which you want to control the target.
   - Use netcat to connect to the target machine's IP address and port 4444:
     ```
     nc <target_ip> 4444
     ```
     Replace `<target_ip>` with the IP address of the target machine.

3. **Send Commands:**
   - Once connected, you can send commands to the target machine via netcat. For example:
     - `ls`: List files in the current directory.
     - `upload file.txt`: Upload a file to the target machine.
     - `screenshot`: Capture a screenshot of the target machine.
     - `whoami`: Execute a system command to display the current user.

4. **Exit:**
   - To close the connection, send the command `exit`.

Ensure that both machines are on the same network and that the target machine is reachable from the machine running netcat. Also, make sure to replace `<target_ip>` with the actual IP address of the target machine.
