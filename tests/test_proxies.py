import requests

import os

from dotenv import load_dotenv


load_dotenv()
PROXY_CRED = os.getenv("HTTP_PROXY")
proxy = {
    "http": f"http://{PROXY_CRED}",
    "https": f"http://{PROXY_CRED}",
}

def make_request():
    r = requests.get("https://api64.ipify.org/?format=json", proxies=proxy)
    print(r.content)
    
import time
while True:
    make_request()
    time.sleep(5)