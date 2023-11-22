from fastapi import FastAPI, Form
import requests
from utils import send_message
from dotenv import load_dotenv
import os
from typing import List
from models import dictionary_collection
import urllib.parse
from utils import obtain_definitions_mongo

load_dotenv()

app = FastAPI()
whatsapp_number = os.getenv("TO_NUMBER")
api_key = os.getenv("DICTIONARY_API_KEY")

@app.post("/message")
async def reply(Body: str = Form()):
    escaped_body = urllib.parse.quote(Body)
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{escaped_body}?key={api_key}"
    flag = "Please give a valid word"

    if Body.isalpha():
        response = requests.get(url)
        print("Response:", response)
        data = response.json()

        definition = data[0]["shortdef"][0]

        send_message(whatsapp_number, definition)
        
        dictionary_db = {"word": Body, "definition": definition}
        dictionary_collection.insert_one(dictionary_db)
        flag = "Definition sent successfully"
    else:
        return send_message(whatsapp_number, flag)

    return ""

@app.get("/definitions")
async def get_definitions():
    definitions = obtain_definitions_mongo()
    return list(definitions)
