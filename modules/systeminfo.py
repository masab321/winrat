import wmi
import socket
import requests
import psutil

from uuid import getnode as get_mac
# mac address, public ip, private ip, open ports, users
def get_mac_hex():
    mac = "MAC: "
    mac += hex(get_mac())
    mac += "\n"
    return mac

def get_ips():
    ips = ""
    ip_addr = socket.gethostbyname(socket.gethostname())
    ips += f"Private IP: {ip_addr}\n"

    public_ip = requests.get("https://api.ipify.org").text
    ips += f"Public IP: {public_ip}\n"

    return ips

def get_local_ports():
    ports_result = "Ports Listening:\n"
    connections = set()
    for con in psutil.net_connections():
        if con.status == "LISTEN":
            connections.add((con.laddr.port, psutil.Process(con.pid).name()))

    for con in sorted(connections):
        ports_result += f"Port: {con[0]} > {con[1]}\n"

    return ports_result

def get_usernames():
    users = "USER LIST: "
    w = wmi.WMI()
    for usr in w.Win32_UserAccount(["Name"]):
        users += f"{usr.Name} "
    users += "\n"
    return users

def run(file_name, reload_interval=86400):
    result = get_mac_hex()
    result += get_ips()
    result += get_local_ports()
    result += get_usernames()
    return result 

if __name__ == "__main__":
    r = run(15)
    print(r)
