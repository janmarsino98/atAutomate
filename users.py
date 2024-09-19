import constants as c
from dotenv import load_dotenv
import os

load_dotenv()
AVA_AT_SID = os.getenv("AVA_AT_SID")
JAN_AT_SID = os.getenv("JAN_AT_SID")


class User:
    def __init__(self, id:str, name:str, prompt:str, tarifas:str, at_sid:str):
        self.id = id
        self.name = name
        self.prompt = prompt
        self.tarifas = tarifas
        self.at_sid = at_sid
        
user_jan = User(
    id=1,
    name="Jan",
    prompt=c.JAN_PROMPT,
    tarifas=c.JAN_TARIFAS,
    at_sid = JAN_AT_SID
)

user_ava = User(
    id=2,
    name="Ava",
    prompt=c.AVA_PROMPT,
    tarifas=c.AVA_TARIFAS,
    at_sid=AVA_AT_SID,
)


users = [
    user_jan,
    user_ava
]