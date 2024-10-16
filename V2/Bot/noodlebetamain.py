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
from sympy import sympify, Symbol
import http.client

# ------------------------------------------
# CONFIGURATIONS ET INFORMATIONS GLOBALES
# ------------------------------------------

PERM_ADMIN_ID = 1183205593381601380

intents = discord.Intents.default()
#intents.presences = True
intents.members = True
intents.guilds = True


bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command('help')

def read_file(file):
    with open(file, "r") as f:
        return json.load(f)

def write_file(file, var):
    with open(file, 'w') as f:
        json.dump(var, f, indent = 2)


class client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents(members = True, guilds = True))
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        bio.start()
        stats_channels.start()

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

@tasks.loop(seconds=300)
async def stats_channels():
    await bot.wait_until_ready()
    unique_users = set()
    total_members = 0

    for guild in bot.guilds:
        total_members += guild.member_count
        for member in guild.members:
            unique_users.add(member.id)

    k_number = "{:.2f}k".format(total_members / 1000)

    users_voc_channel = bot.get_channel(1182347473314914405)
    guild_voc_channel = bot.get_channel(1182347501743910933)
    membres_voc_channel = bot.get_channel(1201952627437346936)

    await users_voc_channel.edit(name='🎉・Utilisateurs : ' + f'{k_number}')
    await guild_voc_channel.edit(name='🔮・Serveurs : ' + f'{len(bot.guilds)}')
    await membres_voc_channel.edit(name='🎉・Users Uniques : ' + f'{len(unique_users)}')

    await asyncio.sleep(300)

    
@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(1182414516940718130)
    
    embed = discord.Embed(description = f'''```diff
+ {guild.name} ・ {guild.member_count} Membres.
    Owner: {guild.owner.name} ({guild.owner.id})        
```''')

    await channel.send(f'<@947519926137143409>', embed = embed)

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(1182414516940718130)
    
    embed = discord.Embed(description = f'''```diff
- {guild.name} ・ {guild.member_count} Membres.
    Owner: {guild.owner.name} ({guild.owner.id})    
```''')

    await channel.send(f'<@947519926137143409>', embed = embed)
    
# ------------------------------------------
# description / bio
# ------------------------------------------

@tasks.loop(seconds=4)
async def bio():
    await bot.wait_until_ready()
    
    # Chemin d'accès au dossier sur MAC
    folder_path = '/home/container/'
    
    total_members = 0
    total_lines = 0
    
    excluded_dirs = ['.cache', '.local']
    
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    total_lines += len(file_content.readlines())
    
    for guild in bot.guilds:
        total_members += guild.member_count
    
    k_number = "{:.2f}k".format(total_members / 1000)
    
    formatted_total_lines = "{:,}".format(total_lines).replace(",", "'")

    status = [f'📜 {formatted_total_lines} Lignes 🔍', 'v0.5.3.1 ⭐ Beta', 'Developed with the 💖 by Sheikoo_']

    for i in status:
        await bot.change_presence(activity=discord.Game(str(i)))
        await asyncio.sleep(4)

# ------------------------------------------
# description / bio
# ------------------------------------------

@tree.command(name = 'serverinfo', description = 'Voir les informations du serveur.')
async def serverinfo(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    roles = [role for role in guild.roles[1:] if not role.managed][:20]
    member_count = sum(not member.bot for member in guild.members)
    members = guild.members
    bots = sum(member.bot for member in members)

    online_count = sum(member.status == discord.Status.online for member in guild.members)
    offline_count = sum(member.status == discord.Status.offline for member in guild.members)
    streaming_count = sum(any(activity.type == discord.ActivityType.streaming for activity in member.activities)
        for member in guild.members)
    dnd_count = sum(member.status == discord.Status.dnd for member in guild.members)


    all_members = guild.members

    normal_roles = set()
    integrated_roles = set()

    for member in all_members:
        if not member.bot:
            normal_roles.update(set(role.id for role in member.roles))
        else:
            integrated_roles.update(set(role.id for role in member.roles))

    everyone_role = guild.default_role
    integrated_roles.add(everyone_role.id)

    booster_role = guild.premium_subscriber_role
    if booster_role:
        integrated_roles.add(booster_role.id)

    boost_level = guild.boost_level if hasattr(guild, 'boost_level') else 0
    boost_count = guild.premium_subscription_count if hasattr(guild, 'premium_subscription_count') else 0

    booster_role = next((role for role in guild.roles if role.name.lower() == 'booster'), None)
    booster_role_name = booster_role.name if booster_role else '`Serveur jamais Boost`'

    boost_level = guild.boost_level if hasattr(guild, 'boost_level') else 0

    base_static_limit = 50
    base_animated_limit = 50
    base_sticker_limit = 10

    if boost_level >= 1:
        base_static_limit += 50
        base_animated_limit += 50
        base_sticker_limit += 10

    if boost_level >= 2:
        base_static_limit += 50
        base_animated_limit += 50
        base_sticker_limit += 15

    if boost_level >= 3:
        base_static_limit += 200
        base_animated_limit += 200
        base_sticker_limit += 60

    static_emojis = [emoji for emoji in guild.emojis if not emoji.animated]
    animated_emojis = [emoji for emoji in guild.emojis if emoji.animated]
    total_static_emojis = min(len(static_emojis), base_static_limit)
    total_animated_emojis = min(len(animated_emojis), base_animated_limit)
    total_emojis = total_static_emojis + total_animated_emojis
    total_stickers = min(len(guild.stickers) if guild.stickers else 0, base_sticker_limit)

    all_channels = guild.channels

    text_channels = [channel for channel in all_channels if isinstance(channel, discord.TextChannel)]
    voice_channels = [channel for channel in all_channels if isinstance(channel, discord.VoiceChannel)]
    stage_channels = [channel for channel in all_channels if isinstance(channel, discord.StageChannel)]
    category_channels = [channel for channel in all_channels if isinstance(channel, discord.CategoryChannel)]
    thread_channels = [channel for channel in all_channels if isinstance(channel, discord.Thread)]

    locked_text_channels = sum(1 for channel in text_channels if channel.overwrites_for(guild.default_role).read_messages is False)
    locked_voice_channels = sum(1 for channel in voice_channels if channel.overwrites_for(guild.default_role).connect is False)
    locked_stage_channels = sum(1 for channel in stage_channels if channel.overwrites_for(guild.default_role).connect is False)
    locked_category_channels = sum(1 for channel in category_channels if channel.overwrites_for(guild.default_role).read_messages is False)
    locked_thread_channels = sum(1 for channel in thread_channels if channel.overwrites_for(guild.default_role).read_messages is False)

    verification_level = guild.verification_level.name
    if verification_level == "none":
        verification_level = "Non Défini"

    afk_channel = guild.afk_channel
    if afk_channel is None:
        afk_channel = "Non Défini"


    afk_timeout = str(int(guild.afk_timeout / 60)) + " minutes"
    if guild.afk_timeout == "disabled":
        afk_timeout = "Non Défini."

    system_channel = guild.system_channel
    if system_channel is None:
        system_channel = "[`Communauté Désactivée`](https://support.discord.com/hc/fr/articles/360047132851-Activation-de-Votre-Serveur-Communautaire)"

    default_notifications = guild.default_notifications
    if default_notifications == discord.NotificationLevel.all_messages:
        default_notifications = 'Tous les messages'
    else:
        default_notifications = 'Mentions uniquement'

    explicit_content_filter = guild.explicit_content_filter
    if explicit_content_filter == discord.ContentFilter.disabled:
        explicit_content_filter = "Désactivé"

    rules_channel = guild.rules_channel
    if rules_channel is None:
        rules_channel = "Non Défini"
    else:
        rules_channel = f"<#{rules_channel.id}>"

    description = guild.description if guild.description is not None else "Aucune Description"

    embed = discord.Embed()
    embed.set_author(name = f'Informations du serveur {guild.name}', icon_url = guild.icon.url)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)

    embed.add_field(name = '<:Pint:1193577847529410580> À Propos', value = f'''**Nom du Serveur** : {guild.name}
**ID du Serveur** : `{guild.id}`
**Nom du Propriétaire** : [{guild.owner.name}](http://discord.com/users/{guild.owner.id})
**ID du Propriétaire** : `{guild.owner.id}`
**Mention** : {guild.owner.mention}
**Créé** : <t:{int(datetime.timestamp(guild.created_at))}:R>
**Membres** : `{member_count}`
**Bots** : `{bots}`''', inline = False)

    embed.add_field(name = '<:Server:1193578128883335309> Paramètres du Serveur', value = f'''**Niveau de Vérification** : {verification_level}
**Salon inactif** : {afk_channel.mention}
**Délai d'Inactivité** : {afk_timeout}
**Salon Messages Système** : {system_channel.mention}
**Notification par Défaut** : {default_notifications}
**Filtre de contenu Média Explicite** : `{explicit_content_filter}`
**Salon des Règles** : {rules_channel}
**Exigence 2FA** : [`Indisponible`](https://support.discord.com/hc/fr/articles/219576828-Mise-en-place-de-l-authentification-à-deux-facteurs)''', inline = False)

    embed.add_field(name = '<:Earth:1193652678291640410> Description du Serveur', value = description, inline = False)

    embed.add_field(name = '<:Emojis:1193654301558575245> Emojis & Stickers Info', value = f'''**Emojis statiques** : {total_static_emojis}/{base_static_limit}
**Emojis animés** : {total_animated_emojis}/{base_animated_limit}
**Total Emojis** : {total_emojis}/{base_static_limit + base_animated_limit}
**Total Stickers** : {total_stickers}/{base_sticker_limit}''', inline = False)

    embed.add_field(name = '<:DiscordBoost:1193657892868456480> État des Boosts', value = f'''**Niveau** : {boost_level}
**Nombre de boost** : {boost_count}
**Rôle "Booster"** : {booster_role_name}''', inline = False)

    embed.add_field(name = '<:Server:1193659497063915530> Salons', value = f'''**Total de Salons** : {len(all_channels)}
**Textuels** : {len(text_channels)} ({locked_text_channels} verrouillé)
**Vocal** : {len(voice_channels)} ({locked_voice_channels} verrouillé)
**Stage** : {len(stage_channels)} ({locked_stage_channels} verrouillé)
**Catégories** : {len(category_channels)} ({locked_category_channels} verrouillé)
**Fils** : {len(thread_channels)} ({locked_thread_channels} verrouillé)''', inline = False)

    embed.add_field(name = '<:DiscordMod:1193673354239033374> Rôles', value = f'''**Total** : {len(normal_roles) + len(integrated_roles)}
**Normal** : {len(normal_roles)}
**Intégrés** : {len(integrated_roles)}''', inline = False)

    embed.add_field(name = '<:Members:1193674114045591653> Membres', value = f'''**Total** : {guild.member_count}
**En Ligne** : {online_count}
**Ne Pas Déranger** : {dnd_count}
**Offline** : {offline_count}
**En Streaming** : {streaming_count}''', inline = False)

    view = discord.ui.View()
    button = discord.ui.Button(label = "Logo du Serveur", style = discord.ButtonStyle.secondary, custom_id = f"serveurinfo//icon")
    view.add_item(button)

    await interaction.response.send_message(embed = embed, view = view, ephemeral = False)

