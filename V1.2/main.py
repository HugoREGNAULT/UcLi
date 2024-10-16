import discord, asyncio, json, re, time, random, requests, typing, json, os, uuid, psutil, datetime, warnings, pytz

warnings.filterwarnings('ignore', category=DeprecationWarning)

from discord import ui, app_commands, Interaction, SelectOption, SelectMenu, ButtonStyle, ActionRow, Button
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from discord.utils import get
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ------------------------------------------
# VARIABLES
# ------------------------------------------

API_ENDPOINT = "https://noodleapi.berchbrown.me/"
API_AUTH = ("noodle", "4l-7MJw5!Z8?8?p5gOUOA^5TSycQh")

# ------------------------------------------
# CONFIGURATIONS ET INFORMATIONS GLOBALES
# ------------------------------------------


def read_file(file):
    r = requests.get(f"{API_ENDPOINT}/files", params={"path": file}, auth=API_AUTH)
    try:
        return r.json()
    except:
        return None


def write_file(file, var):
    r = requests.post(f"{API_ENDPOINT}/files", params={"path": file}, auth=API_AUTH, json=var)
    return r.json()


PERM_ADMIN_ID = 1168586849380474930

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            bio.start()
            print('bio ✔️')
            stats_channels.start()
            print('stats channels ✔️')
            check_giveaways.start()
            print('giveaways data ✔️')
            #            remind_votes.start()
            #            print('remind votes ✔️')
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


# ------------------------------------------
# description / bio
# ------------------------------------------

@tasks.loop(seconds=4)
async def bio():
    await bot.wait_until_ready()
    total_members = 0
    k_number = ""
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
        k_number = "{:.2f}k".format(total_members / 1000)
        ratio = (total_members / len(bot.guilds))
    status = [f'{str(len(bot.guilds))}/100 Serveurs', f'{k_number} Utilisateurs', f'Ratio : {ratio} /Serveur']
    for i in status:
        await bot.change_presence(activity=discord.Game(str(i)))
        await asyncio.sleep(4)


# ------------------------------------------
# description / bio
# ------------------------------------------
# ------------------------------------------
# stats_channels
# ------------------------------------------

@tasks.loop(seconds=300)
async def stats_channels():
    await bot.wait_until_ready()
    l = []
    total_members = 0

    for guild in bot.guilds:
        l.append(str(guild.name) + str(guild.member_count))
        total_members += guild.member_count

    k_number = "{:.2f}k".format(total_members / 1000)

    users_voc_channel = bot.get_channel(1182347473314914405)
    guild_voc_channel = bot.get_channel(1182347501743910933)
    ratio_voc_channel = bot.get_channel(1184526113830097057)

    ratio = (total_members / len(bot.guilds))

    await users_voc_channel.edit(name='🎉・Pepoules : ' + f'{k_number}')
    await guild_voc_channel.edit(name='🔮・Serveurs : ' + f'{len(bot.guilds)}')
    await ratio_voc_channel.edit(name='🏆・Ratio : ' + f'{ratio}')

    await asyncio.sleep(300)


# ------------------------------------------
# stats_channels
# ------------------------------------------
# ------------------------------------------
# on_member_join
# ------------------------------------------

@bot.event
async def on_member_join(member):
    guild = member.guild

    server_role_mapping = {
        1180817795064274967: 1181346547544375417,
    }

    if guild.id in server_role_mapping:
        role_id = server_role_mapping[guild.id]
        role = guild.get_role(role_id)

        if role:
            await member.add_roles(role)
            welcome_channel = guild.get_channel(1180904783050182726)
            await welcome_channel.send(
                f'''Bienvenue {member.mention} sur **Noodle Support** ! Grâce à toi, nous sommes `{guild.member_count}`.''')


# ------------------------------------------
# on_member_join
# ------------------------------------------
# ------------------------------------------
# on_guild_remove
# ------------------------------------------

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(1180905067717599272)

    # Message sur le support

    embed = discord.Embed(description=f'''Je viens de partir du **{guild.name}**, `-{guild.member_count}` membres.''',
                          color=0X1A1A1A)


# ------------------------------------------
# on_guild_remove
# ------------------------------------------
# ------------------------------------------
# on_guild_join
# ------------------------------------------

@bot.event
async def on_guild_join(guild):
    invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, unique=True)

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

    embed = discord.Embed(title=f'{guild.name} ({guild.id})',
                          description=f'''> Salons Textuels : `{text_channels}` ; Salons Vocaux : `{voice_channels}` ; Fils : `{threads}` ; Rôles : `{num_roles}` 

                            » **Nom du Serveur** : `{guild.name}` *{guild.id}*
                            » **Membres** : **{guild.member_count}**''',
                          color=0xF2BB27)

    embed.set_author(name=f'Nouveau Serveur !',
                     icon_url=f'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.timestamp = datetime.utcnow() + timedelta(hours=1)

    embed.add_field(name='Propriétaire', value=f'''{guild.owner.mention} ||{guild.owner.id}||''', inline=False)
    embed.add_field(name='Membres', value=member_count, inline=True)
    embed.add_field(name='Boosts', value=f"{boost_count} boost(s) (Palier {boost_level})", inline=True)
    embed.add_field(name='Niveau de Verif\'', value=verification_level, inline=True)
    embed.add_field(name='Online', value=online_count, inline=True)
    embed.add_field(name='Offline', value=offline_count, inline=True)
    embed.add_field(name='Ne pas Déranger', value=dnd_count, inline=True)
    embed.add_field(name=f'Emojis ({num_emojis})', value=f"{emojis_str}", inline=False)
    embed.add_field(name="Date de création", value=f'<t:{int(datetime.timestamp(guild.created_at))}:D>', inline=False)
    embed.add_field(name="Rejoint le", value=f'<t:{int(guild.me.joined_at.timestamp())}:D>', inline=False)

    channel = bot.get_channel(1180905067717599272)
    await channel.send(embed=embed)

    # MP le Gérant du serveur ou vient d'être ajouté le bot

    message = (
        f'''Nous vous conseillons de rejoindre le serveur support, si vous avez des questions ! https://discord.gg/npctWa7fMc''')
    embed = discord.Embed(title='''Merci d'avoir ajouté Noodle sur un de vos serveur !''',
                          description=f'''Pour afficher la page d'aide, tapez `/help`.\nVous souhaitez participer en aidant à développer le bot ? Faites une suggestion en faisant : `/suggestion` !''',
                          color=0X1A1A1A)
    await guild.owner.send(message, embed=embed)

    # Création d'un channel que personne ne peut voir sauf le gérant, embed + @le gerant

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.owner: discord.PermissionOverwrite(read_messages=True)
    }

    new_channel = await guild.create_text_channel('📒・noodlebot', overwrites=overwrites)
    message = (
        f'''> » Merci de m'avoir ajouté {guild.owner.mention} ! Merci de lire attentivement cet embed, et également d'aller voir vos MPs avec <@962051231973511318>.''')

    embed = discord.Embed(title='Informations NoodleBot',
                          description=f'''Salutations,
                          Merci de m'avoir ajouté sur le `{guild.name}` !
                          Voici quelques principales informations concernant le bot.

                          > \📌 Le bot est essentiellement fonctionnel sur les PalaGames, les Blacklists et la Modération. Vous pourrez retrouver toutes les commandes disponibles en faisant `/help`.

                          > \⭐ Egalement, si vous trouvez des bug, hésitez pas à nous les report en faisant `/report`. Et si vous avez une idée ou une suggestion, ce sera `/suggestion` !

                          Enfin, si vous avez des **questions ou remarques**, le **staff** sera heureux de vous aider. Voici le serveur de support (Cliquez sur le button en bas) ! Bonne découverte.''',
                          color=0X1A1A1A)

    embed.set_author(name='''NoodleBot est opérationnel ! Merci de m'avoir ajouté.''',
                     icon_url='https://cdn.discordapp.com/emojis/1180830461946245160.webp?size=80&quality=lossless')

    await new_channel.send(message, embed=embed, view=view_linkedbutton())


class view_linkedbutton(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(style=discord.ButtonStyle.link, label='Serveur support',
                              url='https://discord.gg/W3g8aV6EFK', emoji='<:link:1183469115780911134>'))


