import constants as c
import requests
import pandas as pd

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