@bot.event
async def on_interaction(interaction):
    try:
        custom_id = interaction.data['custom_id']
    except KeyError:
        custom_id = " "

    # /serveurinfo
    if custom_id.split("//")[0] == "serveurinfo":
        guild = interaction.guild

        tableau = {
            "icon": guild.icon.url if guild.icon else None,
        }

        if custom_id.split("//")[1] == "icon":
            if tableau["icon"]:
                embed = discord.Embed(description=f'''<:Download:1193689126235553798> **[`Télécharger`]({guild.icon.url})**''')
                embed.set_image(url=tableau["icon"])
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Pas de logo sur le serveur.", ephemeral=True)

    try:
        custom_id = interaction.data['custom_id']
    except KeyError:
        custom_id = " "

# @noodle

    if custom_id.split("//")[0] == "pingmentionbot":
        guild = interaction.guild

    split_result = custom_id.split("//")
    if len(split_result) >= 2:
        if split_result[1] == "sysinfo":
            global startTime
            current_time = time.time()
            difference = int(round(current_time - startTime))

            l = []
            total_members = 0

            for guild in bot.guilds:
                l.append(str(guild.name) + str(guild.member_count))
                total_members += guild.member_count

            k_number = "{:.2f}k".format(total_members / 1000)

            headers = {'Authorization': 'Bearer ptlc_iOulNmU5AHYroZh0fmdE8gZMM0sA7OE2tzZY2ayVZhZ'}
            response = requests.get("https://panel.berchbrown.me/api/client/servers/b1545927/resources", headers = headers)
            if response.status_code == 200:
                data = response.json()['attributes']["resources"]

            ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)
            cpu_absolute = data["cpu_absolute"]
            unix_uptime = (data["uptime"])
            disk = round(int(data["disk_bytes"]) / (1024 * 1024), 2)
            tt_charge = 100 * (data["disk_bytes"]) / int(8375181312) 
            disk_2 = round(int (8375181312) / (1024 * 1024), 2)
            formatted_tt_charge = round(tt_charge, 2)

            up = int(startTime)
            embed = discord.Embed(description = f'''<:Arrow:1194020156846915635> **Information du Système** :
> **OS** : Linux
> **Coeurs** : `4`
> **RAM** : `{ram_used} MiB` / `{(psutil.virtual_memory().total // (1024 ** 2))} MB`
> **CPU** : `{cpu_absolute}%` 
> **Nombre de Shards** : `0`
> **Stockage** : `{disk} MB` / `{disk_2} MB`
> **Charge Totale** : `{formatted_tt_charge}%`
> **Nombre d'Utilisateurs** : `{k_number}`
> **Nombre de Serveur** : `{len(bot.guilds)}`
> **Nombre de Commandes Utilisées** : `...`
> **Bot Créé** : <t:1649368800:R>
> **Dernier Redémarrage** : <t:{up}:R>
> **Ping Actuel** : `{round(bot.latency * 1000, 2)}ms`
> **Langage des Scripts** : `Python 3.10.12`
> **/ Commands** : `108`
> **@event** : `2`
> **@loop** : `1`''', color = 0X2B2D31)

            embed.set_author(name = f'Informations du Bot', icon_url = guild.icon.url)
            await interaction.response.send_message(embed = embed, ephemeral = True)

        elif split_result[1] == "devs":

            embed = discord.Embed(description = f'''<:Arrow:1194020156846915635> Vous trouverez ci-dessous les informations concernant le propriétaire, les développeurs et les membres de l'équipe du staff.
                              
<:Responsable:1194024640281059449> **Créateur & Développeur Bot**
`1.` [`sirop2menthe_`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A créé le projet **<t:1649445749:R>**

<:TheRealCreator:1194020154191908905> **Responsable DashBoard & Développeur**
`2.` [`wizzarco`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1702291020:R>**

<:TheRealCreator:1194020154191908905> **Responsable Grafana/VPS & Développeur**
`3.` [`berchbrown`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1656928860:R>**
                              
<:TheRealCreator:1194020154191908905> **Responsable WebSite & Développeur**
`4.` [`xaya.`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1703693640:R>**
        
```                                  

```                                  
                                  
<:WebDev:1194027977470648330> **Développeuse WebSite**
`5.` [`anino75`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1650203460:R>**
                            
<:Heart:1189609724635795506> **Consultant & Conseiller**
`6.` [`sirlink_`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1704490140:R>**
                                                         
<:Earth:1193652678291640410> **Community Manager**
`7.` [`adqm.fr`](https://noodle-bot.fr/about-staff)
**Status :** <:DiscordStatusOnline:1184534287932989460> / A rejoint le projet **<t:1702077300:R>**''', color = 0X2B2D31)

            embed.set_author(name = f'A Propos des Développeurs', icon_url = guild.icon.url)
            await interaction.response.send_message(embed = embed, ephemeral = True)

        elif split_result[1] == "link":

            embed = discord.Embed(description = f'''<:DiscordMod:1193673354239033374> **[Serveur Support](https://discord.gg/YAju2FBKKK)**
N'hésitez pas à cliquer sur le lien du `Serveur de Support` et à rejoindre notre communauté pour toute assistance dont vous pourriez avoir besoin.
                              
<:Earth:1193652678291640410> **[Notre Site](https://noodle-bot.fr/)**
Cliquez sur ce lien pour être redirigé vers notre site internet !
                              
<:Link:1191708382550294588> **[Inviter le Bot](https://discord.com/api/oauth2/authorize?client_id=962051231973511318&permissions=39465179278711&scope=bot+applications.commands)**
Cliquez sur le bouton `Inviter le Bot` pour ajouter Noodle sur n'importe lequel de vos serveurs.
                              
<:Server:1193578128883335309> **[Voter sur Top.gg](https://top.gg/bot/962051231973511318)**
Cliquez sur l'option `Voter sur Top.gg` et votez pour l'incroyable Noodle (le best).
                              
<:Members:1189510759655411762> **[Politique de Confidentialité](https://palalink-1.gitbook.io/untitled/about-the-bot/privacy-policy-politique-de-confidentialite)**
Cliquez sur l'option `Politique de confidentialité` pour vérifier la politique de confidentialité de **NoodleBot**.
                              
<:Diamond:1189559520666587176> **[Conditions d'utilisation](https://palalink-1.gitbook.io/untitled/about-the-bot/terms-of-services-tos-cgu)**
Cliquez sur l'option `Conditions d'utilisation` pour être redirigé vers la page des conditions d'utilisation de **NoodleBot**.''', color = 0X2B2D31)

            embed.set_author(name = f'Liens Utiles de NoodleBot', icon_url = guild.icon.url)
            await interaction.response.send_message(embed = embed, ephemeral = True)