# ------------------------------------------
# on_guild_join
# ------------------------------------------
# ------------------------------------------
# HELP
# ------------------------------------------

@tree.command(name='help', description='Afficher la liste des commandes.')
async def help(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(description=f'''» **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes disponibles** : `54`
    » **Préfix** : `/<commande>`

    *Ne manquez pas l'opportunité de découvrir notre __[`nouveau site`](https://noodle.fr/)__.* *Non dispo*''',
                          color=0x1A1A1A)

    embed.set_author(name=f'/help',
                     icon_url='https://cdn.discordapp.com/emojis/1181323583281188994.webp?size=80&quality=lossless')
    embed.timestamp = datetime.utcnow() + timedelta(hours=1)

    embed.add_field(name='''\📌 Administration''',
                    value='''> • `/note` ; `pingall` ; `webstatus` ; `uptime` ; `guilds` ; `adminlinks` ; `adminping`.''',
                    inline=False)
    embed.add_field(name='''\🎉 Giveaways''', value='''> • `/gstart` ; `/gend` ; `/greroll`.''', inline=False)
    embed.add_field(name='''\🔊 Salons InterServeur''',
                    value='''> • `/hubjoin` `/hubleave` ; `/hublist` ; `/channelblock`.''', inline=False)
    embed.add_field(name='''\⭐ Level System''', value='''> • `/lvlinfos` ; `/rank` ; `/leaderboard`.''', inline=False)
    embed.add_field(name='''\🚔 Modération''',
                    value='''> • `/commandslist` ; `/ban` ; `/unban` ; `/timeout` ; `/warn` ; `/lookup` ; `/unwarn` ; `/untimeout` ; `/lock` ; `/unlock` ; `/clear`.''',
                    inline=False)
    embed.add_field(name='''\🔮 Blacklist''',
                    value='''> • `/explications` ; `/blacklist` ; `/set` ; `/demande` ; `/appel` ; `/infosbl` ; `/scan`.''',
                    inline=False)
    embed.add_field(name='''\🔧 Utilitaire''', value='''> • `/ping` ; `/help` ; `/suggestion` ; `/report`.''',
                    inline=False)
    embed.add_field(name='''\🎶 Music Mode''', value='''> • `/play` ; `/pause` ; `/leave` ; `/join` ; `/repeat`.''',
                    inline=False)
    embed.add_field(name='''\🖼️ Profil''',
                    value='''> • `/create` ; `/modif` ; `/bio` ; `/profil` ; `/addfriends` ; `/acceptfriend`.''',
                    inline=False)
    embed.add_field(name='''<:LogoPaladium:1181337839363948564> PalaGames''',
                    value='''> • `/upvote` ; `/classement` ; `/infos`.''', inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


# ------------------------------------------
# HELP
# ------------------------------------------
# ------------------------------------------
# UPVOTE
# ------------------------------------------

def load_data():
    data = read_file('./data.json') or {}
    return data


def save_data(data):
    write_file('./data.json', data)


# @tasks.loop(hours=24)
# async def remind_votes():
#    data = load_data()
#
#    for user_id, last_vote_time in data.get('votes', {}).items():
#        last_vote_time = datetime.fromisoformat(last_vote_time)
#        elapsed_time = datetime.utcnow() - last_vote_time
#        if elapsed_time >= timedelta(hours=24):
#            user = bot.get_user(int(user_id))
#            if user:
#                await user.send('Hey ! Vous pouvez à nouveau voter pour un serveur ! Utilisez la commande `/upvote`.')

@tree.command(name='upvote', description='Voter pour le serveur sur lequel vous utilisez la commande.')
async def upvote(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    data = load_data()
    user_id = str(author_member.id)
    if 'votes' not in data:
        data['votes'] = {}
    if user_id in data['votes']:
        last_vote_time = datetime.fromisoformat(data['votes'][user_id])
        elapsed_time = datetime.utcnow() - last_vote_time
        if elapsed_time < timedelta(hours=24):
            time_left = timedelta(hours=24) - elapsed_time
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            embed = discord.Embed(color=0X1A1A1A)
            embed.add_field(name='Temps restant avant de pouvoir revoter :',
                            value=f'''> » `{hours}`h `{minutes}`min.''')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    server_id = str(interaction.guild.id)

    if server_id not in data:
        data[server_id] = {'upvotes': 0}

    data[server_id]['upvotes'] += 1
    data['votes'][user_id] = datetime.utcnow().isoformat()
    save_data(data)

    channel_id = 1180905117222961223
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(title=interaction.guild.name,
                              description=f'''{author_member.mention} a voté pour le serveur `{interaction.guild.name}` !''',
                              color=0X1A1A1A)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.add_field(name='Nombre de Votes :', value=data[server_id]['upvotes'], inline=True)

        await channel.send(embed=embed)

    await interaction.response.send_message(
        f'''<:Vote:1181273257849135187> Vous venez de voter pour le serveur : `{interaction.guild.name}` (**{data[server_id]['upvotes']}** Upvotes) !''',
        ephemeral=True)


# ------------------------------------------
# UPVOTE
# ------------------------------------------
# ------------------------------------------
# CLASSEMENT
# ------------------------------------------

@tree.command(name='classement', description='Afficher les 5 serveurs avec le plus de votes.')
async def classement(interaction: discord.Interaction):
    data = load_data()

    sorted_servers = sorted([(server_id, server_data) for server_id, server_data in data.items() if
                             isinstance(server_data, dict) and 'upvotes' in server_data], key=lambda x: x[1]['upvotes'],
                            reverse=True)

    top_servers = sorted_servers[:5]

    embed = discord.Embed(title='Classement des 5 serveurs avec le plus de votes',
                          description='''> » Toi aussi tu peux participer, alors vote maintenant en faisant `/upvote` !
        > » Pour voir un maximum d'information sur un serveur, éxécute la commande `/infos <NOM_DU_SERVEUR_>`''',
                          color=0X1A1A1A)

    for i, (server_id, server_data) in enumerate(top_servers, start=1):
        guild = bot.get_guild(int(server_id))
        embed.add_field(name=f'''#{i} - **{guild.name}**''',
                        value=f'''\⭐ __Votes :__ {server_data['upvotes']}\n\🚩 __Membres :__ {guild.member_count}''',
                        inline=True)

    await interaction.response.send_message(embed=embed)


# ------------------------------------------
# CLASSEMENT
# ------------------------------------------
# ------------------------------------------
# SUGGESTION
# ------------------------------------------

@tree.command(name='suggestion', description='Soumettre une suggestion.')
async def suggestion(interaction: discord.Interaction, texte: str):
    author_member: discord.Member = interaction.user
    channel = bot.get_channel(1180904879045234729)

    view = discord.ui.View()

    button = discord.ui.Button(label="✅ Pour", 
                               style=discord.ButtonStyle.secondary, 
                               custom_id=f"pour")
    view.add_item(button)

    button = discord.ui.Button(label="❌ Contre", 
                               style=discord.ButtonStyle.secondary, 
                               custom_id=f"contre")
    view.add_item(button)

    suggestion_embed = discord.Embed(title='Nouvelle Suggestion', color=0X1A1A1A)

    suggestion_embed.add_field(name='Date', value=datetime.utcnow().strftime('%d %B %Y %H:%M:%S'))
    suggestion_embed.add_field(name='Auteur', value=author_member.mention)
    suggestion_embed.add_field(name='Contenu', value=texte)

    suggestion_message = await channel.send(embed=suggestion_embed)

    await suggestion_message.add_reaction("👍")
    await suggestion_message.add_reaction("👎")

    await interaction.response.send_message('''Votre suggestion a été soumise avec succès!''', ephemeral=True)


# ------------------------------------------
# SUGGESTION
# ------------------------------------------
# ------------------------------------------
# ADMINPING
# ------------------------------------------

@tree.command(name='adminping', description='Voir les latences du bot.')
@discord.app_commands.checks.has_role(1180819110133764147)
async def adminping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds=difference))

    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    headers = {'Authorization': 'Bearer ptlc_iOulNmU5AHYroZh0fmdE8gZMM0sA7OE2tzZY2ayVZhZ'}

    # Get Discord latency
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

    response = requests.get("https://panel.berchbrown.me/api/client/servers/b1545927/resources", headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()['attributes']["resources"]
            ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)
            current_state = response.json()['attributes']["current_state"]

            # Additional resource data
            cpu_absolute = data.get("cpu_absolute", 0)
            disk_bytes = data.get("disk_bytes", 0)
            network_rx_bytes = data.get("network_rx_bytes", 0)
            network_tx_bytes = data.get("network_tx_bytes", 0)
        except json.JSONDecodeError as e:
            print(f"Error decoding server response JSON: {e}")
            ram_used = '''Erreur de décodage de la réponse du serveur JSON'''
            current_state = '''Erreur de décodage de la réponse du serveur JSON'''
    else:
        print(f"Error accessing server resources API. Status code: {response.status_code}")
        ram_used = '''Erreur d'accès aux ressources du serveur API'''
        current_state = '''Erreur d'accès aux ressources du serveur API'''

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

    embed = discord.Embed(title='\🏓 Pong !', color=0X1A1A1A)
    embed.add_field(name='> Latence VPS <:Online:1184534287932989460>',
                    value=f'» `{response.elapsed.total_seconds() * 1000:.2f}ms`', inline=False)
    embed.add_field(name='> LocalHost <:Offline:1184534286364332102>', value=f'» `{current_state}`', inline=False)
    embed.add_field(name='> API <:Online:1184534287932989460>',
                    value=f'» `{response.elapsed.total_seconds() * 100:.2f}ms`', inline=False)
    embed.add_field(name='> Ping Bot <:Online:1184534287932989460>', value=f'» `{round(bot.latency * 1000)}ms`',
                    inline=False)
    embed.add_field(name='> Latence Discord <:Online:1184534287932989460>', value=f'» `{discord_latency}ms`',
                    inline=False)
    embed.add_field(name='> RAM Utilisée <:Online:1184534287932989460>',
                    value=f'» `{ram_used} Mo / {(psutil.virtual_memory().total // (1024 ** 2))} Mo`', inline=False)
    embed.add_field(name='> CPU Absolute Usage <:Online:1184534287932989460>', value=f'» `{cpu_absolute}%`', inline=False)
    embed.add_field(name='> Disk Usage <:Online:1184534287932989460>', value=f'» `{disk_bytes} bytes`', inline=False)
    embed.add_field(name='> Network RX <:Online:1184534287932989460>', value=f'» `{network_rx_bytes} bytes`', inline=False)
    embed.add_field(name='> Network TX <:Online:1184534287932989460>', value=f'» `{network_tx_bytes} bytes`', inline=False)
    embed.add_field(name='> Lancé depuis :', value=f'`{uptime_str}`')

    ping_total = f"{response.elapsed.total_seconds() * 1000 + bot.latency * 1000 + float(discord_latency)}"
    embed.set_footer(text = f'Ping total : {ping_total}ms')

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ------------------------------------------
# ADMINPING
# ------------------------------------------
# ------------------------------------------
# PING
# ------------------------------------------
    
@tree.command(name = 'ping', description = '''Voir toutes les latences concernant le bot.''')
async def ping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds=difference))

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

    response = requests.get("https://panel.berchbrown.me/api/client/servers/b1545927/resources", headers=headers)

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

    embed = discord.Embed(title='\🏓 Pong !', color=0X1A1A1A)
    embed.add_field(name='> Latence VPS <:Online:1184534287932989460>',
                    value=f'» `{response.elapsed.total_seconds() * 1000:.2f}ms`', inline=False)
    
    embed.add_field(name='> LocalHost <:Offline:1184534286364332102>', value='» `Offline`')
    embed.add_field(name='> API <:Online:1184534287932989460>', value=f'» `{response.elapsed.total_seconds() * 100:.2f}ms`')
    embed.add_field(name='> Ping Bot <:Online:1184534287932989460>', value=f'» `{round(bot.latency * 1000)}ms`')
    embed.add_field(name='> Latence Discord <:Online:1184534287932989460>', value=f'» `{discord_latency}ms`')
    embed.add_field(name='> RAM Utilisée <:Online:1184534287932989460>', value=f'» `{ram_used} Mo / {(psutil.virtual_memory().total // (1024 ** 2))} Mo`')
    embed.add_field(name='> Lancé depuis :', value = f'`{uptime_str}`')

    await interaction.response.send_message(embed = embed, ephemeral = True)

