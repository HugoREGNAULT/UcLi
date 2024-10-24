import discord, asyncio, json, re, time, random, requests, typing, json, os, uuid, psutil, datetime, warnings, pytz, logging, string, pyfiglet

warnings.filterwarnings('ignore', category = DeprecationWarning)

from discord import ui, app_commands, Interaction, SelectOption, SelectMenu, ButtonStyle, ActionRow, Button
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from discord.utils import get
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import http.client

# ------------------------------------------
# CONFIGURATIONS ET INFORMATIONS GLOBALES
# ------------------------------------------

PERM_ADMIN_ID = 1295717965261443215

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.guilds = True

config_file = "./guilds-config.json" # ./guilds-config.json


bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command('help')


class client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents(members = True, guilds = True))
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        global startTime
        startTime = time.time()
        france_tz = pytz.timezone('Europe/Paris')
        current_time = datetime.now(france_tz)
        formatted_time = current_time.strftime("%d %B %Y - %Hh%M")

        print(formatted_time)
        print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️      │
    │                                             │
    │  {self.user} is  Online ==> ✔️            │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛''')


bot = client()
tree = app_commands.CommandTree(bot)

TOKEN = 'MTAwMTk3MDUyODgzNzQzNTQwMw.G3Uv9I.vfSQ3gE1QkDjedGsC3qRj_Be0b63po19URTFKQ'

structure = {
    "Modération": ["Ban", "Unban", "TimeOut", "UntimeOut", "Warn", "Purge", "Clear", "Kick", "Lock", "Unlock", "DelWarn", "BanList", "ModLogs"],
    "Utilitaires Divers": ["GuessTheNumber", "GStart", "GReroll", "HubJoin", "HubList", "HubLeave", "AddBanList", "UserInfo", "BotInfo", "ServerInfo", "ServerStats", "EmbedBuilder"],
    "Utilitaires Divers 2": ["Ascii", "MSG", "Avatar", "8ball", "Rank", "Join", "Trad", "Skip", "LeaderBoard", "Play", "Register", "Leave", "Repeat"],
    "Minis Jeux": ["Balance", "Work", "Claim", "Rob", "Morpion", "Puissance4"],
    "Social&Profil": ["Like", "Friends", "Request", "FriendStatus", "Create", "Profil", "ProfilSet"],
    "Commandes Basiques": ["Config", "Ping", "Help", "Suggestion", "BugReport", "Support"],
    "Configuration": ["Security", "IA", "Message", "StatsChannels", "AutoRole", "Soutien"],
    "Administration": ["AdminPing", "UpTime", "GuildsList", "AdminLog", "AdminConfig"]
}

@tree.command(name = "setup", description = "Crée les catégories et salons de la structure de base.")
@commands.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    guild = interaction.guild

    for category_name, channels in structure.items():
        category = await guild.create_category(category_name)

        for channel_name in channels:
            formatted_name = f"❌ {channel_name}"
            await guild.create_text_channel(formatted_name, category=category)
    
    await interaction.response.send_message("Catégories et salons créés avec succès !")

bot.run(TOKEN)