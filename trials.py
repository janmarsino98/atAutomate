import requests
import os
from dotenv import load_dotenv
import constants as c
import pandas as pd
import random
import uuid
from datetime import datetime

load_dotenv()
proxy_cred = os.getenv("HTTP_PROXY")
proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}


r = requests.get("https://api.myip.com", proxies=proxy)
print(r.json())