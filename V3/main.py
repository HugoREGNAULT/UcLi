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

        update_roles_loop.start()
        print('update_roles_loop 🟢')
        bio.start()
        print('bio 🟢')
        stats_channels.start()
        print('stats_channels 🟢')
        #appliquer_interets.start()
        #print('appliquer_interets 🟢')

        global startTime
        startTime = time.time()
        france_tz = pytz.timezone('Europe/Paris')
        current_time = datetime.now(france_tz)
        formatted_time = current_time.strftime("%d %B %Y - %Hh%M")

        startup_message = """
**Bot Démarré avec succès** ✅
-# 🔄 **update_roles_loop** : `UP 🟢`
-# 📋 **bio** : `UP 🟢`
-# 📊 **stats_channels** : `UP 🟢`
-# 🎯 **appliquer_interets** : `DOWN 🔴`

    Tout est opérationnel !
    """

        channel = bot.get_channel(1299049208418144256)
        await channel.send(startup_message)

        print(formatted_time)
        print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️      │
    │                                             │
    │  {self.user} is  Online ==> ✔️            │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛''')


bot = client()
tree = app_commands.CommandTree(bot)

def convert(time):
    pos = ["s", "m", "h", "d"]
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

def parse_duration(duration_str):
    try:
        amount, unit = int(duration_str[:-1]), duration_str[-1]

        if unit == 's':
            return amount
        elif unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 3600
        elif unit == 'd':
            return amount * 86400
        else:
            return None
    except ValueError:
        return None

# ------------------------------------------
# stats_channels
# ------------------------------------------

@tasks.loop(seconds = 300)
async def stats_channels():
    await bot.wait_until_ready()
    l = []
    total_members = 0

    for guild in bot.guilds:
        l.append(str(guild.name) + str(guild.member_count))
        total_members += guild.member_count

    k_number = "{:.2f}k".format(total_members / 1000)

    users_voc_channel = bot.get_channel(1295673591634985018)
    guild_voc_channel = bot.get_channel(1295674283078586399)

    await users_voc_channel.edit(name = '🎉・Utilisateurs : ' + f'{k_number}')
    await guild_voc_channel.edit(name = '🔮・Serveurs : ' + f'{len(bot.guilds)}')

    await asyncio.sleep(300)

# ------------------------------------------
# stats_channels
# ------------------------------------------
# ------------------------------------------
# description / bio
# ------------------------------------------

@tasks.loop(seconds = 10)
async def bio():
    await bot.wait_until_ready()
    total_members = 0
    k_number = ""
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
        k_number = "{:.2f}k".format(total_members / 1000)
    status = [f'{str(len(bot.guilds))} Serveurs', f'{k_number} Utilisateurs', 'V 0.0.1']
    for i in status:
        await bot.change_presence(activity = discord.Game(str(i)))
        await asyncio.sleep(10)

# ------------------------------------------
# description / bio
# ------------------------------------------   
# ------------------------------------------
# /HELP
# ------------------------------------------  

@tree.command(name = 'help', description = 'Affiche la liste des commandes du bot.')
@app_commands.describe(page = 'Choisissez une catégorie')
@app_commands.choices(
    page = [
        app_commands.Choice(name = "🚓 ・ Modération  (13 Commandes)", value = "1"),
        app_commands.Choice(name = "🔧 ・ Utilitaire Divers  (12 Commandes)", value = "2"),
        app_commands.Choice(name = "🎉 ・ Divertissements  (13 Commandes)", value = "3"),
        app_commands.Choice(name = "🏓 ・ Minis - Jeux  (6 Commandes)", value = "4"),
        app_commands.Choice(name = "🎨 ・ NoodleSocial & Profil  (7 Commandes)", value = "5"),
        app_commands.Choice(name = """🌱 ・ Commandes "Basiques"   (6 Commandes)""", value = "6"),
        app_commands.Choice(name = "💎 ・ Configurations  (6 Commandes)", value = "7"),
        app_commands.Choice(name = "📌 ・ Administration Noodle  (5 Commandes)", value = "8"),
        app_commands.Choice(name = "» Prochainement...", value = "9")
    ])
async def help(interaction: discord.Interaction, page: str):
    author_member: discord.Member = interaction.user

    if page == "1":
        embed = discord.Embed(title = '\🚓 ・ Commandes de Modération',
                              description = f'''» `13` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)

        commands = [
    ('<:Members:1295680149697593374> </ban:1189506715696238662> `BAN_MEMBERS`', '> » *Bannir un membre du serveur.*'),
    ('<:Members:1295680149697593374> </unban:1189506715696238663> `BAN_MEMBERS`', '> » *Débannir un ancien membre du serveur.*'),
    ('<:Members:1295680149697593374> </timeout:1189506715696238665> `MODERATE_MEMBERS`', '> » *Exclure temporairement un membre du serveur.*'),
    ('<:Members:1295680149697593374> </untimeout:1189506716409282610> `MODERATE_MEMBERS`', '> » *Redonner la parole à un membre du serveur.*'),
    ('<:Members:1295680149697593374> </warn:1189506716409282611> `MODERATE_MEMBERS`', '> » *Avertir un membre du serveur.*'),
    ('<:Messages:1295679608775118890> </purge:1189506716409282612> `MANAGE_MESSAGES`', '> » *Supprimer tous les messages d\'un salon.*'),
    ('<:Messages:1295679608775118890> </clear:1016023411190927407> `MANAGE_MESSAGES`', '> » *Effacer un nombre X de messages.*'),
    ('<:Members:1295680149697593374> </kick:1189506716912590945> `KICK_MEMBERS`', '> » *Expulser un membre du serveur.*'),
    ('<:Messages:1295679608775118890> </lock:1189506716912590946> `MANAGE_CHANNELS`', '> » *Vérouiller un salon écrit.*'),
    ('<:Messages:1295679608775118890> </unlock:1189506717449457777> `MANAGE_CHANNELS`', '> » *Dévérouiller un salon écrit.*'),
    ('<:Members:1295680149697593374> </delwarn:1189506717449457778> `MODERATE_MEMBERS`', '> » *Supprimer un avertissement d\'un membre du serveur.*'),
    ('<:Members:1295680149697593374> </banlist:1189506717449457779> `MODERATE_MEMBERS`', '> » *Voir la liste des utilisateurs discord bannis par NoodleBot.*'),
    ('<:OneWaySign:1189511733765750865> </modlogs:1189506717449457780>', '> » *Voir la liste des infractions d\'un membre.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "2":
        embed = discord.Embed(title = '\🔧 ・ Utilitaire Divers',
                              description = f'''» `12` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Key:1189517270406418442> </guessthenumber:1189525903320027187> `MODERATE_MEMBERS`', '> » *Lancer un "Cherche le nombre gagnant".*'),
    ('<:Giveaway:1189516089546256434> </gstart:1189525903320027188> `MANAGE_GUILD`', '> » *Créer un giveaway.*'),
    ('<:Giveaway:1189516089546256434> </greroll:1189525903320027189> `MANAGE_GUILD`', '> » *Relancer le giveaway.*'),
    ('<:Flag:1189516434515185715> </hubjoin:1189525903320027190> `ADMINISTRATOR`', '> » *Activer le hub interserver.*'),
    ('<:Flag:1189516434515185715> </hublist:1189525903320027191>', '> » *Afficher la liste des serveurs dans le hub.*'),
    ('<:Flag:1189516434515185715> </hubleave:1189525903320027192> `MANAGE_GUILD`', '> » *Enlever le serveur du hub.*'),
    ('<:Members:1189510759655411762> </addbanlist:1189525903320027193> `MODERATE_MEMBERS`', '> » *Activer le fait de bannir les membres bannis par d\'autres serveurs.*'),
    ('<:MagnifyingGlass:1189516822517649448> </userinfo:1189525903793991771>', '> » *Afficher les informations relatives à un membre.*'),
    ('<:MagnifyingGlass:1189516822517649448> </botinfo:1189525903793991772>', '> » *Afficher les informations actuelles du bot.*'),
    ('<:MagnifyingGlass:1189516822517649448> </serverinfo:1189525903793991773>', '> » *Voir les informations du serveur.*'),
    ('<:Key:1189517270406418442> </serverstats:1189525903793991774>', '> » *Afficher les statistiques d\'un serveur.*'),
    ('<:Key:1189517270406418442> </embedbuilder:1189525903793991775> `ADMINISTRATOR`', '> » *Créer un embed à partir de 0.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "3":
        embed = discord.Embed(title = '\🎉 ・ Divertissement',
                              description = f'''» `13` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Thunder:1189542107732516885> </ascii:1189550272549232702> ', '> » *Transformer un text ou un mot en mode "ASCII".*'),
    ('<:Thunder:1189542107732516885> </msg:1189550273098678333>', '> » *Envoyer secrêtement un message à quelqu\'un.*'),
    ('<:Thunder:1189542107732516885> </avatar:1189550273098678334>', '> » *Afficher l\'avatar d\'un membre.*'),
    ('<:Thunder:1189542107732516885> </8ball:1189550273098678335>', '> » *Poser une question à la boule magique.*'),
    ('<:XP:1189535112665251890> </rank:1189550273098678336>', '> » *Afficher votre classement, niveau et XP.*'),
    ('<:Micro:1189542740334227466> </join:1189550273652346950>', '> » *Faire rejoindre le bot dans un salon vocal.*'),
    ('<:MultiChat:1189543066307149884> </trad:1189550273652346951>', '> » *Traduire, un mot, une phrase, un texte dans une autre langue.*'),
    ('<:Music:1189541335166894152> </skip:1189550273652346952>', '> » *Passer à la musique suivante.*'),
    ('<:XP:1189535112665251890> </leaderboard:1189550274298257409>', '> » *Montre le classement des 10 + actifs.*'),
    ('<:Music:1189541335166894152> </play:1189550274298257410>', '> » *Jouer une musique.*'),
    ('<:Music:1189541335166894152> </register:1189550274298257411>', '> » *Ajouter un titre à votre liste des favoris.*'),
    ('<:Micro:1189542740334227466> </leave:1189550274772205648>', '> » *Faire quitter le bot d\'un channel vocal.*'),
    ('<:Music:1189541335166894152> </repeat:1189550274772205649>', '> » *Rejouer la musique précédente.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "4":

        embed = discord.Embed(title = '\🏓 ・ Minis - Jeux',
                              description = f'''» `6` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Diamond:1189559520666587176> </balance:1189558357959389325> ', '> » *Voir son patrimoine financier.*'),
    ('<:Diamond:1189559520666587176> </work:1189558357959389326>', '> » *Faire un travail rémunéré.*'),
    ('<:Diamond:1189559520666587176> </claim:1189558357959389327>', '> » *Récupérer de l\'argent.*'),
    ('<:Diamond:1189559520666587176> </rob:1189558357959389328>', '> » *Voler de l\'argent à quelqu\'un.*'),
    ('<:Controller:1189559928264871956> </morpion:1189558357959389329>', '> » *Jouer au Morpion (Tic Tac Toe).*'),
    ('<:Controller:1189559928264871956> </puissance4:1189558357959389330>', '> » *Lancer une partie de Puissance 4.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "5":

        embed = discord.Embed(title = '\🎨 ・ UcLiSocial & Profil',
                              description = f'''» `7` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Heart:1189609724635795506> </like:1189612545120673925> ', '> » *Aimer un profil.*'),
    ('<:Heart:1189609724635795506> </friends:1189612545619787826>', '> » *Voir sa liste des amis.*'),
    ('<:Star:1189609722010153022> </request:1189612545619787827>', '> » *Envoyer une demande d\'amis.*'),
    ('<:Heart:1189609724635795506> </friendsstatus:1189612545619787829>', '> » *Voir les demandes d\'amis reçues.*'),
    ('<:Key:1189517270406418442> </create:1189612546227982347>', '> » *Se créer un profil social.*'),
    ('<:Controller:1189559928264871956> </profil:1189612546227982349>', '> » *Voir un profil publique.*'),
    ('<:Key:1189517270406418442> </profilset:1189612546227982350>', '> » *Modifier une partie de son profil publique.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "6":

        embed = discord.Embed(title = '\🌱 ・ Commandes "Basiques"',
                              description = f'''» `6` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Flag:1189516434515185715> </config:1189618352533012600> ', '> » *Faire les configurations de base du bot.*'),
    ('<:Link:1189618705034907748> </ping:1189618352533012601>', '> » *Voir les latences du bot.*'),
    ('<:Heart:1189609724635795506> </help:1180816142030352424>', '> » *Afficher la liste des commandes.*'),
    ('<:Heart:1189609724635795506> </suggestion:1189618352533012602>', '> » *Faire une suggestion pour améliorer le bot.*'),
    ('<:Heart:1189609724635795506> </bugreport:1189618353011183636>', '> » *Report un bug / un problème avec le bot.*'),
    ('<:Members:1189510759655411762> </support:1189618353011183638>', '> » *Avoir le lien du serveur de support du bot.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "7":

        embed = discord.Embed(title = '\💎 ・ Configurations',
                              description = f'''» `5` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:Members:1189510759655411762> </security:1189633555001790596> `MANAGE_GUILD`', '> » *Configurer les systèmes de sécurité.*'),
    ('<:Configurations:1189630693609848934> </ia:1189633555001790597> `MANAGE_CHANNELS`', '> » *Voir les options pour l\'IA intégrée.*'),
    ('<:Messages:1189511252603588648> </messages:1189633555001790599> `MANAGE_GUILD`', '> » *Configurer des messages d\'arrivées et départs.*'),
    ('<:Flag:1189516434515185715> </statschannels:1189633555001790600> `MANAGE_CHANNELS`', '> » *Créer des salons de statistiques personnalisables.*'),
    ('<:Configurations:1189630693609848934> </autorole:1189633555442180127> `ADMINISTRATOR`', '> » *Configurer le fait de donner un rôle automatiquement à un nouvel arrivant.*'),
    ('<:OneWaySign:1189511733765750865> </soutien:1189640939338219540> `ADMINISTRATOR`', '> » *Donner un rôle automatiquement en fonction d\'une bio.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

    if page == "8":

        embed = discord.Embed(title = '\📌 ・ Administration Noodle"',
                              description = f'''» `4` **commandes disponibles**
• `PERMISSIONS` : Permission que vous devez avoir pour pouvoir utiliser la commande.''',
                              color = 0x151976)
        
        commands = [
    ('<:OneWaySign:1189511733765750865> </adminping:1189633555442180128> `1183205593381601380`', '> » *Voir tous les ping concernant Noodle (Site, VPS...).*'),
    ('<:OneWaySign:1189511733765750865> </uptime:1189633555442180129> `1183205593381601380`', '> » *Affiche le temps de fonctionnement de Noodle*'),
    ('<:OneWaySign:1189511733765750865> </guildslist:1189633555442180130> `1183205593381601380`', '> » *Envoi la liste des serveurs sur lequel est NoodleBot.*'),
    ('<:OneWaySign:1189511733765750865> </adminlog:1189633555442180131> `1183205593381601380`', '> » *Voir les dernières actions faites avec le bot.*'),
    ('<:OneWaySign:1189511733765750865> </adminconfig:1189902299506692116> `1183205593381601380`', '> » *Configurer les options administratives du bot.*')
]

        for command, description in commands:
            embed.add_field(name = command, value = description, inline = False)

            embed.set_footer(text = f'Latence du bot : {round(bot.latency * 1000)}ms')
            embed.timestamp = datetime.now()

        await interaction.response.send_message(embed = embed, ephemeral = True)

# ------------------------------------------
# /HELP
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                          MODERATION COMMANDS                                                                           #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

@tree.command(name = 'ban', description = 'Bannir un membre du serveur.')
@app_commands.default_permissions(ban_members = True)
async def ban(interaction: discord.Interaction, membre : discord.Member, reason: str = '''Aucune raison précisée.'''):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''<:UserError:1191512488932540476> Vous ne pouvez pas vous bannir vous - même !''', ephemeral = True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''<:UserPermissionsError:1191513416020533398> Vous ne pouvez pas bannir cette personne car elle est à un rôle supérieur à vous !''', ephemeral = True)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !''', ephemeral = True)

    try:
        await membre.send(f'''## \🔒 **Bannissement du Serveur `{interaction.guild.name}`. **

Salut {membre.mention},
Nous espérons que ce message te trouve bien. Malheureusement, nous devons t'informer que tu as été banni du serveur **`{interaction.guild.name}`** par __{author_member.mention}__.

\📜 **Raison du Bannissement :**
```diff
- {reason}
```

\📌 **Si tu as des questions ou si tu souhaites discuter de cette décision, n'hésite pas à contacter l'administrateur responsable.**

> Nous te rappelons que le respect des règles du serveur est crucial pour maintenir un environnement positif pour tous les membres. Nous espérons que tu comprends cette mesure et que tu pourras apprendre de cette expérience.

Cordialement,
L'équipe de modération de **`{interaction.guild.name}`** .''')
        await interaction.guild.ban(membre, reason = reason)
        await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} **à été banni !**', ephemeral = True)

    except:
        return await interaction.response.send_message(
            f'''<:BotError:1191522519824478269> Je n'arrive pas à bannir ce membre !''', ephemeral = True)

@tree.command(name = 'unban', description = 'Débannir un ancien membre du serveur.')
@app_commands.default_permissions(ban_members = True)
async def unban(interaction: discord.Interaction, membre: discord.User):
    author_member: discord.Member = interaction.user

    try:
        await interaction.guild.unban(membre)
        await interaction.response.send_message(f'<:Valid:1191522096958939236> `{membre}` **à correctement été débanni !**', ephemeral = True)
    except:
        await interaction.response.send_message(f'''<:BotError:1191522519824478269> **Ce membre n'est pas banni de ce serveur.**''', ephemeral=True)

@tree.command(name = 'timeout', description = 'Exclure temporairement un membre du serveur.')
@app_commands.default_permissions(moderate_members = True)
async def timeout(interaction: discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison n'a été précisée''', days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Vous ne pouvez pas vous exclure temporairement vous - même !', ephemeral = True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'<:UserPermissionsError:1191513416020533398> Vous ne pouvez pas exclure temporairement cette personne car elle est à un rôle supérieur à vous !', ephemeral = True)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !', ephemeral = True)

    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28):
        return await interaction.response.send_message(f'<:Info:1191696749178408970> La durée d\'exclusion doit être inférieure à `28` jours !', ephemeral = True)

    end_timestamp_utc = int((datetime.now() + duration).timestamp())
    duration_str = f'<t:{end_timestamp_utc}:R>'

    await membre.send(f'''## \⌛ **Timeout du Serveur `{interaction.guild.name}`. **

Salut {membre.mention}, tu as été temporairement exclu du serveur **`{interaction.guild.name}`** par __{author_member.mention}__.
> \⏰ **Durée du Timeout :** `{duration}`

\📜 **Raison du Timeout :**
```diff
+ {reason}
```

\📌 *Tu retrouveras ta parole sur ce serveur,* **{duration_str}**.''')
    await membre.timeout(duration, reason = reason)

    await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} a été temporairement exclu ({duration}) !', ephemeral = True) 

@tree.command(name = 'untimeout', description = 'Redonner la parole à un membre du serveur.')
async def untimeout(interaction: discord.Interaction, membre: discord.Member):
    author_member: discord.Member = interaction.user

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !', ephemeral=True)

    duration = timedelta(days = 0, hours = 0, minutes = 0, seconds = 1)
    await membre.timeout(timedelta(seconds = 0))
    await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} a été rétabli !', ephemeral = True)

data_file = './data_infractions.json'

@tree.command(name = 'warn', description = 'Avertir un membre du serveur.')
@app_commands.default_permissions(moderate_members = True)
async def warn(interaction: discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison n'a été précisée'''):
    author_member: discord.Member = interaction.user

    try:
        with open(data_file, 'r') as f:
            warnings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        warnings = {}

    guild_id = interaction.guild_id
    current_time = int(datetime.now().timestamp())

    if str(membre.id) in warnings:
        warnings[str(membre.id)].append({
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'membre_name': membre.display_name,
            'timestamp': current_time,
            'guild_name': interaction.guild.name
        })
    else:
        warnings[str(membre.id)] = [{
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'membre_name': membre.display_name,
            'timestamp': current_time,
            'guild_name': interaction.guild.name
        }]

    with open(data_file, 'w') as f:
        json.dump(warnings, f, indent = 2)
    
    await membre.send(f'''## <:UserError:1191512488932540476> **Avertissement sur le Serveur `{interaction.guild.name}`. **
Salut {membre.mention}, tu viens de recevoir un avertissement sur le serveur **`{interaction.guild.name}`** de la part de __{author_member.mention}__.

> \📜 **Raison de l'avertissement :**
```diff
+ {reason}
```
\📌 *N'oublie pas de respecter les règles du serveur. Pour consulter la liste de tes avertissements, utilise la commande </modlogs:1189506717449457780>.*''')
    await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} a été warn. Pour voir la liste des warns, utilisez </modlogs:1189506717449457780>.', ephemeral = True)

@tree.command(name = 'purge', description = 'Supprimer le salon et en créer un nouveau au même endroit.')
@app_commands.default_permissions(manage_channels = True)
async def purge(interaction: discord.Interaction, channel: discord.TextChannel):
    author_member: discord.Member = interaction.user
    category = channel.category
    position = channel.position

    if category:
        mention_author = f'<@{author_member.id}>'
        await channel.delete()

        new_channel = await category.create_text_channel(name=channel.name, position=position)
        await new_channel.send(f'<:IntegrationsChannelsFollowed:1191717286407577670> {mention_author} à recréé ce salon avec succès à l\'aide du </purge:1189506716409282612> .')
        response_message = f'<:IntegrationsChannelsFollowed:1191717286407577670> Salon supprimé et recréé avec succès.'
    else:
        response_message = f'<:IntegrationsChannelsFollowed:1191717286407577670> La catégorie du salon n\'a pas pu être déterminée. Le salon n\'a pas été supprimé, ni recréé.'

    await interaction.response.send_message(response_message, ephemeral = True)

@tree.command(name = 'clear', description = 'Effacer un nombre X de messages.')
async def clear(interaction: discord.Interaction, nombre_de_message : int):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'kick', description = 'Expulser un membre du serveur.')
async def kick(interaction: discord.Interaction, membre : discord.Member, reason: str = '''Aucune raison précisée.'''):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'lock', description = 'Vérouiller un salon écrit.')
async def lock(interaction: discord.Interaction, channel: discord.TextChannel):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'unlock', description = 'Dévérouiller un salon écrit.')
async def unlock(interaction: discord.Interaction, channel : discord.TextChannel):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'delwarn', description = 'Supprimer un avertissement d\'un membre du serveur.')
async def delwarn(interaction: discord.Interaction, membre : discord.Member, warn_id : int):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'banlist', description = 'Voir la liste des utilisateurs discord bannis par NoodleBot.')
async def banlist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'modlogs', description = 'Voir la liste des infractions d\'un membre.')
async def modlogs(interaction: discord.Interaction, membre : discord.Member):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                          MODERATION COMMANDS                                                                           #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                      UTILITAIRE / DIVERS COMMANDS                                                                      #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name = 'guessthenumber', description = 'Lancer un "Cherche le nombre gagnant".')
async def guessthenumber(interaction: discord.Interaction, channel: discord.TextChannel, number_max : int):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'gstart', description = 'Créer un giveaway.')
async def gstart(interaction: discord.Interaction, durée: str, gagnants: int, lot: str):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'greroll', description = 'Relancer le giveaway.')
async def greroll(interaction: discord.Interaction, id: int):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'hubjoin', description = 'Activer le hub interserver.')
async def hubjoin(interaction: discord.Interaction, channel: discord.TextChannel):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'hublist', description = 'Afficher la liste des serveurs dans le hub.')
async def hublist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'hubleave', description = 'Enlever le serveur du hub.')
async def greroll(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'addbanlist', description = 'Activer le fait de bannir les membres bannis par d\'autres serveurs.')
async def addbanlist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name='userinfo', description='Afficher les informations relatives à un membre.')
async def userinfo(interaction: discord.Interaction, membre: discord.Member):
    userFlags = membre.public_flags.all()

    badge_emojis = {
        'discord_employee': '<:DiscordStaff:1191856488021491843>',
        'discord_partner': '<:PartneredServerOwner:1191856486423474286>',
        'hypesquad_events': '<:HypesquadEvents:1191856482350792794>',
        'hypesquad_bravery': '<:HypesquadHouseOfBravery:1191856495327969400>',
        'hypesquad_brilliance': '<:HypesquadHouseOfBrilliance:1191856798399996066>',
        'hypesquad_balance': '<:HypesquadHouseOfBalance:1191856498519851048>',
        'early_supporter': '<:EarlySupporter:1191856729449844806>',
        'bughunter_level_1': '<:BugHunter:1191856479012147300>',
        'bughunter_level_2': '<:BugHunterLevel2EmojiID>',
        'active_developer': '<:ActiveDeveloper:1191856490127040582>',
        'verified_bot': '<:BOTVerified:1191724979226689637>',
    }

    badges = [badge_emojis.get(flag.name, flag.name) for flag in userFlags]

    embed = discord.Embed(title = f'\📌 Informations sur {membre.name}', color = 0X1A2B60)

    embed.add_field(name = '''<:GuildsMembers:1191803373897400390> Informations Générales''',
                    value=f'''> » **Pseudo** : `{membre.name}#{membre.discriminator}`
    > » **ID** : `{membre.id}`.
    > » **Créé le** : <t:{int(membre.created_at.timestamp())}:D> (<t:{int(membre.created_at.timestamp())}:R>)
    > » **Badge(s)** : {" ; ".join(badges)}''', inline = True)

    embed.add_field(name = f'''<:IntegrationsChannelsFollowed:1191717286407577670> Informations de {membre.name} sur le Serveur''',
                    value = f'''> » **Rejoint le** : <t:{int(membre.joined_at.timestamp())}:D> (<t:{int(membre.joined_at.timestamp())}:R>)
    > » **Surnom** : `{membre.nick if membre.nick else "Aucun"}`
    > » **Bot** : {"<:DiscordStatusOnline:1184534287932989460>" if membre.bot else "<:Danger:1296505953155416132>"}''', inline = False)

    embed.add_field(name = f'Rôles (`{len(membre.roles) - 1}`)', value = f'''```{""" ; """.join([role.name for role in membre.roles[1:]]) if len(membre.roles) > 1 else "Aucun"}
```''', inline = True)

    embed.add_field(name = f'''Serveurs en commun entre {membre.name} et NoodleBot''',
                    value = f'''```diff
{"+ ".join([f"""- {guild.name}
""" for guild in membre.mutual_guilds])}
```''', inline = False)

    embed.set_thumbnail(url = membre.avatar.url)

    await interaction.response.send_message(embed = embed, ephemeral = True)

