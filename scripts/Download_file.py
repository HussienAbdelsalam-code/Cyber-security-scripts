#!/usr/bin/env python3

import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name , "wb") as out_file:
        out_file.write(get_response.content)

download("https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Nissan_Skyline_GT-R_R34_V_Spec_II.jpg/800px-Nissan_Skyline_GT-R_R34_V_Spec_II.jpg")
