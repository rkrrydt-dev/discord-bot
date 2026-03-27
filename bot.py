import os
import json
import threading
from flask import Flask

import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials

TOKEN = os.getenv("TOKEN")
SHEET_NAME = "NomDeTonSheet"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).worksheet("Compta")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot en ligne"

@app.route("/health")
def health():
    return "OK"

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.command()
async def argent(ctx):
    benef = sheet.acell("I20").value
    treso = sheet.acell("B4").value

    message = (
        f"💰 Bénéf semaine : {benef}\n"
        f"💵 Trésorerie : {treso}"
    )

    await ctx.send(message)

def run_web():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

bot.run(TOKEN)
