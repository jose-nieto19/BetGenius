#!/bin/python

import requests
import json
import time
from datetime import datetime
import telebot

msg_partidos=""
msg_predicciones=""

uri = f'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'XXXXXXXXXXXXXXXXXXXXXX', 'Accept-Encoding': ''}

response = requests.get(uri, headers=headers)
json_response=response.json()

#MOSTRAR LOS PARTIDOS DEL DIA
date = datetime.now()
day=date.day
if(day<10):
    day="0"+str(day)
month=date.month
if(month<10):
    month="0"+str(month)
year=date.year

msg_partidos=msg_partidos+"***********PARTIDOS DEL DIA: "+str(day)+"/"+str(month)+"/"+str(year)+" ************\n\n"

for match in json_response["matches"]:
    date = str(int(match["utcDate"][11:13]) + 2)+":"+match["utcDate"][14:16]
    msg_partidos=msg_partidos+"COMPETICIÓN: "+match["competition"]["name"]+"\nPARTIDO: "+match["homeTeam"]["name"]+"- "+match["awayTeam"]["name"]+"\nHORA INICIO: " + date + "h\n-------------------------------------------\n"

    

bot = telebot.TeleBot("XXXXXXXXXXXXXXXXXXXXXX", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
#bot.set_webhook()

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hola! Bienvenid@ al bot de BetGenius. Elige con los botones del teclado si quieres que te envíe los partidos que hay en el día de hoy o las predicciones para ellos.")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Hola! Bienvenid@ al bot de BetGenius. Esto es lo que hace cada comando:\n /partidos - Te envío los horarios de los partidos que hay en el día de hoy.\n /predicciones - Te envío las predicciones para los partidos que hay en el día de hoy.\n /start - Te envío un mensaje de bienvenida al bot.\n /help - Solicitas ayuda para saber que hace cada comando y te envío la información de ello.")
	
@bot.message_handler(commands=['partidos'])
def send_partidos(message):
	bot.reply_to(message, msg_partidos)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, "Este mensaje o comando no vale. Utiliza los botones del teclado.")

uri = f'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'XXXXXXXXXXXXXXXXXXXXXX', 'Accept-Encoding': ''}
response = requests.get(uri, headers=headers)
if (response.status_code == 200):
    print("API Football --> OK")

if (bot.get_me() is not None):
    print("Bot Telegram --> OK")
	
bot.infinity_polling()