@tree.command(name = 'ping', description = 'Voir les latences de Noodle.')
async def ping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))

    up = int(startTime)

    headers = {'Authorization': 'Bearer ptlc_LlL7MBJkz1bCO83YjsfkOGz3DE4Upxs0qoUHUAo6aTq'}
    response = requests.get("https://panel.noodle-bot.fr/api/client/servers/aecf0c88/resources", headers = headers)
    if response.status_code == 200:
        data = response.json()['attributes']["resources"]

    ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)
    cpu_absolute = data["cpu_absolute"]
    unix_uptime = (data["uptime"])
    disk = round(int(data["disk_bytes"]) / (1024 * 1024), 2)

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

    embed = discord.Embed(description = f'''> Latence API : `{response.elapsed.total_seconds() * 100:.2f}ms`
> Latence DataBase : `...`
> Latence Bot : `{round(bot.latency * 1000, 2)}ms`
> Latence VPS : `{response.elapsed.total_seconds() * 1000:.2f}ms`
> UpTime Bot : <t:{up}:R>''', color = 0X2B2D31)

    embed.add_field(name = '<:Server:1195485496827199628> Ressources (Utilisées)', value = f'''RAM : `{ram_used} MiB` / `{(psutil.virtual_memory().total // (1024 ** 2))} MB`\nCPU : `{cpu_absolute}%`''')
    embed.set_author(name = f'Ping Bot / {guild.name}')

    await interaction.response.send_message(embed = embed)

@tree.command(name = 'uptime', description = 'Voir la date du dernier Reload du bot.')
async def uptime(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))

    up = int(startTime)

    embed = discord.Embed(description = f'''<:Timer:1195495722490011852> **Dernier Restart du Bot** : <t:{up}:R>''', color = 0X2B2D31)
    await interaction.response.send_message(embed = embed)

@tree.command(name = 'help', description = 'Afficher toutes les commandes.')
async def help(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    headers = {'Authorization': 'Bearer ptlc_iOulNmU5AHYroZh0fmdE8gZMM0sA7OE2tzZY2ayVZhZ'}
    response = requests.get("https://panel.berchbrown.me/api/client/servers/b1545927/resources", headers = headers)
    if response.status_code == 200:
        data = response.json()['attributes']["resources"]

    ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)

    embed = discord.Embed(description = f'''<:SlashPrefix:1194002886175227954> Préfixe pour ce serveur : `/`
<:WebDev:1194027977470648330> Total des commandes : `127`
<:Server:1195485496827199628> Latence Bot : `{round(bot.latency * 1000, 2)}ms` 

\👋 **Greet / Saluer**
> ↪ `/joingreetsetup` ; `/joingreet` ; `/pjoingreet` ; `/pjoingreetboost`.

\💎 **Roles**
> ↪ `/customrole` ; `/crsetup` ; `/activityrole` ; `/actrole` ; `/statusrole` ; `/srsetup` ; `/pautorole` ; `/pautorolesetup` ; `/pinvrole` ; `/pinvrolesetup`.

\🔧 **Utilitaire**
> ↪ `/autoresponse` ; `/tempvc` ; `/starboard` ;`/mediaonly` ; `/poll` ; `/afk` ; `/avatar` ; `/banner` ; `/boostcount` ; `/channelinfo` ; `/cancel` ; `/emojiinfo` ; `/firstmsg` ; `/membercount` ; `/list` ; `/roleinfo` ; `/revoke` ; `/steal` ; `/snipe` ; `/serverbanner` ; `/servericon` ; `/stickerinfo` ; `/serverinfo` ; `/translate` ; `/userinfo`.

\🎉 **Giveaway**
> ↪ `/gcreate` ; `/gend` ; `/greroll` ;`/glist`.

\⚡ **Automod**
> ↪ `/automod` ; `/automodsetup`.

\📌 **Moderation**
> ↪ `/pmodaccess` ; `/pdeletemodresponse` ; `/ban` ; `/purge` ; `/deafen` ; `/hide` ; `/hideall` ; `/kick` ; `/lock` ; `/lockall` ; `/timeout` ; `/modlogs` ; `/modstatus` ; `/nick` ; `/role` ; `/rolemenu` ; `/roleall` ; `/roleicon` ; `/temprole` ; `/unban` ; `/unbanall` ; `/undeafen` ; `/unhide` ; `/unhideall` ; `/unlock` ; `/unlockall` ; `/untimeout` ; `/unmuteall` ; `/vckick` ; `/vcmute` ; `/vcunmute` ; `/warn` ; `/warnclear`.

\🚀 **Application**
> ↪ `/papplications` ; `/papplicationsetup`.

\🔔 **Notifications**
> ↪ `/pnotifications` ; `/pnotificationsetup`.

\🧭 **Suivi des Votes**
> ↪ `/pvotetracker` ; `/votetrackersetup`.

\📜 **Logging**
> ↪ `/plogging` ; `/ploggingsetup` ; `/ploggingmenu`.

\🎟️**Ticket**
> ↪ `/pticket` ; `/pticketsetup`.

\🍕 **Fun**
> ↪ `/ttt` ; `/say` ; `/pic` ; `/compliment` ; `/cry` ; `/hug` ; `/kill` ; `/kiss` ; `/lick` ; `/pet` ; `/slap` ; `/wanted` ; `/dé` ; `/randomnumber` ; `/msg` ; `/rank` ; `/level` ; `/prediction` ; `/profil`.

\🔍 **Extras / Premium**
> ↪ `/activity` ; `/audit` ; `/aichat` ; `/botinfo` ; `/bi` ; `/botupdate` ; `/calculator` ; `/editcolor` ; `/help` ; `/invite` ; `/ping` ; `/profil` ; `/support` ; `/uptime` ; 
> `/vote` ; `/weather`.

<:Link:1191708382550294588> __**Liens Importants**__
[Invite](https://discord.com/api/oauth2/authorize?client_id=962051231973511318&permissions=39465179278711&scope=bot+applications.commands) / [Support](https://discord.gg/YAju2FBKKK) / [Voter](https://top.gg/bot/962051231973511318)''',
                          color = 0X2B2D31)

    embed.set_author(name = f'''Menu d'Aide de NoodleBot''', icon_url = guild.icon.url)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)
    await interaction.response.send_message(embed = embed)

