# Local IP address
import socket
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"IP Address: {ip_address}")


# Public IP address
import requests
public_ip = requests.get('https://api.ipify.org').text
print(f"Public IP Address: {public_ip}")