@tree.command(name = 'botinfo', description = 'Afficher les informations actuelles du bot.')
async def botinfo(interaction: discord.Interaction):
    author_member : discord.Member = interaction.user

    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count

    start_time = time.time()
    id = bot.user.id
    created_at_time = interaction.guild.created_at.strftime(f'%d/%m/%Y %H:%M:%S')
    ping = round(bot.latency * 1000, 2)
    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds=difference))
    version = discord.__version__
    servers_count = len(bot.guilds)

    headers = {'Authorization': 'Bearer ptlc_iOulNmU5AHYroZh0fmdE8gZMM0sA7OE2tzZY2ayVZhZ'}
    response = requests.get("https://panel.paladium-bot.fr/api/client/servers/2679a683/resources", headers = headers)

    if response.status_code == 200:
            data = response.json()['attributes']["resources"]

    ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)

    embed = discord.Embed(title = f'» Informations sur le Bot', 
                          description = f'''> Pour plus d'informations sur le bot, cliquez __[`ici`](https://panel.berchbrown.me/server/b1545927)__.
    » **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes** : `31`
    » **Préfix** : `/`''', color = 0X1A2B60)

    embed.add_field(name = '''\📌 Informations Générales''', value = f'''> » **Créateur** : <@947519926137143409>
    > » **Développeurs** : `sirop2menthe_`''', inline = True)

    embed.add_field(name = f'''\📊 Statistiques''', value = f'''> » **Serveurs** : `{str(servers_count)}`
    > » **Utilisateurs** : `{total_members}`
    > » **Commandes** : `82`''', inline = False)

    embed.add_field(name = f'''\🔧 Informations sur Système''', value = f'''> » **Hébergeur** : [`VPSHebergAccess`](https://panel.berchbrown.me/server/b1545927)
    > » **Plateforme** : `VPS Linux - 04`
    > » **Processeur** : `3.30 GHz 2 vCore(s) Xeon® E5`
    > » **Mémoire RAM** : `{ram_used} / {(psutil.virtual_memory().total // (1024 ** 2))} Mo`''', inline = False)

    embed.add_field(name = '''\👾 Informations sur le Bot''', value = f'''> » **Temps de Connexion** : `{str(uptime)}`
    > » **DataBase** : `En cours de création...`
    > » **Discord.py** : `{version}`
    > » **Version du Bot** : `V2.1 (BETA)`
    > » **ID** : `962051231973511318`''', inline = False)
    
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1181292316892348429/1191885351975915580/Frame_2608834.png?ex=65a710bc&is=65949bbc&hm=0f8bb48b5217078d35217ad7e87272083bf3b9c3d6464b07d9e9fd099acbd76c&')
    embed.set_footer(text = 'NoodleBot © 2024 Tous Droits Réservés.', icon_url = 'https://cdn.discordapp.com/attachments/1181292316892348429/1191885351975915580/Frame_2608834.png?ex=65a710bc&is=65949bbc&hm=0f8bb48b5217078d35217ad7e87272083bf3b9c3d6464b07d9e9fd099acbd76c&')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed, view = view_linkedbutton(), ephemeral = True)