# ------------------------------------------
# ADMINPING
# ------------------------------------------
# ------------------------------------------
# REPORT
# ------------------------------------------

@tree.command(name='report', description='Reporter un bug du bot.')
async def report(interaction: discord.Interaction, contenu: str):
    author_member: discord.Member = interaction.user
    channel = bot.get_channel(1180904913321074788)
    embed = discord.Embed(title='Nouveau Bug découvert !', color=0X1A1A1A)

    embed.add_field(name='Date', value=datetime.utcnow().strftime('%d %B %Y %H:%M:%S'))
    embed.add_field(name='Auteur', value=author_member.mention)
    embed.add_field(name='Contenu', value=contenu)

    await channel.send(embed=embed)
    await interaction.response.send_message('''Votre bug a été correctement été report !''', ephemeral=True)


# ------------------------------------------
# REPORT
# ------------------------------------------
# ------------------------------------------
# COMMANDSLIST
# ------------------------------------------
@tree.command(name='commandslist', description='Informations sur les commandes de Modération.')
@app_commands.choices(
    commande=[
        app_commands.Choice(name='''/ban & /unban''', value=1),
        app_commands.Choice(name='''/timeout & /untimout''', value=2),
        app_commands.Choice(name='''/warn & /lookup''', value=3),
        app_commands.Choice(name='''/lock & /unlock''', value=4),
        app_commands.Choice(name='''/clear''', value=5)
    ]
)
async def commandslist(interaction: discord.Interaction, commande: int):
    author_member: discord.Member = interaction.user

    if commande == 1:
        embed1 = discord.Embed(title='/ban & /unban', color=0X1A1A1A)
        embed1.add_field(name='/ban', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/ban [membre] [raison*]`
                        `*` : *Non obligatoire pour éxécuter la commande.*''')
        embed1.add_field(name='/unban', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/unban [id]`''')

        await interaction.response.send_message(embed=embed1, ephemeral=True)

    if commande == 2:
        embed2 = discord.Embed(title='/timeout & /untimout', color=0X1A1A1A)
        embed2.add_field(name='/timeout', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/timeout [membre] [raison*] [days*] [heures*] [minutes*] [secondes*]`
                        `*` : *Non obligatoire pour éxécuter la commande.*''')
        embed2.add_field(name='/untimeout', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/untimeout [membre]`''')

        await interaction.response.send_message(embed=embed2, ephemeral=True)

    if commande == 3:
        embed3 = discord.Embed(title='/warn & /lookup', color=0X1A1A1A)
        embed3.add_field(name='/warn', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `1h`
                        » **Explications** : `/warn [membre] [raison]`''')
        embed3.add_field(name='/lookup', value='''» **Permission** : `MODERATE_MEMBERS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/lookup [id]`''')

        await interaction.response.send_message(embed=embed3, ephemeral=True)

    if commande == 4:
        embed4 = discord.Embed(title='/lock & /unlock', color=0X1A1A1A)
        embed4.add_field(name='/lock', value='''» **Permission** : `MANAGE_CHANNELS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/lock [channel]''')
        embed4.add_field(name='/unlock', value='''» **Permission** : `MANAGE_CHANNELS`
                        » **CoulDown** : `Non`
                        » **Explications** : `/unlock [channel]`''')

        await interaction.response.send_message(embed=embed4, ephemeral=True)

    if commande == 5:
        embed5 = discord.Embed(title='/clear', color=0X1A1A1A)
        embed5.add_field(name='/clear', value='''» **Permission** : `MANAGE_MESSAGES`
                        » **CoulDown** : `10s`
                        » **Explications** : `/clear [nombre_de_message] [raison*]`''')

        await interaction.response.send_message(embed=embed5, ephemeral=True)


# ------------------------------------------
# COMMANDSLIST
# ------------------------------------------
# ------------------------------------------
# BAN
# ------------------------------------------

@tree.command(name='ban', description='Bannir un membre du serveur.')
@app_commands.default_permissions(moderate_members=True)
async def ban(interaction: discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison précisée.'''):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(
            f'''<:Warning:1181322717618765974> Vous ne pouvez pas vous bannir vous - même !''', ephemeral=True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(
            f'''<:Warning:1181322717618765974> Vous ne pouvez pas bannir cette personne car elle est à un rôle supérieur à vous !''',
            ephemeral=True)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(
            f'''<:Warning:1181322717618765974> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !''',
            ephemeral=True)

    try:
        await interaction.guild.ban(membre, reason=reason)
        await interaction.response.send_message(f'{membre.mention} a été banni ! `[{reason}]`', ephemeral=True)

    except:
        return await interaction.response.send_message(
            f'''<:Warning:1181322717618765974> Je n'arrive pas à bannir ce membre !''', ephemeral=False)


# ------------------------------------------
# BAN
# ------------------------------------------
# ------------------------------------------
# LVLINFOS
# ------------------------------------------

@tree.command(name='lvlinfos', description='Afficher les informations sur le Système des Levels.')
async def lvlinfos(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(title='Informations sur le Système de Niveaux',
                          description='''> » `/rank` : Permet d'afficher votre classement, votre niveau et votre nombre d'XP.
                          > » `/leaderboard` : Afficher les 10 premiers interserveur.

                          \📌 **A Noter** : Vous gagnez entre 1 et 10 XP, par minute, peut importe le nombre de messages que vous enverrez. Quand une personne atteint le niveau `50 (max)`, tout repars à 0.''',
                          color=0X1A1A1A)

    await interaction.response.send_message(embed=embed, ephemeral=True)

# ------------------------------------------
# LVLINFOS
# ------------------------------------------
# ------------------------------------------
# GUILDS
# ------------------------------------------

@tree.command(name='guilds', description='Afficher la liste des serveurs sur lesquels se trouvent le bot.')
@discord.app_commands.checks.has_role(1180819110133764147)
async def guildlist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    role = discord.utils.get(author_member.guild.roles, id=1180819110133764147)

    if role in author_member.roles:
        guilds = sorted(interaction.client.guilds, key=lambda guild: guild.member_count, reverse=True)

        messages = []
        current_message = '**Liste des serveurs**\n\n'

        for guild in guilds:
            guild_name = guild.name
            guild_owner = guild.owner.mention
            guild_member_count = str(guild.member_count)

            if len(current_message) + len(guild_name) + len(guild_owner) + len(guild_member_count) + 13 > 2000:
                messages.append(current_message)
                current_message = ''

            current_message += f'» `{guild_name}` ({guild_owner}) (**{guild_member_count}** Membres)\n'

        messages.append(current_message)

        for i, message in enumerate(messages):
            if i == 0:
                await interaction.response.send_message(message, ephemeral=True)
            else:
                await interaction.followup.send(message, ephemeral=True)


# ------------------------------------------
# GUILDS
# ------------------------------------------
# ------------------------------------------
# CLEAR
# ------------------------------------------

@tree.command(name='clear', description='Pour supprimer un nombre X de messages')
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, number: int):
    author_member: discord.Member = interaction.user
    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(limit=number, check=lambda msg: not msg.pinned)

    if number == 1:
        await interaction.followup.send(f'<:Yes:1181323585567080529> **1** message a correctement été effacé !')
    else:
        await interaction.followup.send(
            f'<:Yes:1181323585567080529> **{len(deleted)}** messages on correctement été effacés ! *Les messages épinglés ne sont pas effacés.*')


# ------------------------------------------
# CLEAR
# ------------------------------------------
# ------------------------------------------
# UI (USERINFO)
# ------------------------------------------

@tree.command(name='ui', description='Donne des informations sur un membre du serveur.')
async def userinfo(interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
    if member is None:
        author_member = interaction.user
    else:
        author_member = member

    user_flags = author_member.public_flags

    embed = discord.Embed(title=f'Informations sur {author_member.name}',
                          color=0x1A1A1A)

    embed.add_field(name='''\📌 Informations Générales''',
                    value=f'''> » **Pseudo** : `{author_member.name}#{author_member.discriminator}`
    > » **ID** : `{author_member.id}`.
    > » **Créé le** : <t:{int(author_member.created_at.timestamp())}:D>.
    > » **Badge(s)** : `Indisponible`''', inline=True)

    embed.add_field(name='''\⚡ Informations sur le Serveur''',
                    value=f'''> » **Rôles ({len(author_member.roles) - 1})** : {", ".join([role.mention for role in author_member.roles[1:]]) if len(author_member.roles) > 1 else "Aucun"}
    > » **Rejoint le** : <t:{int(author_member.joined_at.timestamp())}:D>.
    > » **Surnom** : {author_member.nick if author_member.nick else "Aucun"}''', inline=False)

    embed.set_thumbnail(url=author_member.avatar.url)
    if author_member.banner:
        embed.set_image(url=author_member.banner.url)

    await interaction.response.send_message(embed=embed)


# ------------------------------------------
# UI (USERINFO)
# ------------------------------------------
# ------------------------------------------
# WARN
# ------------------------------------------

data_file = './warn.json'


@tree.command(name='warn', description='Avertir un membre du serveur')
@app_commands.default_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, membre: discord.Member,
               reason: str = '''Aucune raison n'a été précisée'''):
    author_member: discord.Member = interaction.user

    guild_id = interaction.guild_id

    warnings = read_file(data_file)

    current_time = int(datetime.utcnow().timestamp())

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
    write_file(data_file, warnings)

    embed = discord.Embed(description=f'''Vous venez d'être warn sur le serveur {interaction.guild.name}''')

    await membre.send(embed=embed)
    await interaction.response.send_message(
        f'<:Yes:1181323585567080529> {membre.mention} a été warn. Pour voir la liste des warns, utilisez `/lookup`',
        ephemeral=True)


# ------------------------------------------
# WARN
# ------------------------------------------
# ------------------------------------------
# LOOKUP
# ------------------------------------------

@tree.command(name='lookup', description='Voir la liste des avertissements de quelqu\'un')
@app_commands.default_permissions(moderate_members=True)
async def lookup(interaction: discord.Interaction, member: discord.Member):
    author_member: discord.Member = interaction.user

    if os.path.exists(data_file):
        warnings = read_file(data_file)
    else:
        warnings = {}

    member_id = str(member.id)

    if member_id in warnings:
        user_warnings = warnings[member_id]

        embed = discord.Embed(title=f'» Avertissements de {member.name}',
                              color=0x1A1A1A)

        for index, warning in enumerate(user_warnings):
            author_id = warning['author_id']
            guild_id = warning['guild_id']
            reason = warning['reason']
            author_name = warning['author_name']
            membre_name = warning['membre_name']
            timestamp = warning.get('timestamp', 'Non disponible')
            guild_name = warning.get('guild_name', 'Non disponible')

            field_name = f'<:SlashCommand:1181323583281188994> **`#{index + 1} `**'
            field_value = f'''> » **Modérateur** : <@{author_id}> (`{author_id}`)
            > » **Raison** : `{reason}` <t:{timestamp}>
            > » **Serveur** : `{guild_name}`'''
            embed.add_field(name=field_name, value=field_value, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f'Aucun avertissement trouvé pour `{member_id}`.', ephemeral=True)


# ------------------------------------------
# LOOKUP
# ------------------------------------------
# ------------------------------------------
# UNWARN
# ------------------------------------------

@tree.command(name='unwarn', description='Retirer un avertissement à un membre')
@app_commands.default_permissions(moderate_members=True)
async def unwarn(interaction: discord.Interaction, member: discord.Member):
    author_member: discord.Member = interaction.user

    if os.path.exists(data_file):
        warnings = read_file(data_file)
    else:
        warnings = {}

    author_id = str(author_member.id)
    member_id = str(member.id)

    if member_id in warnings and any(warning['author_id'] == author_id for warning in warnings[member_id]):
        warnings[member_id] = [warning for warning in warnings[member_id] if warning['author_id'] != author_id]
        write_file(data_file, warnings)
        await interaction.response.send_message(f'<:Yes:1181323585567080529> Avertissement retiré à {member.mention}.',
                                                ephemeral=True)
    else:
        await interaction.response.send_message(f'Aucun avertissement trouvé pour {member.mention} émis par vous.',
                                                ephemeral=True)


# ------------------------------------------
# UNWARN
# ------------------------------------------
# ------------------------------------------
# GSTART
# ------------------------------------------

def load_giveaways():
    return read_file('./giveaways_data.json')


def save_giveaways(giveaways):
    write_file('./giveaways_data.json', giveaways)


@tree.command(name='gstart', description='Lancer un giveaway sur le serveur.')
@app_commands.default_permissions(administrator=True)
async def gstart(interaction: discord.Interaction, duration: str, winners: int, prize: str):
    duration_seconds = parse_duration(duration)
    author_member: discord.Member = interaction.user
    if duration_seconds is None:
        await interaction.response.send_message('Format de durée invalide.', ephemeral=True)
        return

    end_timestamp_utc = int((datetime.utcnow() + timedelta(seconds=duration_seconds)).timestamp()) + 3600
    duration_str = f'<t:{end_timestamp_utc}:R>'

    g_embed = discord.Embed(description=f'''> **Tirage** : {duration_str}
> **Nombre de gagnant(s)** : `{winners} Gagnants` *Peut être vous ?*

»  Cliquez sur la réaction <a:Gift:1183055072293302373>  pour participer !''',
                            color=0XF2BB27)
    g_embed.add_field(name='\🎉 Lot', value=f'''```yaml
⟫  {prize}  ⟪
```''')
    g_embed.set_image(
        url='https://cdn.discordapp.com/attachments/1181292316892348429/1183063284484669459/Frame_10.png?ex=6586f88b&is=6574838b&hm=53a763a6563b4523d4357c2bd0a8c0fc9e08a58b8966e2acd3e56cfca5525cd9&')

    giveaway_embed = discord.Embed(title=f'🎉 Giveaway : {prize}',
                                   description=f'''Cliquez sur la réaction 🎉 pour participer!\nDurée : {duration}''',
                                   color=0XFFFFFF)

    giveaway_message = await interaction.channel.send(f'''<a:Gift:1183055072293302373> **Nouveau Giveaway !**''',
                                                      embed=g_embed)
    await giveaway_message.add_reaction('<a:Gift:1183055072293302373>')

    channel_c = interaction.channel
    await interaction.response.send_message(f'Giveaway créé {interaction.channel.mention} !', ephemeral=True)

    giveaways = load_giveaways()
    giveaways[giveaway_message.id] = {
        'channel_id': interaction.channel.id,
        'author_id': author_member.id,
        'end_timestamp': end_timestamp_utc,
        'winners': winners,
        'prize': prize
    }
    save_giveaways(giveaways)


def format_duration(seconds):
    if seconds >= 86400:
        return f'{seconds // 86400} jour(s)'
    elif seconds >= 3600:
        return f'{seconds // 3600} heure(s)'
    elif seconds >= 60:
        return f'{seconds // 60} minute(s)'
    else:
        return f'{seconds} seconde(s)'


@tasks.loop(seconds=5)
async def check_giveaways():
    giveaways = load_giveaways()

    current_timestamp = int(datetime.utcnow().timestamp())
    expired_giveaways = [giveaway_id for giveaway_id, data in giveaways.items() if
                         data['end_timestamp'] <= current_timestamp]

    for giveaway_id in expired_giveaways:
        giveaway_data = giveaways.pop(giveaway_id)
        save_giveaways(giveaways)

        channel = bot.get_channel(giveaway_data['channel_id'])
        author = await bot.fetch_user(giveaway_data['author_id'])
        winners = await select_giveaway_winners(channel, giveaway_data['winners'])

        winners_text = ', '.join(winner.mention for winner in winners)

        for winner in winners:
            embed_w = discord.Embed(title='Nous avons un gagnant !',
                                    description=f'''> » Félicitations {winners_text} ! 
                                      > Vous avez remporté le giveaway de {author.mention}.

                                      > **Lot** : {giveaway_data['prize']}''',
                                    color=0XF2BB27)

            await channel.send(f'''||{author.mention} / {winners_text}||''', embed=embed_w)

            embed_win = discord.Embed(title='Tu as gagné un giveaway !',
                                      description=f'''> » Félicitations ! Vous avez remporté le giveaway de {author.mention}.

> **Lot** : {giveaway_data['prize']}''',
                                      color=0XF2BB27)

            await winner.send(f'''{winner.mention}''', embed=embed_win)


def calculate_end_timestamp(start_timestamp, duration_seconds):
    end_timestamp = start_timestamp + duration_seconds
    return end_timestamp

async def select_giveaway_winners(channel, num_winners):
    participants = [member for member in channel.members if not member.bot]
    winners = random.sample(participants, min(num_winners, len(participants)))
    return winners

def parse_duration(duration):
    if duration.endswith("s") and duration[:-1].isdigit():
        return int(duration[:-1])
    elif duration.endswith("m") and duration[:-1].isdigit():
        return int(duration[:-1]) * 60
    elif duration.endswith("d") and duration[:-1].isdigit():
        return int(duration[:-1]) * 86400
    else:
        return None


# ------------------------------------------
# GSTART
# ------------------------------------------
# ------------------------------------------
# GREROLL
# ------------------------------------------

@tree.command(name='greroll', description='Retenter le tirage au sort pour un giveaway spécifique.')
async def greroll(interaction: discord.Interaction, giveaway_id: int):
    giveaways = load_giveaways()
    if giveaway_id not in giveaways:
        await interaction.response.send_message('ID de giveaway invalide.', ephemeral=True)
        return

    giveaway_data = giveaways[giveaway_id]

    current_timestamp = int(datetime.utcnow().timestamp())
    if giveaway_data['end_timestamp'] > current_timestamp:
        await interaction.response.send_message('Le giveaway spécifié n\'est pas encore terminé.', ephemeral=True)
        return

    old_winners = await select_giveaway_winners(interaction.channel, giveaway_data['winners'])

    try:
        old_message = await interaction.channel.fetch_message(giveaway_id)
        await old_message.delete()
    except discord.NotFound:
        pass

    new_winners = await select_giveaway_winners(interaction.channel, giveaway_data['winners'])
    winners_text = ', '.join(winner.mention for winner in new_winners)

    for winner in new_winners:
        embed = discord.Embed(title='Nouveau tirage au sort !',
                              description=f'Félicitations {winners_text} ! Vous avez remporté le giveaway de {interaction.author.mention}.\nLot : {giveaway_data["prize"]}',
                              color=0XF2BB27)
        await interaction.channel.send(f'||{interaction.author.mention} / {winners_text}||', embed=embed)

        embed_win = discord.Embed(title='Tu as gagné un giveaway !',
                                  description=f'Félicitations ! Vous avez remporté le giveaway de {interaction.author.mention}.\nLot : {giveaway_data["prize"]}',
                                  color=0XF2BB27)
        await winner.send(f'{winner.mention}', embed=embed_win)

    await interaction.response.send_message(
        f'Nouveau tirage au sort effectué pour le giveaway avec l\'ID {giveaway_id}.', ephemeral=True)


# ------------------------------------------
# GREROLL
# ------------------------------------------
# ------------------------------------------
# TIMOUT
# ------------------------------------------

@tree.command(name='timeout', description='Exclure temporairement un membre du serveur')
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, membre: discord.Member,
                  reason: str = '''Aucune raison n'a été précisée''', days: int = 0, hours: int = 0, minutes: int = 0,
                  seconds: int = 0):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(
            f'<:Warning:1181322717618765974> Vous ne pouvez pas vous exclure temporairement vous - même !',
            ephemeral=True)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(
            f'<:Warning:1181322717618765974> Vous ne pouvez pas exclure temporairement cette personne car elle est à un rôle supérieur à vous !',
            ephemeral=True)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(
            f'<:Warning:1181322717618765974> Cette personne est un Modérateur du serveur, je ne peux pas faire cela !',
            ephemeral=True)

    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if duration >= timedelta(days=28):
        return await interaction.response.send_message(
            f'<:Warning:1181322717618765974> La durée d\'exclusion doit être inférieure à `28` jours !', ephemeral=True)

    await membre.timeout(duration, reason=reason)

    await interaction.response.send_message(
        f'<:Yes:1181323585567080529> {membre.mention} a été temporairement exclu ({duration}) !', ephemeral=True)


