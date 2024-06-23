#!/usr/bin/env python

import requests

url = "<url>"


def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        pass

with open("output/path/file","r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = url + word 
        response = request(test_url)
        if response:
            print(f"[+]Discovered URL --> {test_url}")
