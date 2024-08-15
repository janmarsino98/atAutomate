import requests
from dotenv import load_dotenv
import os
import constants as c

load_dotenv()
proxy_cred = os.getenv("HTTP_PROXY")

proxy = {
    "http": f"http://{proxy_cred}",
    "https": f"http://{proxy_cred}",
}


r = requests.get("https://id.airtasker.com/u/email-verification?ticket=P6fEkptlj9dntYWtezhQZsYkJBM672St#", headers=c.HEADERS, proxies=proxy)
print(r.status_code)