# ------------------------------------------
# TIMEOUT
# ------------------------------------------
# ------------------------------------------
# UNBAN
# ------------------------------------------

@tree.command(name='unban', description='''Débannir un utilisateur du serveur''')
@app_commands.default_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, membre: discord.User):
    author_member: discord.Member = interaction.user

    try:
        await interaction.guild.unban(membre)
        await interaction.response.send_message(f'<:Yes:1181323585567080529>  {membre} a été débanni !**',
                                                ephemeral=True)
    except:
        await interaction.response.send_message(
            f'''<:Warning:1181322717618765974> Cet utilisateur n'est pas banni !**''', ephemeral=True)


# ------------------------------------------
# UNBAN
# ------------------------------------------
# ------------------------------------------
# HUBJOIN
# ------------------------------------------

@tree.command(name='hubjoin', description='Ajouter le salon actuel au hub.')
@app_commands.default_permissions(administrator=True)
async def hubjoin(interaction: discord.Interaction):
    salon_id = interaction.channel.id
    guild_name = interaction.guild.name
    channel = interaction.channel
    salons_data = read_file('./salons.json')

    if salon_id not in salons_data["salons_ids"]:
        salons_data["salons_ids"].append(salon_id)

        write_file('./salons.json', salons_data)

        embed = discord.Embed(description=f'`{guild_name}` a rejoint le Hub !',
                              color=0X1A1A1A)
        await channel.send(embed=embed)

        for salon_id in salons_data["salons_ids"]:
            if salon_id != interaction.channel.id:
                salon = bot.get_channel(salon_id)

                if salon:
                    await interaction.response.send_message(
                        f'''Ce channel {interaction.channel.mention} rejoint le Hub''', ephemeral=True)
                    await salon.send(f"`{guild_name}` a rejoint le Hub : {interaction.channel.mention}")

    else:
        await interaction.response.send_message(
            'Le salon est déjà dans le hub. Si vous pensez qu\'il s\'agit d\'une erreur, veuillez contacter le support.',
            ephemeral=True)