class view_linkedbutton(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(style = discord.ButtonStyle.primary, label = 'Discord Support', url = 'https://discord.gg/W3g8aV6EFK', emoji = '<:Link:1191708382550294588>'))

@tree.command(name = 'serveurinfo', description = 'Voir les informations du serveur.')
async def serveurinfo(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    threads = len(guild.threads)
    roles = [role for role in guild.roles[1:] if not role.managed][:20]
    num_roles = len(roles)
    boost_count = guild.premium_subscription_count
    boost_level = guild.premium_tier
    verification_level = guild.verification_level.name
    member_count = sum(not member.bot for member in guild.members)
    online_count = sum(member.status == discord.Status.online for member in guild.members)
    offline_count = sum(member.status == discord.Status.offline for member in guild.members)
    streaming_count = sum(
        activity.type == discord.ActivityType.streaming for member in guild.members for activity in member.activities)
    dnd_count = sum(member.status == discord.Status.dnd for member in guild.members)
    emojis = guild.emojis
    num_emojis = len(emojis)
    animated_emojis = []
    normal_emojis = []

    for emoji in emojis:
        if emoji.animated:
            if len(animated_emojis) < 25:
                animated_emojis.append(str(emoji))
        else:
            if len(normal_emojis) < 25:
                normal_emojis.append(str(emoji))

        if len(normal_emojis) + len(animated_emojis) >= 50:
            break

    emojis_str = " ; ".join(normal_emojis + animated_emojis)[:1000]

    embed = discord.Embed()
    embed.set_author(name = f'Informations du serveur {guild.name}', icon_url = guild.icon.url)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)



    embed = discord.Embed(title = '\📜 Informations du serveur.',
                          description = f'''> » Salons Textuels : `{text_channels}` ; Salons Vocaux : `{voice_channels}` ; Fils : `{threads}` ; Rôles : `{num_roles}`''',
                          color = 0X1A2B60)

    embed.add_field(name = '» Propriétaire', value = f'''{guild.owner.mention} ||{guild.owner.id}||''', inline = False)
    embed.add_field(name = '» Membres', value = member_count, inline = True)
    embed.add_field(name = '» Boosts', value = f"{boost_count} boost(s) (Palier {boost_level})", inline = True)
    embed.add_field(name = '» Niveau de Verif\'', value = verification_level, inline = True)

    if num_roles > 20:
        role_mentions = [role.mention for role in roles]
        role_mentions.append("...")
    else:
        role_mentions = [role.mention for role in roles]

    embed.add_field(name = '» Rôles', value = " ; ".join(role_mentions), inline = False)
    embed.add_field(name = '» Online', value = online_count, inline = True)
    embed.add_field(name = '» Offline', value = offline_count, inline = True)
    embed.add_field(name = '» Ne pas Déranger', value = dnd_count, inline = True)
    embed.add_field(name = f'» Emojis ({num_emojis})', value = f"{emojis_str}", inline = False)
    embed.add_field(name = "» Date de création", value = f'<t:{int(datetime.timestamp(guild.created_at))}:D> (<t:{int(datetime.timestamp(guild.created_at))}:R>)', inline = False)
    embed.add_field(name = "» Rejoint le", value = f'<t:{int(guild.me.joined_at.timestamp())}:D> (<t:{int(guild.me.joined_at.timestamp())}:R>)', inline = False)

    embed.set_thumbnail(url = guild.icon.url)
    embed.set_footer(text = '© 2023 NoodleBot - Tous droits réservés', icon_url = 'https://cdn.discordapp.com/attachments/1181292316892348429/1191881490481545336/Frame_2608834.png?ex=65a70d23&is=65949823&hm=f4160efe57769a9664859f75af4f200aa28b6b3d7c76131697995f2aa7e2321b&')
    embed.timestamp = datetime.now()

    await interaction.response.send_message(embed = embed, ephemeral = True)