@tree.command(name = 'dé', description = 'Lancer le dé.')
async def dé(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    nombre_random = random.randint(1, 6)

    embed = discord.Embed(description = f'''\🎲 Vous avez obtenus, **{nombre_random}** en lançant **le dé** !''', color = 0X2B2D31)
    embed.set_footer(text = f'Lancé par {author_member.name}', icon_url = author_member.avatar.url)
    await interaction.response.send_message(embed = embed)

@tree.command(name = 'randomnumber', description = 'Lancer le dé.')
async def randomnumber(interaction: discord.Interaction, minimum: int, maximum: int):
    author_member: discord.Member = interaction.user
    nombre_random = random.randint(minimum, maximum)

    embed = discord.Embed(description = f'''Tirage d'un **nombre aléatoire** entre `{minimum}` et `{maximum}` ...\n> `Nombre tiré` : **{nombre_random}** !''', color = 0X2B2D31)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)
    await interaction.response.send_message(embed = embed)

@tree.command(name = 'avatar', description = 'Afficher l\'avatar d\'un membre.')
async def avatar(interaction: discord.Interaction, membre: discord.Member):
    author_member: discord.Member = interaction.user
    
    embed = discord.Embed(description = f'''<:Download:1193689126235553798> **[`Télécharger`]({membre.avatar.url})**''')
    embed.set_image(url = f'{membre.avatar.url}')
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)

    await interaction.response.send_message(embed = embed)

@tree.command(name='say', description='Envoyer un message répété par le bot.')
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    not_allowed_words = ['@', 'everyone', 'here']

    embed_not_allowed = discord.Embed(description=f'''La façon correcte d'utiliser la commande est la suivante :
/say `[#channel]` `<texte>*`

`<texte>*` : Des mots sont interdits.''', color = 0X2B2D31)
    embed_not_allowed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)
    embed_not_allowed.set_author(name = f'Commande /say', icon_url = guild.icon.url)

    if any(word in message for word in not_allowed_words):
        await interaction.response.send_message(embed = embed_not_allowed, ephemeral = True)
    else:
        await channel.send(f'{message}')
    await interaction.response.send_message(f'''<:Arrow:1194020156846915635> Votre message a été envoyé dans le salon {channel.mention}''', ephemeral = True)

@tree.command(name = 'profil', description = 'Afficher le profil d\'un membre.')
async def profil(interaction: discord.Interaction, membre: discord.Member):

    author_member: discord.Member = interaction.user

    guild = bot.get_guild(1180817795064274967)

    badge_roles = {
        1183205593381601380: '<:Responsable:1194024640281059449> **Créateur**',
        1181346547544375417: '<:Members:1193674114045591653> **Utilisateur**',
        1183479565352435843: '<:Giveaway:1189516089546256434> **Amis**',
        1183204421795065897: '<:TheRealCreator:1194020154191908905> **Noodle Staff**',
    }

    guild = await bot.fetch_guild(1180817795064274967)
    GUILD = bot.get_guild(1180817795064274967)
    user_badges = [badge_roles[role_id] for role_id in badge_roles if (role := discord.utils.get(guild.roles, id=role_id)) and guild.get_member(membre.id) and role in guild.get_member(membre.id).roles]
    badges_description = "\n".join(user_badges) if user_badges else "Aucun badge"

    embed = discord.Embed(description = f'''### <:TheRealCreator:1194020154191908905> **Liste des badges**
                          
{badges_description}

Pour recevoir vos badges, vous devez être présent sur notre serveur de support. 
Pour rejoindre le serveur de support, [cliquez ici](https://discord.gg/YAju2FBKKK).''')
    
    guild = interaction.guild
    embed.set_author(name = f'Profil de {membre.name}', icon_url = guild.icon.url)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)
    embed.set_thumbnail(url = author_member.avatar.url)

    await interaction.response.send_message(embed = embed)

@tree.command(name = 'userinfo', description = 'Afficher les informations relatives à un membre.')
async def userinfo(interaction: discord.Interaction, membre: discord.Member):
    userFlags = membre.public_flags.all()
    print(membre.activity)
    guild = interaction.guild

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

    permissions_list = [f"{'+' if value else '-'} {perm.replace('_', ' ').title()}" for perm, value in membre.guild_permissions]
    formatted_permissions = "\n".join(permissions_list)

    embed = discord.Embed(description=f'''<:Members:1193674114045591653> __**A Propos de {membre.name}**__
**Pseudo** : `{membre.name}#{membre.discriminator}`
**Mention** : {membre.mention}
**ID** : `{membre.id}`
**Bot** : {"<:DiscordStatusOnline:1184534287932989460>" if membre.bot else "<:DiscordStatusOffline:1184534286364332102>"}
**Badge(s)** : {" ; ".join(badges)}
**Compte Créé** : <t:{int(membre.created_at.timestamp())}:D> (<t:{int(membre.created_at.timestamp())}:R>)
**A Rejoint** : <t:{int(membre.joined_at.timestamp())}:D> (<t:{int(membre.joined_at.timestamp())}:R>)

<:Activity:1195765463859331224> __**Activité**__
**Biographie** : `Indisponible pour le moment.`
**Joue/Stream/Ecoute...** : XXX

<:DiscordMod:1193673354239033374> __**Rôles**__ {len(membre.roles) - 1}
**Rôle le + Haut** : XXX
**Rôles** : {""" ; """.join([role.mention for role in membre.roles[1:]]) if len(membre.roles) > 1 else "Aucun"}

<:OneWaySign:1189511733765750865> __**Permissions sur Ce Serveur**__
```diff
{formatted_permissions}'
```
''', color = 0X2B2D31)

    embed.set_author(name = f'Informations de {membre.name}', icon_url = guild.icon.url)
    embed.set_thumbnail(url = membre.avatar.url)

    await interaction.response.send_message(embed = embed)


@tree.command(name = 'activity', description = '''Voir l'activité de quelqu'un.''')
async def activity(interaction: discord.Interaction, membre: discord.Member):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    custom_status = None
    for activity in membre.activities:
        if isinstance(activity, discord.CustomActivity):
            custom_status = activity.name
            break

    bio = custom_status if custom_status else 'Aucun statut personnalisé.'

    if membre.activities:
        for activity in membre.activities:
            if isinstance(activity, discord.Game):
                status = f'En train de jouer à {activity.name}'
                break
            elif isinstance(activity, discord.Streaming):
                status = f'En train de streamer {activity.name}'
                break
            elif isinstance(activity, discord.Spotify):
                status = f'Écoute Spotify - {activity.title} by {activity.artist}'
                break
        else:
            status = "Activité inconnue"
    else:
        status = "Aucune activité en cours."

    embed = discord.Embed(description = f'<:Activity:1195765463859331224> __**Activité**__\n'
                                      f'**Personnalité : {bio}**\n'
                                      f'**{status}**', color = 0X2B2D31)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)

    await interaction.response.send_message(embed = embed)