# ------------------------------------------
# HUBJOIN
# ------------------------------------------
# ------------------------------------------
# HUBLEAVE
# ------------------------------------------

@tree.command(name='hubleave', description='Retirer le salon actuel du hub.')
@app_commands.default_permissions(administrator=True)
async def hubleave(interaction: discord.Interaction):
    salon_id = interaction.channel.id
    channel = interaction.channel

    salons_data = read_file('./salons.json')

    if salon_id in salons_data["salons_ids"]:
        salons_data["salons_ids"].remove(salon_id)

        write_file('./salons.json', salons_data)

        await interaction.response.send_message(f'Salon retiré du hub : {interaction.channel.mention}', ephemeral=True)

        embed = discord.Embed(description=f'`{interaction.guild.name}` a quitté le Hub.',
                              color=0X1A1A1A)

        await channel.send(embed=embed)
    else:
        await interaction.response.send_message(
            'Le salon n\'est pas dans le hub. Si vous pensez qu\'il s\'agit d\'une erreur, veuillez contacter le support.',
            ephemeral=True)


# ------------------------------------------
# HUBLEAVE
# ------------------------------------------
# ------------------------------------------
# HUBLIST
# ------------------------------------------

@tree.command(name='hublist', description='Afficher la liste des serveurs dans le hub.')
async def hublist(interaction: discord.Interaction):
    salons_data = read_file('./salons.json')

    if salons_data["salons_ids"]:
        server_list = "\n".join([f'\- `{guild_name}` <#{salon_id}> (`{salon_id}`)' for guild_id, guild_name, salon_id in
                                 get_guild_info(salons_data)])
        await interaction.response.send_message(f'> » **Liste des serveurs dans le hub** :\n{server_list}',
                                                ephemeral=True)
    else:
        await interaction.response.send_message('La liste des serveurs dans le hub est vide.', ephemeral=True)