@tree.command(name = 'serverstats', description = 'Afficher les statistiques d\'un serveur.')
async def serverstats(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'embedbuilder', description = 'Créer un embed à partir de 0.')
async def embedbuilder(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                      UTILITAIRE / DIVERS COMMANDS                                                                      #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       DIVERTISSEMENTS COMMANDS                                                                         #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name = 'ascii', description = 'Transformer un text ou un mot en mode "ASCII"')
async def ascii(interaction: discord.Interaction, texte: str):
    author_member: discord.Member = interaction.user
    
    ascii_art = pyfiglet.figlet_format(texte)

    await interaction.response.send_message(f'''```
{ascii_art}
```''')

@tree.command(name = 'msg', description = 'Envoyer secrêtement un message à quelqu\'un.')
async def msg(interaction: discord.Interaction, destinataire: discord.Member, message: str):
    author_member: discord.Member = interaction.user

    await destinataire.send(message)
    await interaction.response.send_message(f'<:Valid:1191522096958939236> Message correctement envoyé à {destinataire.mention}', ephemeral = True)

@tree.command(name = 'avatar', description = 'Afficher l\'avatar d\'un membre.')
async def avatar(interaction: discord.Interaction, membre: discord.Member):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

eight_ball_responses = [
    "Oui, sans aucun doute.",
    "Non, absolument pas.",
    "C'est certain.",
    "Je ne pense pas.",
    "Demande-moi plus tard.",
    "Je n'en suis pas si sûr.",
    "Les signes pointent vers oui.",
    "Ma réponse est non.",
    "Il est décidé que oui.",
    "Réponse floue, réessaye.",
    "Compte là-dessus.",
    "Ne compte pas dessus.",
    "Cela semble prometteur.",
    "Les perspectives ne sont pas bonnes.",
    "C'est très probable.",
    "Je ne peux pas prédire ça maintenant.",
    "Tu peux compter là-dessus.",
    "Pas aujourd'hui.",
    "C'est presque sûr.",
    "La réponse est en toi.",
    "Peut-être bien.",
    "Certainement.",
    "Les étoiles disent non.",
    "Il est trop tôt pour le dire.",
    "Cela semble incertain.",
    "Oui, mais prépare-toi au pire.",
    "Non, mais il y a un espoir.",
    "La chance est de ton côté.",
    "Je ne sais pas pour l'instant.",
    "Il y a de fortes chances."
]

@tree.command(name='8ball', description='Poser une question à la boule magique.')
async def ball(interaction: discord.Interaction, question: str):
    author_member: discord.Member = interaction.user

    response = random.choice(eight_ball_responses)
    embed = discord.Embed(
        title="🎱 Boule Magique 8ball 🎱",
        description=f"**Question** : {question}",
        color=discord.Color.purple()  # Couleur de l'embed
    )

    embed.add_field(name="Réponse", value=response, inline=False)
    embed.set_footer(text=f"Question posée par : {author_member.display_name}", icon_url=author_member.avatar.url if author_member.avatar else None)
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'rank', description = 'Afficher votre classement, niveau et XP.')
async def rank(interaction: discord.Interaction, membre: discord.Member = None):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'join', description = 'Faire rejoindre le bot dans un salon vocal.')
async def join(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'trad', description = 'Activer le fait de bannir les membres bannis par d\'autres serveurs.')
@app_commands.describe(langue_1 = 'Choisissez la langue de votre texte')
@app_commands.choices(
    langue_1 = [
        app_commands.Choice(name = "FR (France)", value = "1"),
        app_commands.Choice(name = "AN (English)", value = "2"),
    ]
)
async def trad(interaction: discord.Interaction, langue_1: str, texte: str, langue_2: str):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'skip', description = 'Passer à la musique suivante.')
async def skip(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'play', description = 'Jouer une musique.')
async def play(interaction: discord.Interaction, titre_et_artiste:str):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'register', description = 'Ajouter un titre à votre liste des favoris.')
async def register(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'leave', description = 'Faire quitter le bot d\'un channel vocal.')
async def leave(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'repeat', description = 'Rejouer la musique précédente.')
async def repeat(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       DIVERTISSEMENTS COMMANDS                                                                         #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                        MINIS - JEUX COMMANDS                                                                           #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
@tree.command(name = 'balance', description = 'Voir son patrimoine financier.')
async def balance(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'work', description = 'Faire un travail rémunéré.')
async def work(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'claim', description = 'Récupérer de l\'argent.')
async def claim(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

# ------------------------------
# Puissance 4
# ------------------------------

ROWS = 6
COLUMNS = 7

PLAYER_TOKENS = {
    '1': '🔴',  # Joueur 1
    '2': '🟡'   # Joueur 2
}

STATS_FILE = './puissance4_stats.json'

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def update_stats(winner_id, loser_id):
    stats = load_stats()

    if winner_id not in stats:
        stats[winner_id] = {'wins': 0, 'losses': 0}
    if loser_id not in stats:
        stats[loser_id] = {'wins': 0, 'losses': 0}

    stats[winner_id]['wins'] += 1
    stats[loser_id]['losses'] += 1

    save_stats(stats)

def calculate_ratio(stats):
    wins = stats['wins']
    losses = stats['losses']
    if losses == 0:
        return float('inf') if wins > 0 else 0
    return wins / losses

class Puissance4(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=None)
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.board = [['⚪' for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.game_over = False

        for i in range(COLUMNS):
            self.add_item(ColumnButton(i))

    def display_board(self):
        return '\n'.join([' '.join(row) for row in self.board])

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def insert_token(self, column, token):
        for row in range(ROWS-1, -1, -1):
            if self.board[row][column] == '⚪':
                self.board[row][column] = token
                return row

    def check_win(self, row, col, token):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Droite, Bas, Diagonale /
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == token:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, col - dc * i
                if 0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == token:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    async def end_game(self, interaction, winner, loser):
        self.game_over = True
        self.clear_items()  # Désactiver les boutons
        update_stats(str(winner.id), str(loser.id))  # Mettre à jour les statistiques
        await interaction.response.edit_message(content=f'{winner.mention} a gagné la partie !\n\n{self.display_board()}', view=self)

class ColumnButton(discord.ui.Button):
    def __init__(self, column):
        super().__init__(label=str(column + 1), style=discord.ButtonStyle.primary, custom_id=str(column))
        self.column = column

    async def callback(self, interaction: discord.Interaction):
        view: Puissance4 = self.view
        if interaction.user != view.current_player:
            await interaction.response.send_message("Ce n'est pas votre tour.", ephemeral=True)
            return

        if view.game_over:
            await interaction.response.send_message("La partie est terminée.", ephemeral=True)
            return

        token = PLAYER_TOKENS['1'] if view.current_player == view.player1 else PLAYER_TOKENS['2']
        row = view.insert_token(self.column, token)
        if row is None:
            await interaction.response.send_message("Cette colonne est pleine. Choisissez une autre colonne.", ephemeral=True)
            return

        if view.check_win(row, self.column, token):
            winner = view.current_player
            loser = view.player1 if winner == view.player2 else view.player2
            await view.end_game(interaction, winner, loser)
        else:
            view.switch_player()  # Passer au joueur suivant
            await interaction.response.edit_message(content=f"Tour de {view.current_player.mention} !\n\n{view.display_board()}", view=view)

@tree.command(name='puissance4', description='Lancer une partie de Puissance 4.')
async def puissance4(interaction: discord.Interaction, adversaire: discord.Member):
    author_member: discord.Member = interaction.user
    if author_member == adversaire:
        await interaction.response.send_message("Vous ne pouvez pas jouer contre vous-même.", ephemeral=True)
        return

    view = Puissance4(author_member, adversaire)
    await interaction.response.send_message(f"Partie de Puissance 4 entre {author_member.mention} et {adversaire.mention} !\n\n{view.display_board()}", view=view)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                        MINIS - JEUX COMMANDS                                                                           #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  NOODLESOCIAL & PROFIL COMMANDS                                                                        #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def load_data():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump({}, f)
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# Initialiser les données si elles n'existent pas pour un utilisateur
def init_user_data(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {
            "profil": {},
            "friends": [],
            "friend_requests": []
        }
        save_data(data)

def add_friend(user_id, friend_id):
    data = load_data()
    data[str(user_id)]["friends"].append(friend_id)
    save_data(data)

def add_friend_request(user_id, from_id):
    data = load_data()
    data[str(user_id)]["friend_requests"].append(from_id)
    save_data(data)

def accept_friend_request(user_id, from_id):
    data = load_data()
    if from_id in data[str(user_id)]["friend_requests"]:
        data[str(user_id)]["friend_requests"].remove(from_id)
        data[str(user_id)]["friends"].append(from_id)
        data[str(from_id)]["friends"].append(user_id)
        save_data(data)

@tree.command(name='like', description='Aimer un profil.')
async def like(interaction: discord.Interaction, profil: discord.Member):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Vous avez aimé le profil de {profil.display_name}.', ephemeral=True)

@tree.command(name='friends', description='Voir sa liste des amis.')
async def friends(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    init_user_data(author_member.id)

    data = load_data()
    friends_list = data[str(author_member.id)]["friends"]
    
    if friends_list:
        friends_names = ', '.join([f"<@{friend_id}>" for friend_id in friends_list])
        await interaction.response.send_message(f'Vos amis : {friends_names}.', ephemeral=True)
    else:
        await interaction.response.send_message('Vous n\'avez pas encore d\'amis.', ephemeral=True)

@tree.command(name='request', description='Envoyer une demande d\'amis.')
async def request(interaction: discord.Interaction, profil: discord.Member):
    author_member: discord.Member = interaction.user
    init_user_data(profil.id)
    init_user_data(author_member.id)

    add_friend_request(profil.id, author_member.id)
    await interaction.response.send_message(f'Vous avez envoyé une demande d\'ami à {profil.display_name}.', ephemeral=True)

@tree.command(name='friendsstatus', description='Voir les demandes d\'amis reçues.')
async def friendsstatus(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    init_user_data(author_member.id)

    data = load_data()
    requests_list = data[str(author_member.id)]["friend_requests"]
    
    if requests_list:
        requests_names = ', '.join([f"<@{req_id}>" for req_id in requests_list])
        await interaction.response.send_message(f'Vous avez des demandes d\'amis de : {requests_names}.', ephemeral=True)
    else:
        await interaction.response.send_message('Vous n\'avez pas de demandes d\'amis en attente.', ephemeral=True)

@tree.command(name='create', description='Se créer un profil social.')
async def create(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    init_user_data(author_member.id)

    await interaction.response.send_message(f'Votre profil a été créé avec succès !', ephemeral=True)

@tree.command(name='profil', description='Voir un profil publique.')
async def profil(interaction: discord.Interaction, profil: discord.Member):
    init_user_data(profil.id)
    
    data = load_data()
    profil_data = data[str(profil.id)]["profil"]
    
    if profil_data:
        await interaction.response.send_message(f'Profil de {profil.display_name} : {profil_data}.', ephemeral=True)
    else:
        await interaction.response.send_message(f'{profil.display_name} n\'a pas encore configuré son profil.', ephemeral=True)

@tree.command(name='profilset', description='Modifier une partie de son profil publique.')
async def profilset(interaction: discord.Interaction, key: str, value: str):
    author_member: discord.Member = interaction.user
    init_user_data(author_member.id)

    data = load_data()
    data[str(author_member.id)]["profil"][key] = value
    save_data(data)

    await interaction.response.send_message(f'Votre profil a été mis à jour : {key} = {value}.', ephemeral=True)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  NOODLESOCIAL & PROFIL COMMANDS                                                                        #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                          BASIC COMMANDS                                                                                #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

@tree.command(name = 'config', description = 'Faire les configurations de base du bot.')
async def config(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'ping', description = 'Voir les latences du bot.')
async def ping(interaction: discord.Interaction, profil: discord.Member):
    author_member: discord.Member = interaction.user

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds = difference))

    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    headers = {'Authorization': 'Bearer ptlc_iOulNmU5AHYroZh0fmdE8gZMM0sA7OE2tzZY2ayVZhZ'}

    discord_status_response = requests.get("https://discordstatus.com/metrics-display/5k2rt9f7pmny/day.json")

    if discord_status_response.status_code == 200:
        try:
            discord_data = discord_status_response.json()
            discord_latency = discord_data['summary']['last']
        except json.JSONDecodeError as e:
            print(f"Error decoding Discord status JSON: {e}")
            discord_latency = '''Erreur de décodage du statut Discord JSON'''
    else:
        print(f"Error accessing Discord status API. Status code: {discord_status_response.status_code}")
        discord_latency = '''Erreur d'accès à l'API de statut de Discord'''

    response = requests.get("https://panel.berchbrown.me/api/client/servers/b1545927/resources", headers = headers)

    if response.status_code == 200:
        try:
            data = response.json()['attributes']["resources"]
            ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)
        except json.JSONDecodeError as e:
            print(f"Error decoding server response JSON: {e}")
            ram_used = '''Erreur de décodage de la réponse du serveur JSON'''
    else:
        print(f"Error accessing server resources API. Status code: {response.status_code}")
        ram_used = '''Erreur d'accès aux ressources du serveur API'''

    uptime_str = ""
    days, remainder = divmod(difference, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        uptime_str += f"{days} jour{'s' if days > 1 else ''}, "
    if hours > 0 or days > 0:
        uptime_str += f"{hours} heure{'s' if hours > 1 else ''}, "
    if minutes > 0 or hours > 0 or days > 0:
        uptime_str += f"{minutes} minute{'s' if minutes > 1 else ''}, "
    uptime_str += f"{seconds} seconde{'s' if seconds > 1 else ''}"

    def get_website_ping(url):
        conn = http.client.HTTPConnection(url)
        conn.request("GET", "/")
        response = conn.getresponse()
        return response.getheader('X-Response-Time')

    website_url = "noodle-bot.fr"
    website_ping = get_website_ping(website_url)

    embed = discord.Embed(title = '\🏓 Pong !', color = 0X151976)
    embed.add_field(name = '> Latence VPS <:Online:1184534287932989460>',
                    value = f'» `{response.elapsed.total_seconds() * 1000:.2f}ms`', inline = False)

    embed.add_field(name = '> SiteWeb <:Online:1184534287932989460>', value = f'» `{website_ping}ms`')
    embed.add_field(name = '> API <:Online:1184534287932989460>', value = f'» `{response.elapsed.total_seconds() * 100:.2f}ms`')
    embed.add_field(name = '> Ping Bot <:Online:1184534287932989460>', value = f'» `{round(bot.latency * 1000)}ms`')
    embed.add_field(name = '> Latence Discord <:Online:1184534287932989460>', value = f'» `{discord_latency}ms`')
    embed.add_field(name = '> RAM Utilisée <:Online:1184534287932989460>', value = f'» `{ram_used} Mo / {(psutil.virtual_memory().total // (1024 ** 2))} Mo`')
    embed.add_field(name = '> Lancé depuis :', value = f'`{uptime_str}`')

    await interaction.response.send_message(embed = embed, ephemeral = True)

@tree.command(name = 'suggestion', description = 'Faire une suggestion pour améliorer le bot.')
async def suggestion(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'bugreport', description = 'Report un bug / un problème avec le bot.')
async def bugreport(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'support', description = 'Avoir le lien du serveur de support du bot.')
async def support(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                          BASIC COMMANDS                                                                                #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     CONFIGURATIONS COMMANDS                                                                            #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@tree.command(name = 'security', description = 'Configurer les systèmes de sécurité.')
@commands.has_permissions(administrator=True)
async def security(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'ia', description = 'Voir les options pour l\'IA intégrée.')
@commands.has_permissions(administrator = True)
async def ia(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(
        title = "Accès Premium Requis \🚀",
        description = f"> \📌 Désolé, l'accès à la fonctionnalité </ia:1189633555001790597> est réservé aux **utilisateurs premium** <:PremiumBot:1191708380226654270>.",
        color = 0XFFB44F)

    embed.add_field(
        name = "\🔮 Avantages Premium",
        value = "Pour profiter de cette option et d'autres avantages exclusifs, veuillez envisager de passer à un [<:Link:1191708382550294588> abonnement premium](https://noodlebot.io/premium).",
        inline = False)

    embed.set_footer(text = "Merci pour votre compréhension ! 🌟")

    await interaction.response.send_message(embed = embed, ephemeral = True)
 

@tree.command(name = 'messages', description = 'Configurer des messages d\'arrivées et départs.')
@commands.has_permissions(administrator=True)
async def messages(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name='statschannels', description='Créer des salons de statistiques personnalisables.')
@commands.has_permissions(administrator=True)
async def statschannels(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)

    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {}

    if guild_id not in config_data:
        config_data[guild_id] = {
            'sc_totalmembers_id': '`❌`',
            'sc_totalmembers_channel_content': '`❌`',
            'sc_membersnotbot_id': '`❌`',
            'sc_membersnotbot_content': '`❌`',
            'sc_numberboost_id': '`❌`',
            'sc_numberboost_channel_content': '`❌`',
        }

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    guild_config = config_data.get(guild_id, {})
    totalmember_id = guild_config.get("sc_totalmembers_id")
    status_option = f'`❌`' if totalmember_id != "❌" else "`❌`"

    bots_id = guild_config.get("sc_membersnotbot_id")
    status_bots = f'`❌`' if bots_id != "❌" else "`❌`"

    boosts_id = guild_config.get("sc_numberboost_id")
    status_boosts = f'`❌`' if boosts_id != "❌" else "`❌`"

    status = guild_config.get("statschannel_status", '<:Danger:1296505953155416132>')

    embed = discord.Embed(
        title = '\📌 Configuration » \⭐ Salons de Statistiques.',
        description = f'''> • **Status** : {status}
                      > • **Total de Membres** : `{status_option}`
                      > • **Nombre de Bots** : `{status_bots}`
                      > • **Nombre de Boost** : `{status_boosts}`''',
        color = 0X151976)

    await interaction.response.send_message(embed=embed, view=StatsChannelsView(), ephemeral=True)

class StatsChannelsView(discord.ui.View):
    @discord.ui.select(
        placeholder="Choisissez une option...",
        custom_id="select_stats_channel_option",
        options=[
            SelectOption(label="Total de Membres", value="sc_totalmembers", description=f"""Ex : "🌱・Membres : 88" """,
                         emoji="<:XP:1189535112665251890>"),
            SelectOption(label="Membres (non bot)", value="sc_membersnotbot", description="Choisir le rôle à donner automatiquement.",
                         emoji="<:Flag:1189516434515185715>"),
            SelectOption(label="Nombre de boosts", value="sc_numberboost", description="Configurer le canal de logs.",
                         emoji="<:Configurations:1189630693609848934>"),
            SelectOption(label="Activer/ Désactiver", value="toggle", description="Activer ou désactiver le module...",
                         emoji="<:XP:1189535112665251890>")
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        if select.values[0] == "toggle":
            guild_config['statschannel_status'] = '<:DiscordStatusOnline:1184534287932989460>' if guild_config.get('statschannel_status') == '<:Danger:1296505953155416132>' else '<:Danger:1296505953155416132>'

            role_id = guild_config.get("soutien_role_id")
            role_mention = f'<@&{role_id}>' if role_id != "`❌`" else "`❌`"

            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            status = guild_config.get('statschannel_status', '<:Danger:1296505953155416132>')
            condition = guild_config.get('soutien_condition', 'non définie')
            embed = discord.Embed(
                title='\📌 Configuration » \⭐ Biographie de soutien.',
                description=f'''> • **Status** : {status}
                              > • **Condition** : `{condition}`
                              > • **Rôle automatiquement donné** : {role_mention}''',
                color=0X151976)
            await interaction.response.edit_message(embed=embed, view=self)

class SelectChannelModal(discord.ui.Modal, title = "ID Salon"):
    def __init__(self, option_value, guild_id, config_data):
        super().__init__()

        self.option_value = option_value
        self.guild_id = guild_id
        self.config_data = config_data

        self.channel_id = None
        self.content_modal = None

    salon_id = discord.ui.TextInput(
        label="ID du salon",
        style=discord.TextStyle.short,
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=32,
    )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Entrez l'ID du salon vocal :", view=TextInputModal(self.guild_id, self.option_value, self.config_data))

class TextInputModal(discord.ui.Modal):
    channel_id = discord.ui.TextInput(
        label="ID du salon vocal",
        style=discord.TextStyle.short,
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=32,
    )

    async def callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        existing_content = guild_config.get(f'{self.option_value}_channel_content', '`❌`')
        existing_channel = guild_config.get(f'{self.option_value}_id', '`❌`')

        if guild_id not in config_data:
            config_data[guild_id] = {
                f'{self.option_value}_id': '`❌`',
                f'{self.option_value}_channel_content': '`❌`',
            }

        config_data[guild_id][f'{self.option_value}_id'] = self.channel_id.value

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        content_modal = content_modal = discord.ui.TextInput(
            label="Contenu du salon vocal",
            style=discord.TextStyle.short,
            placeholder=f"Ex: {existing_content}",
            required=True,
            max_length=64,
        )

        await interaction.response.send_message("Entrez le contenu du salon vocal :", view=TextContentModal(self.option_value, guild_id, config_data))

class TextContentModal(discord.ui.Modal):
    content = discord.ui.TextInput(
        label="Contenu du salon vocal",
        style=discord.TextStyle.short,
        placeholder="Ex: {content}",
        required=True,
        max_length=64,
    )

    async def callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        existing_channel = guild_config.get(f'{self.option_value}_id', '`❌`')

        if guild_id not in config_data:
            config_data[guild_id] = {
                f'{self.option_value}_id': '`❌`',
                f'{self.option_value}_channel_content': '`❌`',
            }

        config_data[guild_id][f'{self.option_value}_channel_content'] = self.content.value

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        await interaction.response.edit_message("Configuration enregistrée !", view=None)

# /AUTOROLE

@tree.command(name='autorole', description='Configurer le fait de donner un rôle automatiquement à un nouvel arrivant.')
@commands.has_permissions(administrator=True)
async def autorole(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)

    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {}

    # Ajoutez le serveur s'il n'est pas déjà présent dans le fichier JSON
    if guild_id not in config_data:
        config_data[guild_id] = {
            'autorole_logschannel_id': '`❌`',
            'autorole_role': '`❌`',
            'autorole_status': '`❌`'
        }

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    guild_config = config_data.get(guild_id, {})

    # Obtenez les valeurs actuelles
    logs_channel_id = guild_config.get("autorole_logschannel_id")

    role_id = guild_config.get("autorole_role")
    role_mention = f'`❌`' if role_id != f'<@&{role_id}>' else "`❌`"

    channel_id = guild_config.get("autorole_logschannel_id")
    logs_channel_id = f'`❌`' if channel_id != f'<#{channel_id}>' else "`❌`"

    status_id = guild_config.get("autorole_status")
    sstatus_id = status_id  # Conserver la valeur actuelle du statut

    autorole_role = guild_config.get("autorole_role")
    autorole_status = guild_config.get("autorole_status")

    embed = discord.Embed(
        title='\📌 Configuration » \⭐ Autorôle.',
        description=f'''> • **Status** : {status_id}
                      > • **Logs Channel** : {logs_channel_id}
                      > • **Rôle Autorôle** : {role_mention}''',
        color=0x151976)

    await interaction.response.send_message(embed=embed, view=select_autorole_option(), ephemeral=True)

class select_autorole_option(discord.ui.View):

    @discord.ui.select(
        placeholder="Configurer le module...",
        custom_id="select_autorole_option",
        options=[
            SelectOption(label="Activer/ Désactiver", value="toggle", description="Activer ou désactiver le module...",
                         emoji="<:XP:1189535112665251890>"),
            SelectOption(label="Rôle à donner", value="role", description="Choisir le rôle à donner automatiquement.",
                         emoji="<:Flag:1189516434515185715>"),
            SelectOption(label="Logs", value="logs", description="Configurer le canal de logs.",
                         emoji="<:Configurations:1189630693609848934>")
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        if select.values[0] == "toggle":
            # Inverse le statut actuel
            current_status = guild_config.get("autorole_status", "❌")
            new_status = '<:DiscordStatusOnline:1184534287932989460>' if current_status == '<:Danger:1296505953155416132>' else '<:Danger:1296505953155416132>'
            
            # Met à jour le statut dans le fichier JSON
            config_data[guild_id]['autorole_status'] = new_status

            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            await interaction.response.send_message(f"Le module est activé ! {new_status}", ephemeral=True)

        elif select.values[0] == "role":
            await interaction.response.send_modal(modal_autorole_role())
        elif select.values[0] == "logs":
            await interaction.response.send_modal(modal_logs_channel())

class modal_autorole_role(discord.ui.Modal, title="🔧 Configuration du Rôle Autorôle"):

    role_id = discord.ui.TextInput(
        label="ID du rôle à donner automatiquement",
        style=discord.TextStyle.short,
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=32,
    )

    async def callback(self, interaction: discord.Interaction):
        pass

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        existing_logs_channel = guild_config.get('autorole_logschannel_id', 'Logs Undefined')
        existing_status = guild_config.get('autorole_status', 'Status Undefined')

        if guild_id not in config_data:
            config_data[guild_id] = {
                'autorole_status': existing_status,
                'autorole_logschannel_id': existing_logs_channel,
                'autorole_role': 'Role Undefined',
            }

        guild_config = config_data[guild_id]

        config_data[guild_id]['autorole_status'] = existing_status
        config_data[guild_id]['autorole_logschannel_id'] = existing_logs_channel
        config_data[guild_id]['autorole_role'] = self.role_id.value

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        role_mention = f'<@&{self.role_id.value}>'
        embed = discord.Embed(
            title='\📌 Configuration » \⭐ Autorôle.',
            description=f'''> • **Status** : {existing_status}
                          > • **Logs Channel** : {existing_logs_channel}
                          > • **Rôle Autorôle** : {role_mention}''',
            color=0X151976,
        )

        await interaction.response.edit_message(embed=embed, view=select_autorole_option())

class modal_logs_channel(discord.ui.Modal, title="📝 Salon de Logs."):

    logs_channel_id = discord.ui.TextInput(
        label="ID du canal de logs pour l'autorôle",
        style=discord.TextStyle.short,
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=32,
    )

    async def callback(self, interaction: discord.Interaction):
        pass

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        existing_role = guild_config.get('autorole_role')
        existing_status = guild_config.get('autorole_status')

        if guild_id not in config_data:
            config_data[guild_id] = {
                'autorole_status': existing_status,
                'autorole_logschannel_id': 'Logs Undefined',
                'autorole_role': existing_role,
            }

        config_data[guild_id]['autorole_status'] = existing_status
        config_data[guild_id]['autorole_logschannel_id'] = self.logs_channel_id.value
        config_data[guild_id]['autorole_role'] = existing_role

        guild_config = config_data[guild_id]

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        role_mention = f'<@&{existing_role}>'
        embed = discord.Embed(
            title='\📌 Configuration » \⭐ Autorôle.',
            description=f'''> • **Status** : {existing_status}
                          > • **Logs Channel** : <#{self.logs_channel_id.value}>
                          > • **Rôle Autorôle** : {role_mention}''',
            color=0X151976,
        )

        await interaction.response.edit_message(embed=embed, view=select_autorole_option())

# /SOUTIEN

async def update_roles():
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {}

    for guild in bot.guilds:
        guild_id = str(guild.id)
        guild_config = config_data.get(guild_id, {})

        role_id = guild_config.get("soutien_role_id")
        role = None
        if role_id and role_id != "`\u274c`":
            role = guild.get_role(int(role_id))

        if role:
            condition = guild_config.get('soutien_condition', 'non définie').lower()
            for member in guild.members:
                bio_found = False
                for activity in member.activities:
                    if isinstance(activity, discord.CustomActivity) and condition.lower() in activity.name.lower():
                        bio_found = True
                        break

                if bio_found:
                    await member.add_roles(role, reason="Condition de soutien remplie")
                else:
                    await member.remove_roles(role, reason="Condition de soutien non remplie")

@tasks.loop(seconds=10)
async def update_roles_loop():
    await bot.wait_until_ready()
    await update_roles()

@tree.command(name='soutien', description='Donner un rôle automatiquement en fonction d\'une bio.')
@commands.has_permissions(administrator=True)
async def soutien(interaction: discord.Interaction):
    guild_id = str(interaction.guild.id)

    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        config_data = {}

    if guild_id not in config_data:
        config_data[guild_id] = {
            'soutien_status': '<:Danger:1296505953155416132>',
            'soutien_condition': '`❌`',
            'soutien_role_id': '`❌`'
        }

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

    guild_config = config_data.get(guild_id, {})

    role_id = guild_config.get("soutien_role_id")
    role_mention = '`❌`' if role_id == '`\u274c`' else f'<@&{role_id}>'

    embed = discord.Embed(
        title='\📌 Configuration » \⭐ Biographie de soutien.',
        description=f'''> • **Status** : {guild_config.get('soutien_status', '<:Danger:1296505953155416132>')}
                      > • **Condition** : `{guild_config.get('soutien_condition', '`❌`')}`
                      > • **Rôle automatiquement donné** : {role_mention}''',
        color=0x151976)

    await interaction.response.send_message(embed=embed, view=select_soutien_option(), ephemeral=True)

class modal_soutien(discord.ui.Modal, title="📌 Condition"):
    condition = discord.ui.TextInput(
        label="Contenu de la bio",
        style=discord.TextStyle.short,
        placeholder="Ex: .gg/noodle-support",
        required=True,
        max_length=64,
    )

    async def callback(self, interaction: discord.Interaction):
        pass

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        new_condition = self.condition.value if self.condition.value != "❌" else 'non définie'
        config_data[guild_id]['soutien_condition'] = new_condition

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        print(f"Condition updated: {new_condition}")

        role_id = guild_config.get("soutien_role_id")
        role_mention = '`❌`' if role_id == '`❌`' else f'<@&{role_id}>'

        embed = discord.Embed(
            title='\📌 Configuration » \⭐ Biographie de soutien.',
            description=f'''> • **Status** : {guild_config.get('soutien_status', '<:Danger:1296505953155416132>')}
                          > • **Condition** : `{new_condition}`
                          > • **Rôle automatiquement donné** : {role_mention}''',
            color=0X151976)

        await interaction.response.edit_message(embed=embed, view=select_soutien_option())

class modal_role_id(discord.ui.Modal, title="🔧 Configuration du Rôle"):
    role_id = discord.ui.TextInput(
        label="ID du rôle",
        style=discord.TextStyle.short,
        placeholder="Ex: 123456789012345678",
        required=True,
        max_length=32,
    )

    async def callback(self, interaction: discord.Interaction):
        pass

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        existing_condition = guild_config.get('soutien_condition', '`❌`')
        existing_status = guild_config.get('soutien_status', '<:Danger:1296505953155416132>')

        if guild_id not in config_data:
            config_data[guild_id] = {
                'soutien_status': existing_status,
                'soutien_condition': existing_condition,
                'soutien_role_id': '`❌`',
            }

        config_data[guild_id]['soutien_condition'] = existing_condition
        config_data[guild_id]['soutien_role_id'] = self.role_id.value

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        role_mention = '`❌`' if self.role_id.value == '`❌`' else f'<@&{self.role_id.value}>'
        embed = discord.Embed(
            title='\📌 Configuration » \⭐ Biographie de soutien.',
            description=f'''> • **Status** : {existing_status}
                          > • **Condition** : `{existing_condition}`
                          > • **Rôle automatiquement donné** : {role_mention}''',
            color=0X151976,
        )

        await interaction.response.edit_message(embed=embed, view=select_soutien_option())

class select_soutien_option(discord.ui.View):
    @discord.ui.select(
        placeholder="Configurer le module...",
        custom_id="select_soutien_option",
        options=[
            SelectOption(label="Status", value="status", description="Activer ou désactiver le module...",
                         emoji="<:XP:1189535112665251890>"),
            SelectOption(label="Condition", value="condition", description="Créer une condition pour donner le rôle.",
                         emoji="<:OneWaySign:1189511733765750865>"),
            SelectOption(label="Rôle", value="rôle", description="Choisir un rôle à donner.",
                         emoji="<:Flag:1189516434515185715>")
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild_id = str(interaction.guild.id)

        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = {}

        guild_config = config_data.get(guild_id, {})

        status_active = guild_config.get("soutien_status", "") == '<:DiscordStatusOnline:1184534287932989460>'
        role_id = guild_config.get("soutien_role_id")
        role_mention = '`❌`' if role_id == '`❌`' else f'<@&{role_id}>'

        if select.values[0] == "status":
            status_active = not status_active
            guild_config['soutien_status'] = '<:DiscordStatusOnline:1184534287932989460>' if status_active else '<:Danger:1296505953155416132>'

            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            print(f"Status updated: {guild_config['soutien_status']}")

            condition = guild_config.get('soutien_condition', '\u274c')
            embed = discord.Embed(
                title='\📌 Configuration » \⭐ Biographie de soutien.',
                description=f'''> • **Status** : {guild_config.get('soutien_status', '<:Danger:1296505953155416132>')}
                              > • **Condition** : `{condition}`
                              > • **Rôle automatiquement donné** : {role_mention}''',
                color=0X151976)
            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "rôle":
            await interaction.response.send_modal(modal_role_id())

        elif select.values[0] == "condition":
            await interaction.response.send_modal(modal_soutien())


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     CONFIGURATIONS COMMANDS                                                                            #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     ADMINISTRATION COMMANDS                                                                            #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
@tree.command(name = 'adminping', description = 'Voir tous les ping concernant Noodle (Site, VPS...).')
async def adminping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True)

@tree.command(name = 'uptime', description = 'Affiche le temps de fonctionnement de Noodle.')
async def uptime(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'guildslist', description = 'Envoi la liste des serveurs sur lequel est NoodleBot.')
async def guildslist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name = 'adminlog', description = 'Voir les dernières actions faites avec le bot.')
async def adminlog(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    await interaction.response.send_message(f'Commande non disponible.', ephemeral = True) 

@tree.command(name='adminconfig', description='Configurer les options administratives du bot.')
@discord.app_commands.checks.has_role(PERM_ADMIN_ID)
async def admin_config(interaction: discord.Interaction):

    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        config_data = {}

    for guild in bot.guilds:
        guild_id = str(guild.id)

        if guild_id not in config_data:
            config_data[guild_id] = {
                'security_capchat_status': '<:Danger:1296505953155416132>',
                'security_capchat_channel_id': '`\u274c`',
                'security_capchat_logschannel_id': '`\u274c`',
                
                'ia_status': '<:Danger:1296505953155416132>',
                'ia_channel': '`\u274c`',
                'ia_logschannel_id': '`\u274c`',
                
                'm_welcome_status': '<:Danger:1296505953155416132>',
                'm_welcome_content': '`\u274c`',
                'm_welcome_channel_id': '`\u274c`',
                
                'm_goodbye_status': '<:Danger:1296505953155416132>',
                'm_goodbye_content': '`\u274c`',
                'm_goodbye_channel_id': '`\u274c`',
                
                'statschannel_status': '<:Danger:1296505953155416132>',
                'sc_totalmembers_id': '`\u274c`',
                'sc_totalmembers_channel_content': '`\u274c`',
                'sc_membersnotbot_id': '`\u274c`',
                'sc_membersnotbot_content': '`\u274c`',
                'sc_numberboost_id': '`\u274c`',
                'sc_numberboost_channel_content': '`\u274c`',
                
                'autorole_logschannel_id': '`\u274c`',
                'autorole_role': '`\u274c`',
                'autorole_status': '<:Danger:1296505953155416132>',
                
                'soutien_status': '<:Danger:1296505953155416132>',
                'soutien_condition': '`\u274c`',
                'soutien_role_id': '`\u274c`',
                'soutien_permission_warning_sent': False
            }

    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

    await interaction.response.send_message('Options administratives configurées pour tous les serveurs.', ephemeral=True)

@tree.command(name='adminview', description='Voir les options administratives configurées pour ce serveur.')
@discord.app_commands.checks.has_role(PERM_ADMIN_ID)
async def admin_view(interaction: discord.Interaction):
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        await interaction.response.send_message("Le fichier de configuration n'a pas été trouvé.", ephemeral=True)
        return
    except json.decoder.JSONDecodeError:
        await interaction.response.send_message("Erreur lors de la lecture du fichier de configuration.", ephemeral=True)
        return

    guild_id = str(interaction.guild.id)

    if guild_id not in config_data:
        await interaction.response.send_message("Aucune configuration trouvée pour ce serveur.", ephemeral=True)
        return

    guild_config = config_data[guild_id]

    config_message = f"**Configuration pour le serveur {interaction.guild.name}**\n\n"
    config_message += f"**Sécurité**\n"
    config_message += f"- Statut CAPTCHA: {guild_config['security_capchat_status']}\n"
    config_message += f"- Canal CAPTCHA: {guild_config['security_capchat_channel_id']}\n"
    config_message += f"- Canal Logs CAPTCHA: {guild_config['security_capchat_logschannel_id']}\n\n"

    config_message += f"**Intelligence Artificielle**\n"
    config_message += f"- Statut IA: {guild_config['ia_status']}\n"
    config_message += f"- Canal IA: {guild_config['ia_channel']}\n"
    config_message += f"- Canal Logs IA: {guild_config['ia_logschannel_id']}\n\n"

    config_message += f"**Messages de Bienvenue et d'Adieu**\n"
    config_message += f"- Statut Bienvenue: {guild_config['m_welcome_status']}\n"
    config_message += f"- Message de Bienvenue: {guild_config['m_welcome_content']}\n"
    config_message += f"- Canal Bienvenue: {guild_config['m_welcome_channel_id']}\n"
    config_message += f"- Statut Adieu: {guild_config['m_goodbye_status']}\n"
    config_message += f"- Message d'Adieu: {guild_config['m_goodbye_content']}\n"
    config_message += f"- Canal Adieu: {guild_config['m_goodbye_channel_id']}\n\n"

    config_message += f"**Statistiques du Serveur**\n"
    config_message += f"- Statut Canal Statistiques: {guild_config['statschannel_status']}\n"
    config_message += f"- Canal Membres Totaux: {guild_config['sc_totalmembers_id']}\n"
    config_message += f"- Contenu Membres Totaux: {guild_config['sc_totalmembers_channel_content']}\n"
    config_message += f"- Canal Membres Non-Bots: {guild_config['sc_membersnotbot_id']}\n"
    config_message += f"- Contenu Membres Non-Bots: {guild_config['sc_membersnotbot_content']}\n"
    config_message += f"- Canal Nombre Boost: {guild_config['sc_numberboost_id']}\n"
    config_message += f"- Contenu Nombre Boost: {guild_config['sc_numberboost_channel_content']}\n\n"

    config_message += f"**Auto-Role**\n"
    config_message += f"- Canal Logs Auto-Role: {guild_config['autorole_logschannel_id']}\n"
    config_message += f"- Rôle Auto-Role: {guild_config['autorole_role']}\n"
    config_message += f"- Statut Auto-Role: {guild_config['autorole_status']}\n\n"

    config_message += f"**Soutien**\n"
    config_message += f"- Statut Soutien: {guild_config['soutien_status']}\n"
    config_message += f"- Condition Soutien: {guild_config['soutien_condition']}\n"
    config_message += f"- Rôle Soutien: {guild_config['soutien_role_id']}\n"
    config_message += f"- Avertissement Permission Envoyé: {guild_config['soutien_permission_warning_sent']}\n"

    await interaction.response.send_message(config_message, ephemeral=True)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     ADMINISTRATION COMMANDS                                                                            #
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CONFIG_FILE = "./config.json"
DATA_FILE = "./data.json"

with open('./config.json', 'r') as f:
    config = json.load(f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

config = load_config()
LOG_CHANNEL_ID = 1298665863632650240

def format_coins(amount):
    return f"{amount:,}".replace(",", " ")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

user_data = load_data()

async def log_message(interaction, message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log_channel.send(f"{message}")

@tree.command(name='coins', description='Voir tous les 🪙 d\'un joueur.')
async def coins(interaction: discord.Interaction, membre: discord.Member = None):
    membre = membre or interaction.user
    user_id = str(membre.id)
    coins = user_data.get(user_id, {}).get('coins', 0)
    bank_coins = user_data.get(user_id, {}).get('bank', 0)
    grade = user_data.get(user_id, {}).get('grade', 'Joueur')
    taux_interet = config['banque']['taux_interet_par_grade'].get(grade, 0.01)

    montant_apres_interet = bank_coins * (1 + taux_interet)
    embed = discord.Embed(
        title=f"Compte de {membre.display_name}",
        description=f"**Taux d'intérêt** : `{taux_interet*100}%` par jour",
        color=0xFD8B46)
    embed.add_field(name="🏦 En banque", value=f"**{format_coins(bank_coins)}** {config['nom_monnaie']}", inline=False)
    embed.add_field(name="💸 Disponible", value=f"**{format_coins(coins)}** {config['nom_monnaie']}", inline=False)
    embed.add_field(name="📈 Après Intérêts", value=f"**{format_coins(int(montant_apres_interet))}** {config['nom_monnaie']} (J+1)", inline=False)
    embed.set_thumbnail(url=membre.avatar.url)
    embed.set_footer(text=f"Demande par {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)
    await log_message(interaction, f"`[ /COINS ]` {membre.name} a consulté ses {config['nom_monnaie']}.")

@tree.command(name='place', description='Commande pour placer des 🪙 à la banque.')
async def place(interaction: discord.Interaction, montant: int):
    user_id = str(interaction.user.id)
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'bank': 0, 'grade': 'Joueur'}

    if montant > user_data[user_id]['coins']:
        await interaction.response.send_message("Vous n'avez pas assez de 🪙.")
    else:
        user_data[user_id]['coins'] -= montant
        user_data[user_id]['bank'] += montant
        save_data(user_data)
        await interaction.response.send_message(f"Vous avez placé {format_coins(montant)} {config['nom_monnaie']} à la banque.")
        await log_message(interaction, f"`[ /BANKPLACE ]` {interaction.user.name} a placé `{montant}` {config['nom_monnaie']} à la banque.")

@tree.command(name='daily', description='Recevez une récompense quotidienne.')
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    current_time = int(time.time())
    last_reward = user_data.get(user_id, {}).get('last_daily', 0)
    cooldown = config['methodes_gain']['recompense_quotidienne']['cooldown_heures'] * 3600

    if current_time - last_reward < cooldown:
        await interaction.response.send_message("Vous avez déjà réclamé votre récompense quotidienne.")
        return

    montant = config['methodes_gain']['recompense_quotidienne']['montant']
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'bank': 0, 'grade': 'Joueur', 'last_daily': 0}

    user_data[user_id]['coins'] += montant
    user_data[user_id]['last_daily'] = current_time
    save_data(user_data)

    await interaction.response.send_message(f"Vous avez reçu {format_coins(montant)} {config['nom_monnaie']} pour votre connexion quotidienne.")
    await log_message(interaction, f"`[ /DAILY ]` {interaction.user.name} a reçu sa récompense quotidienne.")

@tree.command(name='blackjack', description='Jouez une partie de blackjack.')
async def blackjack(interaction: discord.Interaction, mise: int):
    if mise < config['methodes_gain']['blackjack']['mise_min'] or mise > config['methodes_gain']['blackjack']['mise_max']:
        await interaction.response.send_message(f"La mise doit être entre {config['methodes_gain']['blackjack']['mise_min']} et {config['methodes_gain']['blackjack']['mise_max']}.")
        return

    user_id = str(interaction.user.id)
    if user_id not in user_data or user_data[user_id]['coins'] < mise:
        await interaction.response.send_message("Vous n'avez pas assez de 🪙 pour jouer.")
        return

    bot_score = random.randint(17, 21)
    user_score = random.randint(17, 21)

    embed = discord.Embed(title="Résultat de la Partie de Blackjack", color=discord.Color.blue())
    embed.add_field(name="Mise", value=f"{format_coins(mise)} {config['nom_monnaie']}", inline=False)
    embed.add_field(name="Score de l'Utilisateur", value=str(user_score), inline=False)
    embed.add_field(name="Score du Bot", value=str(bot_score), inline=False)

    if user_score > 21:
        perte = mise
        user_data[user_id]['coins'] -= perte
        message = f"Vous avez dépassé 21 avec un score de {user_score}. Vous avez perdu {format_coins(perte)} {config['nom_monnaie']}."
        embed.add_field(name="Perte", value=f"{format_coins(perte)} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Solde Restant", value=f"{format_coins(user_data[user_id]['coins'])} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Status", value=f"```diff\n- Le 🪙 Win !```", inline=False)

    elif bot_score > 21:
        gain = mise * config['methodes_gain']['blackjack']['multiplicateur_gagner']
        user_data[user_id]['coins'] += gain
        message = f"Le bot a dépassé 21 avec un score de {bot_score}. Vous avez gagné {format_coins(gain)} {config['nom_monnaie']}!"
        embed.add_field(name="Gain", value=f"{format_coins(gain)} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Solde Actuel", value=f"{format_coins(user_data[user_id]['coins'])} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Status", value=f"```diff\n+ {interaction.user.name} Win !```", inline=False)

    elif user_score > bot_score:
        gain = mise * config['methodes_gain']['blackjack']['multiplicateur_gagner']
        user_data[user_id]['coins'] += gain
        message = f"Vous avez gagné contre le bot ! Votre score est de {user_score} et le score du bot est {bot_score}. Vous avez gagné {format_coins(gain)} {config['nom_monnaie']}!"
        embed.add_field(name="Gain", value=f"{format_coins(gain)} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Solde Actuel", value=f"{format_coins(user_data[user_id]['coins'])} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Status", value=f"```diff\n+ {interaction.user.name} Win !```", inline=False)

    elif user_score < bot_score:
        perte = mise
        user_data[user_id]['coins'] -= perte
        message = f"Le bot a gagné cette fois-ci avec un score de {bot_score} contre votre score de {user_score}. Vous avez perdu {format_coins(perte)} {config['nom_monnaie']}."
        embed.add_field(name="Perte", value=f"{format_coins(perte)} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Solde Restant", value=f"{format_coins(user_data[user_id]['coins'])} {config['nom_monnaie']}", inline=False)
        embed.add_field(name="Status", value=f"```diff\n- Le Kasino a Win !```", inline=False)

    else:
        message = f"Égalité ! Votre score est de {user_score} et le score du bot est {bot_score}. Vous ne perdez rien."
        embed.add_field(name="Status", value=f"```diff\n= Égalité !```", inline=False)

    await interaction.response.send_message(message)

    log_channel = interaction.guild.get_channel(1298665863632650240)
    await log_channel.send(embed=embed)

    save_data(user_data)
    await log_message(interaction, f"`[ /BLACKJACK ]` {interaction.user.name} a joué au blackjack avec une mise de {format_coins(mise)} {config['nom_monnaie']}. Le bot a obtenu un score de {bot_score} et l'utilisateur a obtenu un score de {user_score}.")

channel_id = 1298665863632650240

@tasks.loop(hours=24)
async def appliquer_interets():
    channel = bot.get_channel(1299050389865500734)

    for user_id, data in user_data.items():
        grade = data.get('grade', 'Joueur')
        taux_interet = config['banque']['taux_interet_par_grade'].get(grade, 0.01)

        if 'bank' in data:
            old_balance = data['bank']
            if old_balance > 0:
                int_interest = round(old_balance * taux_interet)
                new_balance = old_balance + int_interest
                data['bank'] = new_balance

                embed = discord.Embed(title="Intérêts Appliqués", color=0xFD8B46)
                embed.add_field(name="\🔗 Utilisateur ID", value=f'''```\n{user_id}\n```''', inline=False)
                embed.add_field(name="\💸 Solde avant intérêts", value=f'''```\n{format_coins(old_balance)}\n```''', inline=False)
                embed.add_field(name="\🏦 Solde après intérêts", value=f'''```\n{format_coins(new_balance)}\n```''', inline=False)

                await channel.send(embed=embed)
    save_data(user_data)

@tree.command(name='withdraw', description='Retirer un montant de 🪙 de la banque.')
async def withdraw(interaction: discord.Interaction, montant: int):
    user_id = str(interaction.user.id)

    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'bank': 0, 'grade': 'Joueur'}
    
    if montant > user_data[user_id]['bank']:
        await interaction.response.send_message("Vous n'avez pas assez de 🪙 dans votre banque.")
    else:
        user_data[user_id]['bank'] -= montant
        user_data[user_id]['coins'] += montant
        save_data(user_data)
        await interaction.response.send_message(f"Vous avez retiré {montant} {config['nom_monnaie']} de la banque.")
        await log_message(interaction, f"[ /WITHDRAW ] **{interaction.user.name}** a retiré {montant} {config['nom_monnaie']} de la banque.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = str(message.author.id)
    
    # Log pour vérifier si le message est bien capté
    print(f"Message reçu de {message.author.name} ({user_id}): {message.content}")

    # Vérification que l'utilisateur est dans user_data
    if user_id not in user_data:
        user_data[user_id] = {'coins': 0, 'bank': 0, 'grade': 'Joueur'}
        print(f"Nouvel utilisateur ajouté : {message.author.name}")

    # Log pour vérifier les montants
    montant_par_message = config['methodes_gain']['recompense_message']['montant_par_message']
    print(f"Montant par message : {montant_par_message}")
    
    # Ajout des gains
    user_data[user_id]['coins'] += montant_par_message
    print(f"Nouvelle balance pour {message.author.name}: {user_data[user_id]['coins']} {config['nom_monnaie']}")
    
    # Essai de sauvegarder les données, log en cas d'erreur
    try:
        await save_data(user_data)  # Vérifiez bien que save_data est asynchrone
        print(f"Données sauvegardées pour {message.author.name}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")

    # Essai de log le message
    try:
        await log_message(message, f"{message.author.name} a gagné {montant_par_message} {config['nom_monnaie']} pour avoir envoyé un message.")
        print(f"Log envoyé pour {message.author.name}")
    except Exception as e:
        print(f"Erreur lors du log : {e}")

fruit_emojis = ['🍎', '🍌', '🍒', '🍇', '🍉', '🍊', '🍋', '🍍', '🥭', '🥝']

def generate_combinations():
    all_combinations = [([fruit] * 3) for fruit in fruit_emojis]
    num_winning_combinations = int(100 * 0.45)
    num_non_winning_combinations = 100 - num_winning_combinations

    non_winning_combinations = [
        [random.choice(fruit_emojis), random.choice(fruit_emojis), random.choice(fruit_emojis)]
        for _ in range(num_non_winning_combinations)
    ]

    combinations = all_combinations * int(num_winning_combinations / len(all_combinations)) + non_winning_combinations
    random.shuffle(combinations)

    return combinations

combinations = generate_combinations()

def spin_roulette():
    return random.choice(combinations)

def determine_result(spin):
    return len(set(spin)) == 1

def read_bank_data():
    with open('./data.json', 'r') as f:
        return json.load(f)

def write_bank_data(data):
    with open('./data.json', 'w') as f:
        json.dump(data, f, indent=4)

@tree.command(name="roulette", description="Jouer à la 🪙 !")
async def roulette(interaction: discord.Interaction, mise: int):
    data = read_bank_data()
    user_id = str(interaction.user.id)

    if user_id not in data:
        await interaction.response.send_message("Votre compte est introuvable. Veuillez contacter un administrateur.")
        return

    user_data = data[user_id]

    if mise < 50000:
        await interaction.response.send_message("La mise minimale est de 50 000.")
        return

    if user_data['coins'] < mise:
        await interaction.response.send_message(f"Vous n'avez pas assez d'argent. Votre solde actuel est de {user_data['bank']} coins.")
        return

    user_data['coins'] -= mise

    spin = spin_roulette()
    result = determine_result(spin)

    if result:
        winnings = mise + (mise * 5.5)
        user_data['coins'] += winnings
        await interaction.response.send_message(f'🎉 Vous avez gagné ! Voici votre tirage : {" ".join(spin)}. Vous recevez {winnings} coins !')
    else:
        await interaction.response.send_message(f'😢 Vous avez perdu ! Voici votre tirage : {" ".join(spin)}. Vous perdez la totalité de votre mise de départ !')

    write_bank_data(data)










PLAYER_TOKENS = {
    '1': '❌',  # Joueur 1
    '2': '⭕'   # Joueur 2
}

# Fichier où les stats seront enregistrées
STATS_FILE = './morpion_stats.json'

# Charger ou créer un fichier JSON pour les statistiques
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Sauvegarder les stats dans le fichier JSON
def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

# Mettre à jour les statistiques pour un joueur
def update_stats(winner_id, loser_id):
    stats = load_stats()

    # Initialiser les stats si nécessaire
    if winner_id not in stats:
        stats[winner_id] = {'wins': 0, 'losses': 0}
    if loser_id not in stats:
        stats[loser_id] = {'wins': 0, 'losses': 0}

    # Mettre à jour les stats
    stats[winner_id]['wins'] += 1
    stats[loser_id]['losses'] += 1

    # Sauvegarder les modifications
    save_stats(stats)

# Calculer le ratio win/defeat
def calculate_ratio(stats):
    wins = stats['wins']
    losses = stats['losses']
    if losses == 0:
        return float('inf') if wins > 0 else 0
    return wins / losses

# Classe du jeu Morpion
class Morpion(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=None)
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.board = ['⬜️'] * 9  # Plateau de morpion 3x3
        self.game_over = False

        # Ajouter des boutons pour chaque case
        for i in range(9):
            self.add_item(MorpionButton(i))

    # Fonction pour afficher le plateau
    def display_board(self):
        return f"{self.board[0]}{self.board[1]}{self.board[2]}\n" \
               f"{self.board[3]}{self.board[4]}{self.board[5]}\n" \
               f"{self.board[6]}{self.board[7]}{self.board[8]}"

    # Changer de joueur
    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    # Vérifier si un joueur a gagné
    def check_win(self, token):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        return any(all(self.board[pos] == token for pos in condition) for condition in win_conditions)

    # Vérifier s'il y a égalité
    def check_draw(self):
        return all(spot != '⬜️' for spot in self.board)

    # Terminer la partie
    async def end_game(self, interaction, winner=None):
        self.game_over = True
        self.clear_items()  # Désactiver les boutons

        if winner:
            loser = self.player1 if winner == self.player2 else self.player2
            update_stats(str(winner.id), str(loser.id))
            await interaction.response.edit_message(content=f'{winner.mention} a gagné la partie !\n\n{self.display_board()}', view=self)
        else:
            await interaction.response.edit_message(content=f'Partie terminée : égalité !\n\n{self.display_board()}', view=self)

# Boutons pour chaque case du Morpion
class MorpionButton(discord.ui.Button):
    def __init__(self, position):
        super().__init__(label='⬜️', style=discord.ButtonStyle.secondary, row=position // 3)
        self.position = position

    async def callback(self, interaction: discord.Interaction):
        view: Morpion = self.view
        if interaction.user != view.current_player:
            await interaction.response.send_message("Ce n'est pas votre tour.", ephemeral=True)
            return

        if view.game_over:
            await interaction.response.send_message("La partie est terminée.", ephemeral=True)
            return

        # Insérer le jeton dans la case sélectionnée
        token = PLAYER_TOKENS['1'] if view.current_player == view.player1 else PLAYER_TOKENS['2']
        if view.board[self.position] != '⬜️':
            await interaction.response.send_message("Cette case est déjà occupée.", ephemeral=True)
            return

        view.board[self.position] = token
        self.label = token
        self.disabled = True

        # Vérifier si le joueur a gagné
        if view.check_win(token):
            await view.end_game(interaction, view.current_player)
        # Vérifier s'il y a égalité
        elif view.check_draw():
            await view.end_game(interaction)
        else:
            view.switch_player()  # Passer au joueur suivant
            await interaction.response.edit_message(content=f"Tour de {view.current_player.mention} !\n\n{view.display_board()}", view=view)

# Commande pour lancer une partie de Morpion
@tree.command(name='morpion', description='Lancer une partie de Morpion.')
async def morpion(interaction: discord.Interaction, adversaire: discord.Member):
    author_member: discord.Member = interaction.user

    # Vérifier que l'auteur et l'adversaire ne sont pas les mêmes
    if author_member == adversaire:
        await interaction.response.send_message("Vous ne pouvez pas jouer contre vous-même.", ephemeral=True)
        return

    # Créer le jeu et envoyer le message initial
    view = Morpion(author_member, adversaire)
    await interaction.response.send_message(f"Partie de Morpion entre {author_member.mention} et {adversaire.mention} !\n\n{view.display_board()}", view=view)

def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

data = load_json_data('./data.json')
morpion_stats = load_json_data('./morpion_stats.json')
puissance4_stats = load_json_data('./puissance4_stats.json')

@tree.command(name="leaderboard", description="Affiche différents classements du bot.")
@app_commands.describe(category="Choisissez une catégorie de leaderboard à afficher")
@app_commands.choices(
    category=[
        app_commands.Choice(name="💰 ・ Classement des Richesses (coins)", value="1"),
        app_commands.Choice(name="🎯 ・ Morpion (statistiques)", value="2"),
        app_commands.Choice(name="🟡 ・ Puissance 4 (statistiques)", value="3"),
    ]
)
async def leaderboard(interaction: discord.Interaction, category: app_commands.Choice[str]):
    if category.value == "1":
        sorted_data = sorted(data.items(), key=lambda x: x[1]["bank"], reverse=True)
        leaderboard_message = "**💰 Classement des Richesses (Coins dans la banque) :**\n"
        for rank, (user_id, stats) in enumerate(sorted_data, start=1):
            leaderboard_message += f"**{rank}.** <@{user_id}> : {stats['bank']} coins\n"
    
    elif category.value == "2":
        # Afficher le leaderboard pour le Morpion
        sorted_morpion = sorted(morpion_stats.items(), key=lambda x: x[1]["wins"], reverse=True)
        leaderboard_message = "**🎯 Classement Morpion (Victoires) :**\n"
        for rank, (user_id, stats) in enumerate(sorted_morpion, start=1):
            leaderboard_message += f"**{rank}.** <@{user_id}> : {stats['wins']} victoires, {stats['losses']} défaites\n"
    
    elif category.value == "3":
        # Afficher le leaderboard pour Puissance 4
        sorted_puissance4 = sorted(puissance4_stats.items(), key=lambda x: x[1]["wins"], reverse=True)
        leaderboard_message = "**🔵 Classement Puissance 4 (Victoires) :**\n"
        for rank, (user_id, stats) in enumerate(sorted_puissance4, start=1):
            leaderboard_message += f"**{rank}.** <@{user_id}> : {stats['wins']} victoires, {stats['losses']} défaites\n"
    
    await interaction.response.send_message(leaderboard_message)


bot.run('MTAwMTk3MDUyODgzNzQzNTQwMw.G3Uv9I.vfSQ3gE1QkDjedGsC3qRj_Be0b63po19URTFKQ')