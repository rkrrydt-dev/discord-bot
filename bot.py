import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials

# 🔑 TON TOKEN DISCORD
import os
TOKEN = os.getenv("TOKEN")

# 📄 NOM DE TON GOOGLE SHEET
SHEET_NAME = "Trésorie Red Legion's"

# 🔐 CONNEXION GOOGLE
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

import os
import json

creds_dict = json.loads(os.getenv("GOOGLE_CREDS"))
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).worksheet("Compta")

# 🤖 BOT DISCORD
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ BOT CONNECTÉ
@bot.command()
async def argent(ctx):
    benef = sheet.acell("I20").value
    treso = sheet.acell("B4").value

    message = (
        f"💰 Bénéf semaine : {benef}\n"
        f"💵 Trésorerie : {treso}"
    )

    await ctx.send(message)
# ▶️ LANCEMENT
bot.run(TOKEN)