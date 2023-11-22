from fastapi import FastAPI, Form
import requests
from utils import send_message
from dotenv import load_dotenv
import os
from typing import List
from models import dictionary_collection
import urllib.parse
from utils import obtain_definitions_mongo
import re

load_dotenv()

app = FastAPI()
whatsapp_number = os.getenv("TO_NUMBER")
api_key = os.getenv("DICTIONARY_API_KEY")
riot_api_key = os.getenv("RIOT_API")

@app.post("/messageDictionary")
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

@app.post("/messageLeague")
async def reply(Body: str = Form()):
    escaped_body = urllib.parse.quote(Body)
    # Separar el escaped body (Viene en formato Nombre#Tag) y obtener el nombre y el tag
    name_tag = re.split('%23', escaped_body)
    print(name_tag)
    name = name_tag[0]
    tag = name_tag[1]
    # Obtener PUUID con el nuevo formato de nombre Nombre+#Tag
    url = f"https://la1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={riot_api_key}"
    response = requests.get(url)
    data = response.json()
    riot_id = data["id"]
    url = f"https://la1.api.riotgames.com/lol/league/v4/entries/by-summoner/{riot_id}?api_key={riot_api_key}"
    response = requests.get(url)
    data = response.json()
    tier = data[1]["tier"]
    rank = data[1]["rank"]
    lp = data[1]["leaguePoints"]
    wins = data[1]["wins"]
    losses = data[1]["losses"]
    winrate = round((wins/(wins+losses))*100, 2)
    send_message(whatsapp_number, f"{tier} {rank} {lp} LP\n{wins}W {losses}L\n{winrate}% winrate")


# Seleccion entre diccionario y league con un mensaje y luego se hace la busqueda
@app.post("/message")
async def reply(Body: str = Form()):
    if Body.startswith("Diccionario"):
        word = Body[12:]
        await reply_dictionary(word)
    elif Body.startswith("League"):
        summoner_name = Body[7:]
        await reply_league(summoner_name)
    else:
        send_message(whatsapp_number, "No se reconoce el comando. Escribe Diccionario seguido de una palabra en ingles o League seguido de tu nombre de invocador")
    return ""

async def reply_dictionary(Body: str):
    send_message(whatsapp_number, "Buscando definicion...")

    if Body.isalpha():
        escaped_body = urllib.parse.quote(Body)
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{escaped_body}?key={api_key}"
        response = requests.get(url)
        print("Response:", response)
        data = response.json()

        definition = data[0]["shortdef"][0]

        send_message(whatsapp_number, definition)
        
        dictionary_db = {"word": Body, "definition": definition}
        dictionary_collection.insert_one(dictionary_db)
    else:
        flag = "Please give a valid word"

    send_message(whatsapp_number, flag)
    return ""

async def reply_league(Body: str):
    send_message(whatsapp_number, "Buscando invocador...")
    escaped_body = urllib.parse.quote(Body)
    name_tag = re.split('%23', escaped_body)
    print(name_tag)
    name = name_tag[0]
    tag = name_tag[1]
    url = f"https://la1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={riot_api_key}"
    response = requests.get(url)
    data = response.json()
    riot_id = data["id"]
    url = f"https://la1.api.riotgames.com/lol/league/v4/entries/by-summoner/{riot_id}?api_key={riot_api_key}"
    response = requests.get(url)
    data = response.json()
    if len(data) > 1:
        tier = data[1]["tier"]
        rank = data[1]["rank"]
        lp = data[1]["leaguePoints"]
        wins = data[1]["wins"]
        losses = data[1]["losses"]
        winrate = round((wins / (wins + losses)) * 100, 2)
        message = f"{tier} {rank} {lp} LP\n{wins}W {losses}L\n{winrate}% winrate"
    else:
        message = "Summoner not found or not ranked."
    send_message(whatsapp_number, message)
    return ""
