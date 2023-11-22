from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load the .env file

load_dotenv()
password = os.getenv("MONGO_SECRET")

uri = f"mongodb+srv://josvapstg:{password}@chatbot.gzetn86.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

dictionary_collection = client["MY_DB"]["diccionario"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)