def get_guild_info(salons_data):
    guild_info = []
    for salon_id in salons_data["salons_ids"]:
        salon = bot.get_channel(salon_id)
        if salon:
            guild_info.append((salon.guild.id, salon.guild.name, salon_id))
    return guild_info


# ------------------------------------------
# HUBLIST
# ------------------------------------------
# ------------------------------------------
# GI (GuildInformations)
# ------------------------------------------

@tree.command(name='gi', description='''Liste les informations d'un serveur.''')
async def gi(interaction: discord.Interaction):
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

    embed = discord.Embed(title='\📜 Informations du serveur.',
                          description=f'''> » Salons Textuels : `{text_channels}` ; Salons Vocaux : `{voice_channels}` ; Fils : `{threads}` ; Rôles : `{num_roles}`''',
                          color=0XF2BB27)

    embed.add_field(name='» Propriétaire', value=f'''{guild.owner.mention} ||{guild.owner.id}||''', inline=False)
    embed.add_field(name='» Membres', value=member_count, inline=True)
    embed.add_field(name='» Boosts', value=f"{boost_count} boost(s) (Palier {boost_level})", inline=True)
    embed.add_field(name='» Niveau de Verif\'', value=verification_level, inline=True)

    if num_roles > 20:
        role_mentions = [role.mention for role in roles]
        role_mentions.append("...")
    else:
        role_mentions = [role.mention for role in roles]

    embed.add_field(name='» Rôles', value=" ; ".join(role_mentions), inline=False)
    embed.add_field(name='» Online', value=online_count, inline=True)
    embed.add_field(name='» Offline', value=offline_count, inline=True)
    embed.add_field(name='» Ne pas Déranger', value=dnd_count, inline=True)
    embed.add_field(name=f'» Emojis ({num_emojis})', value=f"{emojis_str}", inline=False)
    embed.add_field(name="» Date de création", value=f'<t:{int(datetime.timestamp(guild.created_at))}:D>', inline=False)
    embed.add_field(name="» Rejoint le", value=f'<t:{int(guild.me.joined_at.timestamp())}:D>', inline=False)

    embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text='© 2023 NoodleBot - Tous droits réservés',
                     icon_url='https://cdn.discordapp.com/attachments/1181292316892348429/1185550326435168387/Logo.png?ex=659004c8&is=657d8fc8&hm=775192a0643471eadf11a46abac72f9ae75264d28a95a70e0e10c7a3683d7429&')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed=embed, ephemeral=True)


# ------------------------------------------
# GI (GuildInformations)
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME MUSIC                                                                #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------
# JOIN
# ------------------------------------------