@tree.command(name = 'support', description = 'Besoin d\'Aide ? Exécutez cette commande !')
async def support(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    embed = discord.Embed(description = '''**Cliquez sur le bouton du serveur d'assistance pour rejoindre mon serveur d'assistance pour tout type d'aide !**''', color = 0X2B2D31)

    view = discord.ui.View()
    button = discord.ui.Button(label = "Discord Support", style = discord.ButtonStyle.secondary, emoji = '<:Link:1191708382550294588>', url = 'https://discord.gg/YAju2FBKKK')
    view.add_item(button)

    await interaction.response.send_message(embed = embed, view = view)

cooldowns_path = "./couldowns.json"

@tree.command(name = 'msg', description = '''Envoyer un message anonymement à quelqu'un.''')
async def msg(interaction: discord.Interaction, destinataire: discord.Member, message: str):
    author_id = str(interaction.user.id)
    guild = interaction.guild
    cooldowns = {}

    try:
        with open(cooldowns_path, 'r') as cooldowns_file:
            cooldowns = json.load(cooldowns_file)
    except FileNotFoundError:
        pass

    if 'cmd_msg' in cooldowns and author_id in cooldowns['cmd_msg']:
        cooldown_time = cooldowns['cmd_msg'][author_id]

        cooldown_datetime = datetime.fromisoformat(cooldown_time)

        if datetime.now() < cooldown_datetime:
            remaining_time = cooldown_datetime - datetime.now()
            remaining_seconds = remaining_time.seconds
            remaining_formatted = f'<t:{int(time.time() + remaining_seconds)}:R>'
            await interaction.response.send_message(f'''Tu pourras réutiliser la commande {remaining_formatted} !''', ephemeral = True)
            return

    cooldowns.setdefault('cmd_msg', {})[author_id] = (datetime.now() + timedelta(hours = 1)).isoformat()

    with open(cooldowns_path, 'w') as cooldowns_file:
        json.dump(cooldowns, cooldowns_file, indent = 4)

    embed = discord.Embed(color = 0X2B2D31)
    embed.set_author(name = f'Message envoyé de {interaction.user.name}', icon_url = guild.icon.url)

    await interaction.response.send_message(f'<:Arrow:1194020156846915635> Message envoyé à {destinataire.mention}.', ephemeral = True)
    await destinataire.send(message, embed = embed)

@tree.command(name = 'botinfo', description = 'Voir les informations sur le bot.')
async def botinfo(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    embed = discord.Embed(description = f'''<:Point:1196045136417783839>    NoodleBot se distingue comme un **bot Discord polyvalent**, **riche en fonctionnalités** \🛠️, dédié à **l'amélioration de l'expérience au sein de votre serveur**. \🎉 Des **outils de modération** aux **fonctionnalités de divertissement et d'utilité**, NoodleBot propose une gamme complète pour **répondre à toutes les exigences de votre communauté Discord**. \📌 Son **interface conviviale** et ses options de **commande diversifiées sont soigneusement conçues** pour accroître tant **le plaisir que l'efficacité dans votre serveur**. \🎉

<:Point:1196045136417783839>    Attentif à l'**optimisation**, NoodleBot se vante d'**une latence remarquablement basse** \⚡, **garantissant** des **réponses rapides** aux commandes et des **interactions fluides**. Grâce à son **infrastructure avancée** et à **des techniques de codage efficaces**, \🚀 Peu importe la taille de votre serveur, **NoodleBot assure constamment des résultats éclairs**, promettant une **expérience utilisateur inégalée**. \🔥

<:Point:1196045136417783839>    De plus, **NoodleBot évolue continuellement** grâce à des **mises à jour régulières** et à l'**ajout de nouvelles fonctionnalités** ; \📜 grâce aux **recommandations de ses utilisateurs**, demeurant ainsi à la **pointe de la technologie** pour **répondre aux besoins évolutifs** des communautés Discord. \⭐ Avec son **engagement** à couvrir de manière exhaustive **toutes les fonctionnalités de Discord**, **NoodleBot** se positionne comme **le choix idéal** pour ceux en quête d'**une expérience serveur équilibrée et immersive**. \💎
```
                          
```
''', color = 0X2B2D31)

    embed.set_author(name = f'Informations sur Noodle', icon_url = guild.icon.url)
    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)

    await interaction.response.send_message(embed = embed)

@tree.command(name = 'roleinfo', description = 'Voir les informations sur un rôle du serveur.')
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    permissions_list = [f"{'+' if value else '-'} {perm.replace('_', ' ').title()}" for perm, value in role.permissions]
    formatted_permissions = "\n".join(permissions_list)

    hex_color = f"#{role.color.value:06X}"

    unix_creation_time = int(role.created_at.timestamp())

    if role.mentionable == True:
        result = 'Oui'
    else:
        result = 'Non'

    embed = discord.Embed(description = f'''<:Arrow:1194020156846915635> {role.mention}

> **Nom** : `{role.name}`
> **Mention** : {role.mention}
> **ID** : `{role.id}`
> **Créé le** : <t:{unix_creation_time}:F> (<t:{unix_creation_time}:R>)
> **Couleur Hexagonale** : {hex_color}
> **Mentionnable** : `{result}`
> **Membres** : {len(role.members)}
> **Position** : {role.position}

<:OneWaySign:1189511733765750865> __**Permissions**__
```diff
{formatted_permissions}
```''', color = 0X2B2D31)

    embed.set_footer(text = f'Demandé par {author_member.name}', icon_url = author_member.avatar.url)
    embed.set_author(name = f'Informations sur un Rôle', icon_url = guild.icon.url)

    await interaction.response.send_message(embed = embed)

@tree.command(name = 'invite', description = 'Besoin d\'Aide ? Exécutez cette commande !')
async def invite(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    embed = discord.Embed(description = '''**Cliquez sur le bouton ci - dessous, pour m'ajouter !**''', color = 0X2B2D31)

    view = discord.ui.View()
    button = discord.ui.Button(label = "Invite Moi !", style = discord.ButtonStyle.secondary, emoji = '<:Link:1191708382550294588>', url = 'https://discord.com/api/oauth2/authorize?client_id=962051231973511318&permissions=8&scope=applications.commands%20bot')
    view.add_item(button)

    await interaction.response.send_message(embed = embed, view = view)

@tree.command(name='calculator', description='Résoudre un calcul !')
async def calculator(interaction: discord.Interaction, calcul: str):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    expression = sympify(calcul.replace("f'(x)", "diff(f, x)"))
    
    result = expression.evalf()
    embed = discord.Embed(description=f'\🎲 Le résultat de votre calcul, **{calcul}** est `{result:.2f}`!', color=0X2B2D31)
    embed.set_footer(text=f'Lancé par {author_member.name}', icon_url=author_member.avatar.url)

    await interaction.response.send_message(embed=embed) 

@tree.command(name='firstmessage', description='Mais qui a envoyé le premier message ?')
async def firstmessage(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild
    channel = interaction.channel

    async for message in channel.history(limit=1, oldest_first=True):
        first_message_author = message.author
        first_message_url = message.jump_url
        first_message_timestamp = message.created_at.timestamp()
        break
    else:
        await interaction.response.send_message("Aucun message trouvé dans ce salon.")
        return

    embed = discord.Embed(description=f'''> [Lien vers le premier message]({first_message_url})
> **Auteur** : {first_message_author.mention} (`{first_message_author.id}`)
> **Envoyé** : <t:{int(first_message_timestamp)}:R>''',
color=0X2B2D31)
    embed.set_footer(text=f'Demandé par {author_member.name}', icon_url=author_member.avatar.url)
    embed.set_author(name = f'Premier message du Salon', icon_url = message.guild.icon.url)
    
    await interaction.response.send_message(embed=embed)

@tree.command(name='membercount', description='Voir le nombre de personnes sur le serveur.')
async def membercount(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild
    channel = interaction.channel

    online_members = sum(member.status == discord.Status.online for member in guild.members)
    idle_members = sum(member.status == discord.Status.idle for member in guild.members)
    dnd_members = sum(member.status == discord.Status.dnd for member in guild.members)
    offline_members = sum(member.status == discord.Status.offline for member in guild.members)

    human_members = sum(not member.bot for member in guild.members)
    robot_members = sum(member.bot for member in guild.members)

    embed = discord.Embed(description=f'''> **Total de Membres** : {guild.member_count}
    **Humains** : {human_members}
    **Robots** : {robot_members}
    **En Ligne** : {online_members}
    **Inactifs** : {idle_members}
    **Ne Pas Déranger** : {dnd_members}
    **Hors Ligne** : {offline_members}''')

    embed.set_author(name=f'Nombre de Membres', icon_url=guild.icon.url)

    await interaction.response.send_message(embed=embed)

@tree.command(name='boostcount', description='Voir le nombre de boosts et le niveau de boost du serveur.')
async def boostcount(interaction: discord.Interaction):
    guild = interaction.guild

    boost_count = guild.premium_subscription_count
    boost_level = guild.premium_tier

    embed = discord.Embed(description=f'''**Nombre de Boosts** : {boost_count}
    **Niveau de Boost** : {boost_level}''')

    embed.set_author(name=f'Boost du Serveur', icon_url=guild.icon.url)

    await interaction.response.send_message(embed=embed)

@tree.command(name='bi', description='Voir les informations sur le bot.')
async def bi(interaction: discord.Interaction):
    guild = interaction.guild
    channel = interaction.channel

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))

    total_members = 0
    k_number = ""
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
        k_number = "{:.2f}k".format(total_members / 1000)

    up = int(startTime)

    embed = discord.Embed(description=f'''**Développeur** : `Sheikoo_`
    **Nom** : `NoodleBot`
    **Créé le** : <t:1649368800:R>
    **Version de discord.py** : `v2.3.2`
    **Version de Python** : `v3.12.2`
    **Contact** : `contact.hugoregnault@gmail.com`
    **Dernier Redémarrage** : <t:{up}:R>
    
    **Nombre de Serveurs** : `{str(len(bot.guilds))}`
    **Utilisateurs** : `{k_number}`''')

    embed.set_author(name=f'Informations sur NoodleBot', icon_url=guild.icon.url)

    await interaction.response.send_message(embed=embed)

@tree.command(name = 'vote', description = '''Votez pour le bot, c'est par ici !''')
async def vote(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    embed = discord.Embed(description = '''**Cliquez sur le bouton ci - dessous, pour voter pour moi !**''', color = 0X2B2D31)

    view = discord.ui.View()
    button = discord.ui.Button(label = "Invite Moi !", style = discord.ButtonStyle.secondary, emoji = '<:Link:1191708382550294588>', url = 'https://top.gg/bot/962051231973511318')
    view.add_item(button)

    await interaction.response.send_message(embed = embed, view = view)

@tree.command(name = 'aichat', description= 'Parler avec une AI.')
async def aichat(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild
    
    embed = discord.Embed(description=f'''Ce module est temporairement indisponible, il sera disponible en V2 de Noodle, lors de l'ajout du "Mode Premium".
Pour + d'informations, consultez notre [documation sur le mode "Premium"](https://noodle-bot.fr/premium-options)''')
    
    embed.set_author(name=f'Parler avec une IA', icon_url=guild.icon.url)
    
    await interaction.response.send_message(f'{author_member.mention}', embed = embed)

data_file = './data_infractions.json'

@tree.command(name='ban', description='Bannir un membre du serveur.')
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = 'Aucune raison précisée.'):
    author_member = discord.Member = interaction.user

    try:
        with open(data_file, 'r') as f:
            warnings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        warnings = {}

    guild_id = interaction.guild.id
    current_time = int(datetime.now().timestamp())

    ban_count = len(warnings.get(str(member.id), [])) + 1
    ban_identifier = f'ban_{ban_count}'

    if str(member.id) in warnings:
        warnings[str(member.id)].append({
            'ban_id': ban_identifier,
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'member_name': member.display_name,
            'timestamp': current_time,
            'guild_name': interaction.guild.name
        })
    else:
        warnings[str(member.id)] = [{
            'ban_id': ban_identifier,
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'member_name': member.display_name,
            'timestamp': current_time,
            'guild_name': interaction.guild.name
        }]

    with open(data_file, 'w') as f:
        json.dump(warnings, f, indent=2)

    if member.id == author_member.id:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Vous ne pouvez pas vous bannir vous-même !')

    if member.top_role.position > author_member.top_role.position:
        return await interaction.response.send_message(f'<:UserPermissionsError:1191513416020533398> Vous ne pouvez pas bannir cette personne car elle a un rôle supérieur au vôtre !')

    if member.guild_permissions.ban_members:
        return await member.send(f'<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !')

    try:
        await member.send(f'''
        ## \🔒 **Bannissement du Serveur `{interaction.guild.name}`. **

Salut {member.mention},
Nous espérons que ce message te trouve bien. Malheureusement, nous devons t'informer que tu as été banni du serveur **`{interaction.guild.name}`** par __{author_member.mention}__.

\📜 **Raison du Bannissement :**
```diff
- {reason}
```

\📌 **Si tu as des questions ou si tu souhaites discuter de cette décision, n'hésite pas à contacter l'administrateur responsable.**

> Nous te rappelons que le respect des règles du serveur est crucial pour maintenir un environnement positif pour tous les membres. Nous espérons que tu comprends cette mesure et que tu pourras apprendre de cette expérience.

Cordialement,
L'équipe de modération de **`{interaction.guild.name}`** .''')
        await interaction.guild.ban(member, reason=reason)
        await interaction.response.send_message(f'<:Valid:1191522096958939236> {member.mention} **a été banni !**')

    except:
        return await interaction.response.send_message(f'<:BotError:1191522519824478269> Je n\'arrive pas à bannir ce membre !')

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
            'action': "warn",
            'author_name': author_member.display_name,
            'member_name': membre.display_name,
            'timestamp': current_time,
            'guild_name': interaction.guild.name
        })
    else:
        warnings[str(membre.id)] = [{
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'action': "warn",
            'author_name': author_member.display_name,
            'member_name': membre.display_name,
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

@tree.command(name='modlogs', description='Voir la liste des infractions d\'une personne.')
async def modlogs(interaction: discord.Interaction, membre: discord.Member):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    with open('./data_infractions.json', 'r') as file:
        infractions_data = json.load(file)

    if str(membre.id) in infractions_data:
        infractions = infractions_data[str(membre.id)]

        embed = discord.Embed(description=f'''Nombre de Sanctions : `{len(infractions)}`''')
        embed.set_author(name=f'Liste des Sanctions.', icon_url=guild.icon.url)

        for infraction in infractions:
            action = infraction["action"]
            emoji = get_emoji(action)

            embed.add_field(
                name=f'{emoji} {action.capitalize()}',
                value=f'''> **Membre** : {infraction["member_name"]} (`{membre.id}`)
                > **Modérateur** : {infraction["author_name"]} (`{infraction["author_id"]}`)
                > **Action** : {action}
                > **Raison :** {infraction["reason"]}
                > **Serveur** : {infraction["guild_name"]} (`{infraction["guild_id"]}`)
                > **Date** : <t:{infraction["timestamp"]}> (<t:{infraction["timestamp"]}:R>)''',
                inline=False
            )

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f'Aucune infraction trouvée pour {membre.mention}.', ephemeral=True)

def get_emoji(action):
    emojis = {
        'warn': '<:Adding:1203371077368287302>',
        'ban': '<:DiscordMod:1193673354239033374>',
        'timeout': '<:Timer:1195495722490011852>',
        'kick': '<:Kick:1203371079469371492>',
    }
    return emojis.get(action, '')

@tree.command(name='timeout', description='Exclure temporairement un membre du serveur.')
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison n'a été précisée''', days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Vous ne pouvez pas vous exclure temporairement vous-même !', ephemeral=True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'<:UserPermissionsError:1191513416020533398> Vous ne pouvez pas exclure temporairement cette personne car elle est à un rôle supérieur à vous !', ephemeral=True)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !', ephemeral=True)

    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if duration >= timedelta(days=28):
        return await interaction.response.send_message(f'<:Info:1191696749178408970> La durée d\'exclusion doit être inférieure à `28` jours !', ephemeral=True)

    end_timestamp_utc = int((datetime.now() + duration).timestamp())
    duration_str = f'<t:{end_timestamp_utc}:R>'
    command_timestamp_utc = int(datetime.now(pytz.utc).timestamp())

    end_datetime_utc = datetime.utcfromtimestamp(end_timestamp_utc).replace(tzinfo=pytz.utc)
    duration_str = f'<t:{int(end_datetime_utc.timestamp())}:R>'

    await membre.send(f'''## \⌛ **Timeout du Serveur `{guild.name}`. **

Salut {membre.mention}, tu as été temporairement exclu du serveur **`{guild.name}`** par __{author_member.mention}__.
> \⏰ **Durée du Timeout :** `{duration}`

\📜 **Raison du Timeout :**
```diff
+ {reason}
```

\📌 Tu retrouveras ta parole sur ce serveur, {duration_str}.''')

    infractions_data_path = './data_infractions.json'
    with open(infractions_data_path, 'r') as file:
        infractions_data = json.load(file)

    user_id_str = str(membre.id)
    if user_id_str not in infractions_data:
        infractions_data[user_id_str] = []

    infractions_data[user_id_str].append({
        "action": "timeout",
        "author_id": author_member.id,
        "guild_id": guild.id,
        "reason": reason,
        "author_name": str(author_member),
        "member_name": str(membre),
        "timestamp": command_timestamp_utc,
        "guild_name": guild.name,
        "duration": str(duration)
    })

    with open(infractions_data_path, 'w') as file:
        json.dump(infractions_data, file, indent=2)

    await membre.timeout(duration, reason=reason)
    await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} a été temporairement rendu muet ({duration}) !', ephemeral=True)

