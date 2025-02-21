import os
import ssl
import certifi
import yfinance as yf
import requests

# Force SSL to use Certifi's CA bundle
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

session = requests.Session()
session.verify = certifi.where()

ca_path = certifi.where()
print("Certifi CA Path:", ca_path)
print("File Exists:", os.path.exists(ca_path))

print("SSL CA Path:", ssl.get_default_verify_paths())  # Check default CA paths
print("Certifi Path:", certifi.where())  # Check where certifi is looking

print("ssl.OPENSSL_VERSION = ", ssl.OPENSSL_VERSION)
print("sesssion = ", session)  # This should print the path to the CA certificate bundle

print("Effective CA Bundle:", requests.get('https://www.howsmyssl.com/a/check').json()["tls_version"])

# Example: Fetching data with the secure session
ticker = "META"
data = yf.download(ticker, session=session)
print(data)
