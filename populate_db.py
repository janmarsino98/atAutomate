from pymongo import MongoClient
from dotenv import load_dotenv
import os
from users import users

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Create a MongoClient instance using the MongoDB URI
client = MongoClient(MONGO_URI)

# Access the database (automatically selected if the database is in the URI)
db = client.get_default_database()

# Access the collection (replace 'users' with your collection name)
users_collection = db['users']
tasks_collection = db['tasks']
sent_messages_collection = db['sentMessages']

# for user in users:
#     user_dict = {
#         "name": user.name,
#         "prompt": user.prompt,
#         "tarifas": user.tarifas,
#         "at_sid": user.at_sid,
#         "message": user.message
#     }
#     result = users_collection.insert_one(user_dict)
#     print(f"Inserted {user.name} with ID: {result.inserted_id}")
    
    
import pandas as pd

df = pd.read_excel("notifications.xlsx", index_col=0)

for index, row in df.iterrows():
    sent_messages_dict = {
        "slug": row["notifications"]
    }
        
    result = sent_messages_collection.insert_one(sent_messages_dict)