@tree.command(name='kick', description='Expulser un membre du serveur.')
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison précisée.'''):
    author_member: discord.Member = interaction.user
    guild = interaction.guild

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Vous ne pouvez pas vous expulser vous-même !', ephemeral=True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'<:UserPermissionsError:1191513416020533398> Vous ne pouvez pas expulser cette personne car elle est à un rôle supérieur à vous !', ephemeral=True)

    if membre.guild_permissions.kick_members:
        return await interaction.response.send_message(f'<:UserError:1191512488932540476> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !', ephemeral=True)

    await membre.send(f'''## \📌 **Expulsion du Serveur `{guild.name}`. **

Salut {membre.mention}, tu as été expulsé du serveur **`{guild.name}`** par __{author_member.mention}__.
> \📜 **Raison de l'Expulsion :**
```diff
+ {reason}
```

\📌 Tu peux revenir sur ce serveur à tout moment si tu le souhaites.''')
    
    infractions_data_path = './data_infractions.json'
    with open(infractions_data_path, 'r') as file:
        infractions_data = json.load(file)

    user_id_str = str(membre.id)
    if user_id_str not in infractions_data:
        infractions_data[user_id_str] = []

    command_timestamp_utc = int(datetime.now(pytz.utc).timestamp())

    infractions_data[user_id_str].append({
        "action": "kick",
        "author_id": author_member.id,
        "guild_id": guild.id,
        "reason": reason,
        "author_name": str(author_member),
        "member_name": str(membre),
        "timestamp": command_timestamp_utc,
        "guild_name": guild.name
    })

    with open(infractions_data_path, 'w') as file:
        json.dump(infractions_data, file, indent=2)

    await membre.kick(reason=reason)

    await interaction.response.send_message(f'<:Valid:1191522096958939236> {membre.mention} a été expulsé du serveur !', ephemeral=True)


# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME LEVELLING                                                            #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------
# RANK
# ------------------------------------------

class view_guildbutton(discord.ui.View):
    def __init__(self, server_name):
        super().__init__()
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label=server_name, disabled=True))


@bot.event
async def on_message(message):
    if not message.author.bot:

        response = manage_exp_event(message.author)
        levels = read_file('./levels.json')
        level = get_level(levels[str(message.author.id)]['experience'])
        author_name = message.author.name
        author_mention = message.author.mention

        if message.guild:
            server_name = message.guild.name

        if response == "level_gained":
            await message.channel.send(f'''<:Giveaway:1189516089546256434>  **Bravo {author_mention}, tu viens de passer un niveau !** (Level **{level}**)''')

        # Partie InterServ
        class view_guildbutton(discord.ui.View):
            def __init__(self, server_name):
                super().__init__()
                self.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label=server_name, disabled=True))

        if any(word in message.content for word in (
        'http', 'www.', '@here', '@everyone', 'recrut', 'Recrute', '@', '#', '<@', '<#', '>', 'nergo', 'pédé', 'enculé',
        'salope', 'fils de pute', 'connard', 'bougnoul', 'tapette', 'PD', 'nique ta mère', 'FDP', 'retardé', 'enculer',
        'crétin', 'tarlouze', 'sale race', 'bâtard', 'chiennasse', 'tête de nœud', 'zgueg')):
            return
        salons_data = read_file('./salons.json')

        if message.channel.id in salons_data["salons_ids"]:
            for salon_id in salons_data["salons_ids"]:
                if salon_id != message.channel.id:
                    salon = bot.get_channel(salon_id)

                    if salon:
                        await asyncio.sleep(5)
                        webhook = await salon.create_webhook(name=author_name)
                        await asyncio.sleep(5)
                        await webhook.send(
                            content=f"{message.content}",
                            avatar_url=message.author.avatar.url,
                            view=view_guildbutton(server_name))
                        await asyncio.sleep(5)
                        await webhook.delete()
                        
# Mention Bot
                        
        if message.author.id == 1189355739815350282 or message.content.lower() in ["noodlebot", "1189355739815350282", '<@1189355739815350282>', '<!@1189355739815350282>', '<@!1189355739815350282>']:
            if not hasattr(bot, 'mention_replied') or not bot.mention_replied:
                embed = discord.Embed(description = f'''Hey {message.author.mention},
