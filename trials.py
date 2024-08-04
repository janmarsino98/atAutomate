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

# URL de la solicitud
url = "https://www.airtasker.com/api/client/v1/experiences/post-task/post"

def post_task(title, description, price, at_sid):
    payload = {
    "title": title,
    "description": description,
    "date_type": "flexible",
    "price": price,
    "date": datetime.utcnow().isoformat() + 'Z',  # Generar la fecha actual en formato ISO 8601
    "location_type": {"type": "remote"},
    "image_urls": [],
    "origin": "header_post_task-v1",
    "key": str(uuid.uuid4()),  # Generar un UUID
    "attribution_data": {},
    "request_quote_form": []
}
    
    response = requests.post(url, json=payload, headers=c.HEADERS, proxies=proxy, cookies=c.COOKIES)
    return response
    
# df = pd.read_excel("users.xlsx", index_col=0)

# at_sids = list(df["at_sid"])


# for _ in range(5):
#     r = post_task(random.choice(c.RESUME_TITLES), random.choice(c.RESUME_DESCRIPTIONS), 40, random.choice(at_sids))
#     print(r.status_code)


def generate_random_users():
    r = requests.get("https://randomuser.me/api/?results=20&nat=AU&password=special,8-12,number,lower")
    data = r.json()["results"]
    users = []
    for user in data:
        first_name = user["name"]["first"]
        last_name = user["name"]["last"]
        location = user["location"]["city"]
        img = user["picture"]["large"]
        users.append([first_name, last_name, location, img])
        df = pd.DataFrame(users, columns=["First name", "Last Name", "City","img"])
        df.to_excel("sample_profiles.xlsx")
generate_random_users()
    