@tree.command(name='join', description='Rejoindre le salon vocal de l\'utilisateur.')
async def join(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    if author_member.voice is None or author_member.voice.channel is None:
        await interaction.response.send_message('Veuillez rejoindre un salon vocal avant d\'utiliser cette commande.',
                                                ephemeral=True)
        return

    voice_channel = author_member.voice.channel
    try:
        voice_client = await voice_channel.connect()
        await interaction.response.send_message(f'Connecté au salon vocal : {voice_channel.mention}.', ephemeral=True)
    except discord.ClientException:
        await interaction.response.send_message('Le bot est déjà connecté à un salon vocal.', ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message('''Je n'ai pas la permission de rejoindre votre salon vocal.''',
                                                ephemeral=True)
    except Exception as e:
        await interaction.response.send_message('Une erreur est survenue lors de la connexion au salon vocal.',
                                                ephemeral=True)


# ------------------------------------------
# JOIN
# ------------------------------------------
# ------------------------------------------
# LEAVE
# ------------------------------------------

@tree.command(name='leave', description='Quitter le salon vocal.')
async def leave(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    voice_client = discord.utils.get(interaction.client.voice_clients, guild=interaction.guild)

    if voice_client is None:
        await interaction.response.send_message('Le bot n\'est pas connecté à un salon vocal.', ephemeral=True)
        return

    voice_channel = author_member.voice.channel

    if voice_client.channel != voice_channel:
        await interaction.response.send_message('Le bot n\'est pas dans le même salon vocal que vous.', ephemeral=True)
        return

    try:
        await voice_client.disconnect()
        await interaction.response.send_message(f'Déconnecté du salon vocal : {voice_channel.mention}.', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message('Une erreur est survenue lors de la déconnexion du salon vocal.',
                                                ephemeral=True)


# ------------------------------------------
# LEAVE
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME MUSIC                                                                #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME PROFILS                                                              #
# ------------------------------------------------------------------------------------------------------------------------------ #

profiles_file = './profiles.json'


def load_profiles():
    return read_file(profiles_file)


def save_profiles(profiles):
    write_file(profiles_file, profiles)

# ------------------------------------------
# CREATE
# ------------------------------------------

@tree.command(name='create', description='Créer un profil personnalisé.')
async def create(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    profiles = load_profiles()
    author_id = str(author_member.id)

    if author_id in profiles:
        await interaction.response.send_message(
            'Vous avez déjà un profil. Si vous souhaitez le supprimer, utilisez `/profildelete`.', ephemeral=True)
        return

    await interaction.response.send_message(f'Regarde tes MP !', ephemeral=True)

    questions = [
        "Quel est ton prénom ?",
        "Quel est ton sexe ?",
        "Quel est ton pays ?",
        "Quel est ton âge ?",
        "Donne-moi une qualité que tu apprécies chez toi.",
        "Quelles sont tes passions ?",
        "Quel est ton/ses life goal(s) ?",
        "Quels jeux vidéo aimes-tu ?",
        "Quels réseaux sociaux utilises-tu ?",
        "Raconte-nous un peu de toi en quelques phrases (biographie)."
    ]

    answers = []

    for question in questions:
        await interaction.user.send(question)
        response = await bot.wait_for('message', check=lambda m: m.author == author_member, timeout=600)
        answers.append(response.content)

    profile = {
        'ID': author_member.id,
        'Username': author_member.name,
        'Avatar': author_member.avatar.url,
        'Prénom': answers[0],
        'Sexe': answers[1],
        'Pays': answers[2],
        'Age': answers[3],
        'Qualité': answers[4],
        'Passions': answers[5],
        'Life Goals': answers[6],
        'Jeux vidéo': answers[7],
        'Réseaux sociaux': answers[8],
        'Biographie': answers[9],
        'Amis': 0,
        "FriendList": [],
        "ColorProfil": 0X1A1A1A
    }

    profiles[author_id] = profile
    save_profiles(profiles)

    confirmation_embed = discord.Embed(title='Profil créé avec succès !', color=0x1A1A1A)
    confirmation_embed.set_author(name=author_member.name, icon_url=author_member.avatar.url)
    await author_member.send(embed=confirmation_embed)


# ------------------------------------------
# CREATE
# ------------------------------------------
# ------------------------------------------
# PROFIL
# ------------------------------------------

@tree.command(name='profil', description='Afficher un profil')
async def profile(interaction: discord.Interaction, personne: str = None):
    author_member: discord.Member = interaction.user
    profiles = load_profiles()

    if personne is None:
        personne = author_member
    elif isinstance(personne, str):
        personne = discord.utils.get(interaction.guild.members, name=personne)

    if personne:
        found = False
        for user_id, profile in profiles.items():
            if personne.id == int(user_id) or personne.name.lower() == profile['Prénom'].lower():
                found = True
                embed = discord.Embed(description=f'''• **Identité**
>  ›  **Prénom** : `{profile['Prénom']}` ({profile['Sexe']})
>  ›  **Pays** : `{profile['Pays']}`
>  ›  **Age** : `{profile['Age']}`

• **Personnalité**
>  ›  **Qualité(s)** : `{profile['Qualité']}`
>  ›  **Passions** : `{profile['Passions']}`
>  ›  **Life Goal(s)** : `{profile['Life Goals']}`

• **Divers**
>  ›  **Jeux** : `{profile['Jeux vidéo']}`
>  ›  **Réseaux** : `{profile['Réseaux sociaux']}`

**Amis** `❤️` : `{profile['Amis']}`''',
                                      color=0x1A1A1A)

                embed.add_field(name='Biographie', value=f'''```
{profile['Biographie']}
```''')
                embed.set_thumbnail(url=profile['Avatar'])
                embed.set_image(
                    url='https://cdn.discordapp.com/attachments/1181292316892348429/1182987085083312148/Frame_10.png?ex=6586b193&is=65743c93&hm=3d451cb48e7823a46ff4e9b517b1f23f8fa49d310a1db90d4f4a8ad4a5fe89c4&')

                await interaction.response.send_message(embed=embed, ephemeral=True)

        if not found:
            await interaction.response.send_message('Profil introuvable.', ephemeral=True)
    else:
        if str(author_member.id) in profiles:
            own_profile = profiles[str(author_member.id)]
        else:
            await interaction.response.send_message(
                '''Vous n'avez pas de profil. Utilisez `/create` pour en créer un.''', ephemeral=True)


# ------------------------------------------
# PROFIL
# ------------------------------------------
# ------------------------------------------
# BIOGRAPHIE
# ------------------------------------------

@tree.command(name='biographie', description='Modifier sa biographie.')
async def biographie(interaction: discord.Interaction, biographie: str):
    author_member: discord.Member = interaction.user
    user_id = str(author_member.id)
    profiles = load_profiles()

    if user_id in profiles:
        profiles[user_id]['Biographie'] = biographie
        save_profiles(profiles)
        await interaction.response.send_message('Biographie mise à jour. Utilisez `/profil` pour voir votre profil.',
                                                ephemeral=True)
    else:
        await interaction.response.send_message('''Vous n'avez pas de profil. Utilisez `/create` pour en créer un.''',
                                                ephemeral=True)


# ------------------------------------------
# BIOGRAPHIE
# ------------------------------------------
# ------------------------------------------
# ADD FRIEND
# ------------------------------------------

@tree.command(name='addfriend', description='Envoyer une demande d\'ami')
async def add_friend(interaction: discord.Interaction, pseudo: discord.Member):
    author_member: discord.Member = interaction.user
    user_id = str(author_member.id)
    profiles = load_profiles()
    found = False

    friend_requests = load_friend_requests()

    existing_request = next((request for request in friend_requests if
                             request["sender"] == author_member.id and request["receiver"] == pseudo.id), None)

    if existing_request:
        await interaction.response.send_message('''Vous avez déjà envoyé une demande d'ami à cette personne.''',
                                                ephemeral=True)
        return

    for friend_id, profile in profiles.items():
        if pseudo.id == int(friend_id):
            found = True
            if user_id != friend_id and user_id not in profile['Amis']:
                add_friend_request(author_member.id, pseudo.id)

                embed = discord.Embed(
                    description=f'''{author_member.mention} vous a envoyé une demande d'ami. Pour l'accepter, faites `/acceptfriend {author_member.id}`''')
                await pseudo.send(embed=embed)
                await interaction.response.send_message(
                    "Demande d'ami envoyée avec succès. Attendez que l'autre personne accepte.", ephemeral=True)
            elif user_id == friend_id:
                await interaction.response.send_message("Vous ne pouvez pas vous ajouter en ami.", ephemeral=True)
            elif user_id in profile['Amis']:
                await interaction.response.send_message("Vous êtes déjà ami avec cette personne.", ephemeral=True)

    if not found:
        embed1 = discord.Embed(title='''Nouvelle demande d'amis !''',
                               description=f'''> **Vous venez de recevoir une demande d'amis de {author_member.mention} !**

Mais vous n'avez pas de profil créé avec le bot. 
\- Faites `/create` ;
\- Et sur un serveur en commun avec **{author_member.name}**,
> Exécutez la commande `/acceptfriend <@{author_member}>` (Il faut mentionner)''',
                               color=0X1A1A1A)
        await pseudo.send(embed=embed1)
        await interaction.response.send_message("Profil introuvable. *Demande de création de profil envoyée*",
                                                ephemeral=True)


def add_friend_request(sender_id, receiver_id):
    friend_requests = load_friend_requests()

    if not isinstance(friend_requests, list):
        friend_requests = []

    friend_requests.append({"sender": sender_id, "receiver": receiver_id})
    save_friend_requests(friend_requests)


def load_friend_requests():
    read_file('./friendadd.json')


def save_friend_requests(friend_requests):
    write_file(r'./friendadd.json', friend_requests)


# ------------------------------------------
# ADD FRIEND
# ------------------------------------------
# ------------------------------------------
# ACCEPT FRIEND
# ------------------------------------------

@tree.command(name='acceptfriend', description='Accepter une demande d\'ami.')
async def accept_friend(interaction: discord.Interaction, personne: discord.Member):
    author_member: discord.Member = interaction.user
    profiles = load_profiles()

    friend_requests = load_friend_requests()

    matching_request = next((request for request in friend_requests if request["receiver"] == author_member.id), None)

    if matching_request:
        sender_profile = profiles.get(str(matching_request["sender"]))

        if sender_profile:
            profiles[str(author_member.id)]['FriendList'].append(sender_profile['ID'])
            profiles[str(author_member.id)]['Amis'] += 1

            profiles[str(matching_request["sender"])]['FriendList'].append(author_member.id)
            profiles[str(matching_request["sender"])]['Amis'] += 1

            save_profiles(profiles)

            friend_requests.remove(matching_request)
            save_friend_requests(friend_requests)

            await interaction.response.send_message(
                f'{sender_profile["Username"]} a été ajouté à votre liste d\'amis !', ephemeral=True)
            await personne.send(f'Vous êtes maintenant amis avec {author_member.mention} !')
        else:
            await interaction.response.send_message('Profil de l\'expéditeur introuvable.', ephemeral=True)
    else:
        await interaction.response.send_message('Aucune demande d\'ami correspondante trouvée.', ephemeral=True)


# ------------------------------------------
# ACCEPT FRIEND
# ------------------------------------------
# ------------------------------------------
# MODIF
# ------------------------------------------

class modal_modif(ui.Modal, title="Modification de mon profil"):
    pseudo = ui.TextInput(label="Couleur de l'embed", style=discord.TextStyle.short, placeholder="0XFFFFFF",
                          required=False, max_length=8)
    item = ui.TextInput(label="Prénom / Pseudo", style=discord.TextStyle.paragraph, placeholder="Dupont",
                        required=False, max_length=32)
    price = ui.TextInput(label="Âge", style=discord.TextStyle.short, placeholder="17 ans", required=False,
                         max_length=8)
    social = ui.TextInput(label="Mes réseaux", style=discord.TextStyle.short, placeholder="Instagram : ...",
                          required=False,
                          max_length=1024)
    passions = ui.TextInput(label="Passions", style=discord.TextStyle.short, placeholder="Musique, Soirées...",
                            required=False,
                            max_length=1024)


@tree.command(name='modif', description='Modifier le profil')
async def modify_profile(interaction: discord.Interaction):
    await interaction.response.send_modal(modal_modif())


# ------------------------------------------
# MODIF
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME PROFILS                                                              #
# ------------------------------------------------------------------------------------------------------------------------------ #
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
            await message.channel.send(
                f'''<:discotoolsxyzicon14:1183473589442318386>  **Bravo {author_mention}, tu viens de passer un niveau !** (Level **{level}**)''')

        # Partie InterServ
        class view_guildbutton(discord.ui.View):
            def __init__(self, server_name):
                super().__init__()
                self.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label=server_name,
                                                disabled=True))

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


# RANK

experience_ref = {0: 100, 1: 155, 2: 220}
lniv, l_add_exp = 3, 75
max_lvl = 50

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
    with open('./levels.json', 'r') as f:
        levels = json.load(f)
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
    with open('./levels.json', 'r') as f:
        levels = json.load(f)
    if not str(member.id) in levels:
        levels[str(member.id)] = {}
        levels[str(member.id)]['experience'] = 0
        levels[str(member.id)]['last_gain'] = 0
    level_before = get_level(levels[str(member.id)]['experience'], 1)
    if time.time() - levels[str(member.id)]['last_gain'] > 60:
        exp_gained = random.randint(13, 17)
        levels[str(member.id)]['experience'] += exp_gained
        levels[str(member.id)]['last_gain'] = time.time()
    level_after = get_level(levels[str(member.id)]['experience'], 1)
    with open('./levels.json', "w") as f:
        json.dump(levels, f, indent=2)
    if level_after > level_before:
        return "level_gained"
    return "success"

def manage_levels_xp(member, type, method, quantity):
    with open('./levels.json', 'r') as f:
        levels = json.load(f)
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
    with open('./levels.json', 'w') as f:
        json.dump(levels, f, indent=2)

# Couleur
fill = 31, 65, 207

# 800 x 235

@bot.event
async def on_message(message):
    if not message.author.bot:
        response = manage_exp_event(message.author)
        with open('./levels.json', 'r') as f:
            levels = json.load(f)
        level = get_level(levels[str(message.author.id)]['experience'])
        author_name = message.author.mention
        if response == "level_gained":
            await message.channel.send(f"<:Lvlflche:1239638668746948719> **Félicitations {author_name}, tu viens d'atteindre le niveau **{level}** !**")

@tree.command(name = "rank", description = "Permet de voir votre niveau.")
async def rank(interaction: Interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user
    with open('./levels.json', 'r') as f:
        levels = json.load(f)
    if str(user.id) not in levels:
        return await interaction.response.send_message('Vous n\'avez pas encore envoyé de messages !', ephemeral=True)
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
    mask = mask.resize(pfp.size, Image.LANCZOS)

    card.paste(pfp, (32, 42), mask)

    fnt = ImageFont.truetype('Montserrat.ttf', 35)
    fnt2 = ImageFont.truetype('Montserrat.ttf', 45)
    fnt3 = ImageFont.truetype('Montserrat.ttf', 25)

    def get_text_size(text, font):
        return draw_.textbbox((0, 0), text, font=font)[2:]

    draw_ = ImageDraw.Draw(card, "RGBA")

    m1 = f'#{rank}'
    w1, h1 = get_text_size(m1, fnt2)
    m2 = f'RANK'
    w2, h2 = get_text_size(m2, fnt3)
    m3 = f'LEVEL'
    w3, h3 = get_text_size(m3, fnt3)
    m4 = f'{level}'
    w4, h4 = get_text_size(m4, fnt2)
    m5 = f'{experience_str}/{max_xp_str} XP'
    w5, h5 = get_text_size(m5, fnt3)
    m6 = user.name
    w6, h6 = get_text_size(m6, fnt)
    if w6 < 430:
        draw_.text((210, 145 - h6), user.name, font=fnt, fill="white")
    else:
        draw_.text((210, 145 - h6), user.name, font=ImageFont.truetype('Montserrat.ttf', 20), fill="white")
    draw_.text((800 - w5 - 35, 125), m5, font=fnt3, fill="white")
    draw_.text((800 - w3 - w4 - 55, 45), m3, font=fnt3, fill=(fill))
    draw_.text((800 - w4 - 40, 30), m4, font=fnt2, fill=(fill))
    draw_.text((800 - (w3 + w4 + 85) - w1 - w2, 45), m2, font=fnt3, fill="white")
    draw_.text((800 - w1 - w3 - w4 - 70, 30), m1, font=fnt2, fill="white")

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

    embed = discord.Embed(title=f'''Classement d'XP''',
                          description=f'''> » Voici les dix premiers participants inter-serveurs.\n\n {str_leaderboard}\n\n**Mon classement**\n> Vous êtes classé à la `{a_rank}e` place, parmis `{total_users}` participants !''',
                          color=0xFFFFFF)

    embed.set_image(
        url='https://cdn.discordapp.com/attachments/1180904738078863431/1182549075439145021/Rank.png?ex=658519a6&is=6572a4a6&hm=d3e0999f1399020590128f870fec28098bd810684c1f3ba1fdbfe450a3d27761&')
    await interaction.response.send_message(embed=embed)


# ------------------------------------------
# LEADERBOARD
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME LEVELLING                                                            #
# ------------------------------------------------------------------------------------------------------------------------------ #

bot.run('TOKEN')