<:SlashPrefix:1194002886175227954> Mon préfix pour ce serveur est `/`
                                  
Utilise </help:1180816142030352424> pour plus d'information.''', color = 0X2B2D31)

                embed.set_author(name = f'{message.guild.name}', icon_url = message.guild.icon.url)
                embed.set_footer(text = f'Mention de {message.author.name}', icon_url = message.author.avatar.url)
                embed.set_image(url = 'https://cdn.discordapp.com/attachments/1193687694228869322/1194003536799862814/card_background.png?ex=65aec572&is=659c5072&hm=f9b4e6842cf2d0345b9972147940995c729d99995de8e15d6458f184c90bc307&')
            
                view = discord.ui.View()
                button = discord.ui.Button(label = "Information Système", style = discord.ButtonStyle.green, custom_id = f"pingmentionbot//sysinfo")
                view.add_item(button)
                button = discord.ui.Button(label = "Développeurs", style = discord.ButtonStyle.danger, custom_id = f"pingmentionbot//devs")
                view.add_item(button)
                button = discord.ui.Button(label = "Liens Utiles", style = discord.ButtonStyle.primary, custom_id = f"pingmentionbot//link")
                view.add_item(button)
            
                await message.channel.send(embed = embed, view = view)

# RANK

lniv, l_add_exp = 3, 75
max_lvl = 50
experience_ref = {0: 100, 1: 155, 2: 220}

for i in range(0, max_lvl - 1):
    experience_ref[lniv] = experience_ref[lniv - 1] + l_add_exp
    lniv += 1
    l_add_exp += 10

def get_level(exp: int, type: int = 1):
    level = 0
    for i in experience_ref.keys():
        if exp >= experience_ref[i]:
            exp -= experience_ref[i]
            level += 1
        else:
            break
    if type == 1:
        return level
    elif type == 2:
        return exp, level


def get_rank(user_id: int = None, limit: int = 10):
    levels = read_file('./levels.json')
    data_levels = levels
    data_ranks = {}
    for guild in bot.guilds:
        for member in guild.members:
            if str(member.id) in data_levels.keys():
                data_ranks[member.id] = data_levels[str(member.id)]["experience"]
            else:
                data_ranks[member.id] = 0

    data_ranks = sorted(data_ranks.items(), reverse=True, key=lambda i: i[1])
    if user_id != None:
        rank = 1
        for s in data_ranks:
            if s[0] == user_id:
                if s[1] == 0:
                    return 0
                else:
                    return rank
            else:
                rank += 1
    else:
        return data_ranks[0:limit]

def manage_exp_event(member):
    levels = read_file('./levels.json')
    if not str(member.id) in levels:
        levels[str(member.id)] = {}
        levels[str(member.id)]['experience'] = 0
        levels[str(member.id)]['last_gain'] = 0
    level_before = get_level(levels[str(member.id)]['experience'], 1)
    if time.time() - levels[str(member.id)]['last_gain'] > 60:
        exp_gained = random.randint(1, 25)
        levels[str(member.id)]['experience'] += exp_gained
        levels[str(member.id)]['last_gain'] = time.time()
    level_after = get_level(levels[str(member.id)]['experience'], 1)
    write_file('./levels.json', levels)
    if level_after > level_before:
        return "level_gained"
    return "success"

