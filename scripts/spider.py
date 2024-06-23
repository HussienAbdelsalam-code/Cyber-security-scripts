#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse

url = "http://192.168.1.13/mutillidae"
target_links = []

def extract_links_from(url):
    try:
        response = requests.get(url)
        return re.findall('(?:href=")(.*?)"',response.content.decode())
    except Exception:
        print (url)
        return []

    
def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url,link)
        if "#" in link:
            link = link.split('#')[0]
        if url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(url)