def manage_levels_xp(member, type, method, quantity):
    levels = read_file('./levels.json')
    if not str(member.id) in levels:
        levels[str(member.id)] = {}
        levels[str(member.id)]['experience'] = 0
        levels[str(member.id)]['last_gain'] = 0
    if type == "niveau":
        if method == "add":
            for i in range(quantity):
                level = get_level(levels[str(member.id)]['experience'])
                levels[str(member.id)]['experience'] += experience_ref[level]
        elif method == "remove":
            for i in range(quantity):
                level = get_level(levels[str(member.id)]['experience'])
                levels[str(member.id)]['experience'] -= experience_ref[level]
        else:
            return "invalid_method"
    elif type == "experience":
        if method == "add":
            levels[str(member.id)]['experience'] += quantity
        elif method == "remove":
            levels[str(member.id)]['experience'] -= quantity
        else:
            return "invalid_method"
    else:
        return "invalid_type"
    write_file('./levels.json', levels)

# Couleur
fill = 26, 26, 26

def draw_rounded_rectangle(image, bounds, width=1, antialias=4, fill=(fill)):
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='RGBA')
    draw = ImageDraw.Draw(mask)
    for offset, fill in (width / -2, fill), (width / 2, fill):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.rounded_rectangle([left, top, right, bottom], fill=fill, radius=100)
    mask = mask.resize(image.size, Image.LANCZOS)

    image.paste(mask, (0, 0), mask)

# 800 x 235

@tree.command(name='rank', description='Permet de voir votre niveau, et classement.')
async def rank(interaction: discord.Interaction, user: discord.Member = None):
    author_member: discord.Member = interaction.user
    if user is None:
        user = interaction.user
    levels = read_file('./levels.json')
    if str(user.id) not in levels:
        return await interaction.response.send_message('<:Warning:1181322717618765974> Il faut que vous ayez au moins envoyé un message, actuellement vous en avez envoyé 0 !')
    
    experience, level = get_level(levels[str(user.id)]['experience'], 2)
    jauge_width = int(experience / experience_ref[level] * 550)
    card = Image.open("./card_background.png")
    rank = get_rank(user.id)

    experience_str = str(experience)
    if experience > 999:
        experience_str = f"{round(experience / 1000, 1)}k"

    max_xp_str = str(experience_ref[level])
    if experience_ref[level] > 999:
        max_xp_str = f"{round(experience_ref[level] / 1000, 1)}k"

    asset = user.avatar
    avatar = BytesIO(await asset.read())

    pfp = Image.open(avatar)
    pfp = pfp.resize((155, 155))
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS if hasattr(Image, 'ANTIALIAS') else Image.LANCZOS)

    draw_ = ImageDraw.Draw(card, "RGBA")
    draw_.rounded_rectangle((10, 10, 790, 225), radius=3, fill=(60, 60, 60, 180))
    card.paste(pfp, (32, 42), mask)
    rectangle_box = [210, 155, 760, 190]
    draw_rounded_rectangle(card, rectangle_box, fill=(80, 80, 80))

    rectangle_box = [210, 155, 210 + jauge_width, 190]

    if jauge_width > 35:
        draw_rounded_rectangle(card, rectangle_box)
    else:
        rectangle_box = [210, 155, 210 + 35, 190]
        draw_rounded_rectangle(card, rectangle_box)

    fnt = ImageFont.truetype('/Users/hugo/Desktop/Discord/Projets/NoodleBot/V2/Bot/Montserrat.ttf', 35)
    fnt2 = ImageFont.truetype('/Users/hugo/Desktop/Discord/Projets/NoodleBot/V2/Bot/Montserrat.ttf', 45)
    fnt3 = ImageFont.truetype('/Users/hugo/Desktop/Discord/Projets/NoodleBot/V2/Bot/Montserrat.ttf', 25)
    m1 = f'#{rank}'
    bbox1 = draw_.textbbox((0, 0), m1, font=fnt2)
    w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
    m2 = f'RANK'
    bbox2 = draw_.textbbox((0, 0), m2, font=fnt3)
    w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    m3 = f'LEVEL'
    bbox3 = draw_.textbbox((0, 0), m3, font=fnt3)
    w3, h3 = bbox3[2] - bbox3[0], bbox3[3] - bbox3[1]
    m4 = f'{level}'
    bbox4 = draw_.textbbox((0, 0), m4, font=fnt2)
    w4, h4 = bbox4[2] - bbox4[0], bbox4[3] - bbox4[1]
    m5 = f'{experience_str}/{max_xp_str} XP'
    bbox5 = draw_.textbbox((0, 0), m5, font=fnt3)
    w5, h5 = bbox5[2] - bbox5[0], bbox5[3] - bbox5[1]
    m6 = user.name
    bbox6 = draw_.textbbox((0, 0), m6, font=fnt)
    w6, h6 = bbox6[2] - bbox6[0], bbox6[3] - bbox6[1]

    if w6 < 430:
        draw_.text((210, 145 - h6), user.name, font=fnt, fill="white")
    else:
        draw_.text((210, 145 - h6), user.name, font=ImageFont.truetype('/Users/hugo/Desktop/Discord/Projets/NoodleBot/V2/Bot/Montserrat.ttf', 20), fill="white")

    draw_.text((800 - w5 - 35, 125), f"{experience_str}/{max_xp_str} XP", font=fnt3, fill="white")
    draw_.text((800 - w3 - w4 - 55, 45), f"LEVEL", font=fnt3, fill=(fill))
    draw_.text((800 - w4 - 40, 30), f"{level}", font=fnt2, fill=(fill))
    draw_.text((800 - (w3 + w4 + 85) - w1 - w2, 45), f"RANK", font=fnt3, fill="white")
    draw_.text((800 - w1 - w3 - w4 - 70, 30), f"#{rank}", font=fnt2, fill="white")

    card.save(f"card_{user.id}.png")
    await interaction.response.send_message(file=discord.File(f"card_{user.id}.png"))
    os.remove(f"card_{user.id}.png")

# ------------------------------------------
# RANK
# ------------------------------------------
# ------------------------------------------
# LEADERBOARD
# ------------------------------------------

def get_leaderboard(type):
    if type == "levels":
        levels = read_file('./levels.json')
        leaderboard = [(i, levels[i]['experience']) for i in levels]
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        return sorted_leaderboard, len(levels)

@tree.command(name='leaderboard', description='Permet de voir un classement')
async def leaderboard(interaction: Interaction):
    levels = read_file('./levels.json')
    total_users = sum('experience' in user_data for user_data in levels.values())

    leaderboard_data = get_leaderboard("levels")
    leaderboard_list, _ = leaderboard_data
    author_member: discord.Member = interaction.user

    rank = 0
    str_leaderboard = ""
    author_rank = 0
    a_rank = get_rank(author_member.id)

    for (user_id, experience) in leaderboard_list[0:10]:
        rank += 1
        user = bot.get_user(int(user_id))

        if user is not None:
            username = user.name
            userid = user.id
            exp, level_ = get_level(experience, 2)

            if rank == 1:
                str_leaderboard += f'\🥇 <@{userid}>  -  Niveau **{level_}**\n'
            elif rank == 2:
                str_leaderboard += f'\🥈 <@{userid}>  -  Niveau **{level_}**\n'
            elif rank == 3:
                str_leaderboard += f'\🥉 <@{userid}>  -  Niveau **{level_}**\n'
            else:
                str_leaderboard += f'`#{rank}` <@{userid}>  -  Niveau **{level_}**\n'

    embed = discord.Embed(title = f'''Classement d'XP''',
                          description = f'''> » Voici les dix premiers participants inter-serveurs.\n\n {str_leaderboard}\n\n**Mon classement**\n> Vous êtes classé à la `{a_rank}e` place, parmis `{total_users}` participants !''',
                          color = 0xFFFFFF)

    embed.set_image(url = 'https://cdn.discordapp.com/attachments/1180904738078863431/1182549075439145021/Rank.png?ex=658519a6&is=6572a4a6&hm=d3e0999f1399020590128f870fec28098bd810684c1f3ba1fdbfe450a3d27761&')
    await interaction.response.send_message(embed = embed)

# ------------------------------------------
# LEADERBOARD
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME LEVELLING                                                            #
# ------------------------------------------------------------------------------------------------------------------------------ #

bot.run('TOKEN')