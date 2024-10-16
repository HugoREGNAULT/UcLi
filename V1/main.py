import discord, asyncio, json, re, time, random, requests, typing, json, os, uuid, psutil, datetime
import warnings
import matplotlib.pyplot as plt
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=DeprecationWarning)

from discord import ui, app_commands, Interaction, SelectOption
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord.utils import get
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ------------------------------------------
# CONFIGURATIONS ET INFORMATIONS GLOBALES
# ------------------------------------------

load_dotenv()

def read_file(file):
    with open(file, "r") as f:
        return json.load(f)

def write_file(file, var):
    with open(file, 'w') as f:
        json.dump(var, f, indent = 2)

GUILD_ID = 1135594237040263168

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

TOKEN = ('TOKEN')

bot = commands.Bot(command_prefix = '/', intents = intents)
bot.remove_command('help')


class client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            bio.start()
            global startTime 
            startTime = time.time()
#            stats_channels.start()
#           self.add_view(mainBlacklist())
        print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️     │
    │                                             │
    │  {self.user} is  Online ==> ✔️        │
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

# ------------------------------------------
# BIO CHANGEANTE DU BOT
# ------------------------------------------

@tasks.loop(seconds = 4)
async def bio():
    await bot.wait_until_ready()
    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
    status = [f'{str(len(bot.guilds))}/75 Serveurs', 'Préfix : /', f'{total_members} Utilisateurs', f'V0.0.1', f'/help']
    for i in status:
        await bot.change_presence(activity = discord.Game(str(i)))
        users_voc_channel = bot.get_channel(1147188360847294504)
        await users_voc_channel.edit(name="👤︲Users : " + f'{total_members}')
        guild_voc_channel = bot.get_channel(1147188514677596250)
        await guild_voc_channel.edit(name="📻︲Guilds : " + f'{len(bot.guilds)}')
        await asyncio.sleep(4)

# ------------------------------------------
# BIO CHANGEANTE DU BOT
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
    streaming_count = sum(activity.type == discord.ActivityType.streaming for member in guild.members for activity in member.activities)
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
                          color = 0xEBB70E)

    embed.set_author(name = f'Nouveau Serveur !', icon_url = f'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.timestamp = datetime.utcnow()

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

    channel = bot.get_channel(1147185320840921088)
    await channel.send(embed = embed)
    channel_admin = bot.get_channel(1147185320840921088)
    await channel_admin.send(invite)

# ------------------------------------------
# on_guild_join
# ------------------------------------------
# ------------------------------------------
# stats_channels
# ------------------------------------------

#@tasks.loop(seconds = 300)
#async def stats_channels():
#    for guild in bot.guilds:
#        total_members = total_members + guild.member_count
#
#        users_voc_channel = bot.get_channel(1147188360847294504)
#        guild_voc_channel = bot.get_channel(1147188514677596250)
#
#        await users_voc_channel.edit(name="👤︲Users : " + f'{total_members}')
#        guild_voc_channel = bot.get_channel(1147188514677596250)
#        await guild_voc_channel.edit(name="📻︲Guilds : " + f'{len(bot.guilds)}')


# ------------------------------------------
# stats_channels
# ------------------------------------------
# ------------------------------------------
# HELP
# ------------------------------------------

@tree.command(name = 'help', description = 'Afficher la liste des commandes.')
async def help(interaction:discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(title = f'Help BlackPala',
                          description = f'''Pour plus d'informations sur une commande, tapez `/help <nom de la commande>`.
                          » **Préfix** : `/`
                          » **Commandes** : `31`''',
                          color = 0xEBB70E)
    
    embed.add_field(name = '`📌` Administration',
                    value = '''> • `bugreport` ; `debug` ; `guildlist` ; `botinfo` ; `guide`''',
                    inline = False)
    
    embed.add_field(name = '`🤖` BlackLists',
                    value = '''> • `setblacklist` ; `blacklistinfo` ; `setlogschannel`''',
                    inline = False)
    
    embed.add_field(name = '`💎` Paladium',
                    value = '''> • `pala` ; `palastats`''',
                    inline = False)
    
    embed.add_field(name = '`🚔` Modération',
                    value = '''> • `ban` ; `tempban` ; `unban` ; `kick` ; `timeout` ; `untimeout` ; `clear` ; `warn` ; `lookup` ; `userinfo`''',
                    inline = False)
    
    embed.add_field(name = '`📝` Utilitaire',
                    value = '''> • `suggest` ; `avatar` ; `rank` ; `leaderboard` ; `8ball` ; `ping` ; `help` ; `say` ; `guildinfo` ; `invite` ; `avis`''',
                    inline = False)
    
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/help`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# HELP
# ------------------------------------------
# ------------------------------------------
# GUIDE
# ------------------------------------------

@tree.command(name = 'guide', description = '''Pour envoyer l'embed "Guide.''')
@discord.app_commands.checks.has_role(1147168836131508224)
async def guide(interaction:discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(color = 0xEBB70E)
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1147825401159241728/Guide.png')

    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed)

    embed_ = discord.Embed(title = '🧭 Guide',
                           description = f'''Bienvenue sur le guide de BlackPala. Ici découvre la totalité des informations \nimportantes concernant le bot et le serveur. **Bonne lecture !** 📖''')

    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed_)

    embed_w_qsn = discord.Embed(color = 0xEBB70E)
    embed_w_qsn.set_image(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1147828292150370324/QSN.png')
    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed_w_qsn)

    embed__ = discord.Embed(title = '📌 Qui sommes - nous ?',
                            description = f'''BlackPala est un bot qui a été créé par des joueurs de Paladium. Notre bot sert de Blacklist, il est utile pour la Modération, mais comporte de nombreuses autres fonctionnalités. Tous les serveurs en rapport avec Paladium, ou n'ayant aucun rapport avec Paladium peuvent ajouter le bot vu qu'il est Publique ! 🪴''')
    
    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed__)

    embed_w_rules = discord.Embed(color = 0xEBB70E)
    embed_w_rules.set_image(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1147948561451982958/Reglement.png')
    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed_w_rules)


    embed___ = discord.Embed(title = '📒 Règlement du Serveur',
                            description = f'''*Il a pour but de créer un environnement respectueux, convivial et sécurisé pour tous les utilisateurs. En le suivant, vous contribuez à maintenir une atmosphère positive et à favoriser les échanges enrichissants au sein de notre communauté. Nous vous invitons donc à lire attentivement ces règles et à les respecter afin de profiter pleinement de votre séjour parmi nous.*
                            
                             🔸 **`#1 ` Règles sur le "savoir vivre"**
                            \- Les [Terms Of Service](https://discord.com/terms) ainsi que les [Community Guildelines](https://discord.com/guidelines) de discord s'appliquent à ce serveur.
                            \- Merci de garder un comportement respectueux envers chaque membres du serveur.
                            \- Toutes personnes pouvant nuire au serveur, se verra sanctionnée en conséquence.
                            \- La publicité sur ce serveur est interdite.
                            \- Les "ghost ping" seront sanctionnés d'un mute temporaire.
                            

 🔸 **`#2 ` Règles sur le "partage"**
\- Il est prohibé, d'envoyé en message privé, ou sur ce serveur, un quelconque lien. (excepté les GIFs)
\- Les publicités en messages privés sont interdites et sanctionnées d'un ban permanant.
\- La diffusation d'informations sur autruis, fausses ou non sera sévèrement sanctionnée.''')
    
    channel = bot.get_channel(1147992273603276891)
    await channel.send(embed = embed___)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/guide`''',
                               color = 0XDA3939)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# GUIDE
# ------------------------------------------
# ------------------------------------------
# INVITE
# ------------------------------------------

#class button_link(discord.ui.View):
#    @discord.ui.button(label="Ajouter BlackPala",
#                       style=discord.ButtonStyle.link,
#                       url=f"""https://discord.com/api/oauth2/authorize?client_id=1070777159091765258&permissions=19682228563015&scope=applications.commands%20bot""")
#    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
#        return await interaction.response.send_message("Merci d'avoir ajouté **BlackPala** à ton serveur !", ephemeral=True)
#
#@tree.command(name = "invite", description = "Permet d'inviter le bot sur ton serveur")
#async def invite(interaction: Interaction):
#    author_member: discord.Member = interaction.user
#    
#    embed = discord.Embed(title = 'Ajouter BlackPala',
#        description = f'''Pour ajouter <@1070777159091765258> à ton serveur, c'est simple.\nIl te suffit de cliquer sur le bouton et le tour est joué !''',
#                              color = 0xEBB70E)
#    
#    embed.set_footer(text = 'BlackPala (Tests)#6732')
#    embed.timestamp = datetime.utcnow()
#
#    await interaction.response.send_message(embed = embed, view = button_link())

# Logging

#    channel_log = bot.get_channel(1147165529782620253)
#    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/invite`''',
#                               color = 0X8A39dA)
#    
#    embed_logs.add_field(name = 'ID', value = f'''```yaml
#User = {author_member.id}
#Channel = {interaction.channel_id}
#GuildName = {interaction.guild.name}
#```''')
#    
#    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
#    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
#    embed_logs.timestamp = datetime.utcnow()
#
#    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# INVITE
# ------------------------------------------
# ------------------------------------------
# AVATAR
# ------------------------------------------

@tree.command(name = "avatar", description = "Permet de voir la photo de profil de quelqu'un")
async def avatar(interaction: Interaction):
    author_member: discord.Member = interaction.user

    user = interaction.user
    avatar_url = user.avatar.url
    
    embed = discord.Embed(description = f''' • **Avatar de {user.mention}**''',
                              color = 0xEBB70E)
    embed.set_image(url = avatar_url)

    await interaction.response.send_message(embed = embed)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/avatar`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# AVATAR
# ------------------------------------------
# ------------------------------------------
# SUGGEST
# ------------------------------------------

@tree.command(name = 'suggest', description = 'Faire une suggestion pour améliorer le Bot.')
async def suggest(interaction: discord.Interaction, suggestion : str):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(title = f'Suggestion de {author_member.name}',
                          description = f'''> • **Suggestion** : 
                          ```yaml
{suggestion}
                          ```''',
                          color = 0xEBB70E)

    embed.set_footer(text = f'© 2023 BlackPala - Tous droits réservés', icon_url = interaction.guild.icon.url)

    channel = bot.get_channel(1147163494144294955)
    await channel.send(embed = embed)

    await interaction.response.send_message(f'''Votre suggestion à correctement été envoyé ! Merci \:D''', ephemeral = True)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/suggest`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# SUGGEST
# ------------------------------------------
# ------------------------------------------
# PING
# ------------------------------------------

@tree.command(name = 'ping', description = 'Afficher le temps de latence du bot.')
async def ping(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds = difference))

    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count

    headers = {'Authorization': 'Bearer ptlc_ZhAjg2PEWYrW0EdOt01m2gzs88TFc8zXRP0RSx4KaPg'}

    response = requests.get("https://panel.xavrdtp.fr/api/client/servers/9246e162/resources", headers=headers)

    if response.status_code == 200:
        data = response.json()['attributes']["resources"]
        ram_used = round(int(data["memory_bytes"]) / (1024 * 1024), 2)
        embed = discord.Embed(title = f'Temps de latence BlackPala',
                              description=f'''> » **Ping** : `{round(bot.latency * 1000)}ms`
        > » **Temps de Connexion** : `{str(timedelta(seconds=difference))}`
        > » **RAM utilisée** : `{ram_used} Mo / {(psutil.virtual_memory().total // (1024 ** 2))} Mo`
        > » **Latence API** : `{response.elapsed.total_seconds() * 1000:.2f} ms`
        ''',
                              color = 0xEBB70E)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    else:
        print("Erreur lors de la récupération des statistiques du serveur")
        embed = discord.Embed(title = "Une erreur est survenue")

    await interaction.response.send_message(embed=embed)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/ping`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# PING
# ------------------------------------------
# ------------------------------------------
# BAN
# ------------------------------------------

@tree.command(name = 'ban', description = 'Bannir un membre du serveur.')
@app_commands.default_permissions(ban_members = True)
async def ban(interaction:discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison n'a été précisée'''):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''\🔸 **Vous ne pouvez pas vous bannir vous - même !**''', ephemeral = False) 
          
    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''\🔸 **Vous ne pouvez pas bannir cette personne car elle est à un rôle supérieur à vous !**''', ephemeral = False) 
    
    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''\🔸 **Cette personne est un Modérateur du serveur, je ne peux pas faire cela !**''', ephemeral = False) 
    
    try:
        await interaction.guild.ban(membre, reason = reason)
        await interaction.response.send_message(f'\🔹 **{membre} a été banni ! Raison : `[{reason}]`.**', ephemeral = False)

    except:
        return await interaction.response.send_message(f'''\🔸 **Je n'arrive pas à bannir ce membre !**''', ephemeral = False) 

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/ban`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# BAN
# ------------------------------------------
# ------------------------------------------
# UNBAN
# ------------------------------------------

@tree.command(name = 'unban', description = '''Débannir un utilisateur du serveur''')
@app_commands.default_permissions(ban_members = True)
async def unban(interaction:discord.Interaction, membre: discord.User):
    author_member: discord.Member = interaction.user

    try:
        await interaction.guild.unban(membre)
        await interaction.response.send_message(f'\🔹 **{membre} a été débanni !**', ephemeral = False)
    except:
        await interaction.response.send_message(f'''\🔸 **Cette utilisateur n'est pas banni !**''', ephemeral = False) 

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/unban`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# UNBAN
# ------------------------------------------
# ------------------------------------------
# KICK
# ------------------------------------------

@tree.command(name = 'kick', description = 'Expulser un membre du serveur')
@app_commands.default_permissions(kick_members = True)
async def kick(interaction:discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée"):
    author_member: discord.Member = interaction.user


    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''\🔸 **Vous ne pouvez pas vous expulser vous - même !**''', ephemeral = False)     
    
    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''\🔸 **Vous ne pouvez pas expulser cette personne car elle est à un rôle supérieur à vous !**''', ephemeral = False) 
    
    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''\🔸 **Cette personne est un Modérateur du serveur, je ne peux pas faire cela !**''', ephemeral = False) 
    
    try:
        await interaction.guild.kick(membre, reason=reason)
        await interaction.response.send_message(f'\🔹 **{membre} a été expulsé ! Raison : `[{reason}]`**', ephemeral = False)

    except:
        return await interaction.response.send_message(f'''\🔸 **Je n'arrive pas à expulser ce membre !**''', ephemeral = False) 
    
# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/kick`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# KICK
# ------------------------------------------
# ------------------------------------------
# TIMEOUT
# ------------------------------------------

@tree.command(name = 'timeout', description = 'Exclure temporairement un membre du serveur')
@app_commands.default_permissions(moderate_members = True)
async def timeout(interaction: discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée", days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'\🔸 **Vous ne pouvez pas vous exclure temporairement vous - même !**', ephemeral = False)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'\🔸 **Vous ne pouvez pas exclure temporairement cette personne car elle est à un rôle supérieur à vous !**', ephemeral = False)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'\🔸 **Cette personne est un Modérateur du serveur, je ne peux pas faire cela !**', ephemeral = False)

    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28):
        return await interaction.response.send_message(f'\🔸 **La durée d\'exclusion doit être inférieure à `28` jours !**', ephemeral = False)

    await membre.timeout(duration, reason = reason)

    await interaction.response.send_message(f'\🔹 **{membre} a été temporairement exclu ({duration}) ! Raison : `[{reason}]`**', ephemeral = False)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/timeout`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# TIMEOUT
# ------------------------------------------
# ------------------------------------------
# WARN
# ------------------------------------------

data_file = 'data.json'

@tree.command(name='warn', description='Avertir un membre du serveur')
@app_commands.default_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée"):
    author_member: discord.Member = interaction.user

    guild_id = interaction.guild_id

    warnings = {}
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            warnings = json.load(file)

    if str(membre.id) in warnings:
        warnings[str(membre.id)].append({
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'membre_name': membre.display_name
        })
    else:
        warnings[str(membre.id)] = [{
            'author_id': author_member.id,
            'guild_id': guild_id,
            'reason': reason,
            'author_name': author_member.display_name,
            'membre_name': membre.display_name
        }]

    with open(data_file, 'w') as file:
        json.dump(warnings, file, indent=4)

    await interaction.response.send_message(f'\🔹 **{membre.mention} a été averti par {author_member.mention}. Raison : `[{reason}]`**')

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/warn`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# WARN
# ------------------------------------------
# ------------------------------------------
# LOOKUP
# ------------------------------------------

@tree.command(name='lookup', description='Voir la liste des avertissements de quelqu\'un')
@app_commands.default_permissions(moderate_members=True)
async def lookup(interaction: discord.Interaction, id: str):
    author_member: discord.Member = interaction.user

    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            warnings = json.load(file)
    else:
        warnings = {}

    if id in warnings:
        user_warnings = warnings[id]

        embed = discord.Embed(title=f'» Avertissements de {id}',
                              color=0xEBB70E)

        for index, warning in enumerate(user_warnings):
            author_id = warning['author_id']
            guild_id = warning['guild_id']
            reason = warning['reason']
            author_name = warning['author_name']
            membre_name = warning['membre_name']
            timestamp = warning.get('timestamp', 'Non disponible')
            guild_name = warning.get('guild_name', 'Non disponible')

            field_name = f'\🔸 **`#{index + 1} `**'
            field_value = f'''> **Auteur :** {author_name} (`{author_id}`)\n**Raison :** `{reason}`\n**Serveur :** `{guild_name}`\n**Temps :** `{timestamp}`'''
            embed.add_field(name=field_name, value=field_value, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f'\🔸 **Aucun avertissement trouvé pour `{id}`.**')

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/lookup`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# LOOKUP
# ------------------------------------------
# ------------------------------------------
# USERINFO
# ------------------------------------------

@tree.command(name = 'userinfo', description = 'Donne des informations sur un membre du serveur.')
async def userinfo(interaction : discord.Interaction, member : typing.Optional[discord.Member] = None):
    if member is None:
        author_member = interaction.user
    else:
        author_member = member

    user_flags = author_member.public_flags

    embed = discord.Embed(title = f'Informations sur {author_member.name}',
                          color = 0xEBB70E)

    embed.add_field(name = '''\📌 Informations Générales''', value = f'''> » **Pseudo** : `{author_member.name}#{author_member.discriminator}`
    > » **ID** : `{author_member.id}`.
    > » **Créé le** : <t:{int(author_member.created_at.timestamp())}:D>.
    > » **Badge(s)** : `Indisponible`''', inline = True)

    embed.add_field(name = '''\⚡ Informations sur le Serveur''', value = f'''> » **Rôles ({len(author_member.roles) - 1})** : {", ".join([role.mention for role in author_member.roles[1:]]) if len(author_member.roles) > 1 else "Aucun"}
    > » **Rejoint le** : <t:{int(author_member.joined_at.timestamp())}:D>.
    > » **Surnom** : {author_member.nick if author_member.nick else "Aucun"}''', inline = False)

    embed.set_thumbnail(url = author_member.avatar.url)
    if author_member.banner:
        embed.set_image(url = author_member.banner.url)

    await interaction.response.send_message(embed = embed)

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/userinfo`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# USERINFO
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME LEVELLING                                                            #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------
# RANK
# ------------------------------------------

@bot.event
async def on_message(message):
    if not message.author.bot:
        response = manage_exp_event(message.author)
        with open('./levels.json', 'r') as f:
            levels = json.load(f)
        level = get_level(levels[str(message.author.id)]['experience'])
        author_name = message.author.name  # Récupérer le nom de l'auteur
        if response == "level_gained":
            await message.channel.send(f"\🔹 **Bravo {author_name}, tu viens d'atteindre le niveau `#{level} ` !**")

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
fill = 218, 165, 4


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

@tree.command(name = "rank", description = "Permet de voir votre niveau")
async def rank(interaction: Interaction, user: discord.Member = None):
    author_member: discord.Member = interaction.user
    if user == None:
        user = interaction.user
    with open('./levels.json', 'r') as f:
        levels = json.load(f)
    if not str(user.id) in levels:
        return await interaction.response.send_message('Vous n\'avez pas encore envoyé de messages !')
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
    mask = mask.resize(pfp.size, Image.ANTIALIAS)

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

    fnt = ImageFont.truetype('Montserrat.ttf', 35)
    fnt2 = ImageFont.truetype('Montserrat.ttf', 45)
    fnt3 = ImageFont.truetype('Montserrat.ttf', 25)
    m1 = f'#{rank}'
    w1, h1 = draw_.textsize(m1, font=fnt2)
    m2 = f'RANK'
    w2, h2 = draw_.textsize(m2, font=fnt3)
    m3 = f'LEVEL'
    w3, h3 = draw_.textsize(m3, font=fnt3)
    m4 = f'{level}'
    w4, h4 = draw_.textsize(m4, font=fnt2)
    m5 = f'{experience_str}/{max_xp_str} XP'
    w5, h5 = draw_.textsize(m5, font=fnt3)
    m6 = user.name
    w6, h6 = draw_.textsize(m5, font=fnt)
    if w6 < 430:
        draw_.text((210, 145 - h6), user.name, font=fnt, fill="white")
    else:
        draw_.text((210, 145 - h6), user.name, font=ImageFont.truetype('Montserrat.ttf', 20),
                   fill="white")
    draw_.text((800 - w5 - 35, 125), f"{experience_str}/{max_xp_str} XP", font=fnt3, fill="white")
    draw_.text((800 - w3 - w4 - 55, 45), f"LEVEL", font=fnt3, fill=(fill))
    draw_.text((800 - w4 - 40, 30), f"{level}", font=fnt2, fill=(fill))
    draw_.text((800 - (w3 + w4 + 85) - w1 - w2, 45), f"RANK", font=fnt3, fill="white")
    draw_.text((800 - w1 - w3 - w4 - 70, 30), f"#{rank}", font=fnt2, fill="white")

    card.save(f"card_{user.id}.png")


    await interaction.response.send_message(file=discord.File(f"card_{user.id}.png"))
    os.remove(f"card_{user.id}.png")

# Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/rank`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# RANK
# ------------------------------------------

def get_leaderboard(type):
    if type == "levels":
        with open('./levels.json', 'r') as f:
            levels = json.load(f)
        leaderboard = [(i, levels[i]['experience']) for i in levels]
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        return sorted_leaderboard

# ------------------------------------------
# LEADERBOARD
# ------------------------------------------

@tree.command(name='leaderboard', description='Permet de voir un classement')
@app_commands.choices(
    type=[
        app_commands.Choice(name='niveaux', value='levels'),
        app_commands.Choice(name='coins', value='coins')
    ]
)
async def leaderboard(interaction: Interaction, type: str):
    leaderboard_list = get_leaderboard(type)
    author_member: discord.Member = interaction.user
    if type == 'levels':
        with open('./levels.json', 'r') as f:
            levels = json.load(f)
        rank = 0
        str_leaderboard = ""
        for (user_id, experience) in leaderboard_list[0:10]:
            rank += 1
            user = bot.get_user(int(user_id))
            if user is not None:
                username = user.name
                userid = user.id
                exp, level_ = get_level(experience, 2)
                if rank == 1:
                    str_leaderboard += f'\🥇 <@{userid}> (Niveau **{level_}**)\n'
                elif rank == 2:
                    str_leaderboard += f'\🥈 <@{userid}> (Niveau **{level_}**)\n'
                elif rank == 3:
                    str_leaderboard += f'\🥉 <@{userid}> (Niveau **{level_}**)\n'
                elif rank == 4:
                    str_leaderboard += f'`#4` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 5:
                    str_leaderboard += f'`#5` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 6:
                    str_leaderboard += f'`#6` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 7:
                    str_leaderboard += f'`#7` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 8:
                    str_leaderboard += f'`#8` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 9:
                    str_leaderboard += f'`#9` <@{userid}>  (Niveau **{level_}**)\n'
                elif rank == 10:
                    str_leaderboard += f'`#10` <@{userid}>  (Niveau **{level_}**)\n'

    embed = discord.Embed(title = '''» Top #10 Levels''', description = f'''{str_leaderboard}\n\n> » **Comment monter dans le classement ?**
-Il vous suffit d'être actif et de parler dans les salons textuels !''',
    color = 0xEBB70E)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    await interaction.response.send_message(embed = embed)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/leaderboard`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# LEADERBOARD
# ------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------ #
#                                                   SYSTEME LEVELLING                                                            #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------
# BOTINFO
# ------------------------------------------

@tree.command(name = 'botinfo', description = 'Affiche les informations du bot.')
async def botinfo(interaction : discord.Interaction):
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

    embed = discord.Embed(title = f'» Informations sur le Bot', 
                          description = f'''> Pour plus d'informations sur le bot, cliquez __[`ici`](https://panel.xavrdtp.fr/server/9246e162)__.
    » **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes** : `31`
    » **Préfix** : `/`
    
    __[`Serveur Discord`](https://discord.gg/ehsDjn3Wrh)__''', color = 0xA150E8)

    embed.add_field(name = '''\📌 Informations Générales''', value = f'''> » **Créateur** : `sirop2menthe_`
    > » **Développeurs** : `sirop2menthe_#0`''', inline = True)

    embed.add_field(name = '''\📊 Statistiques''', value = f'''> » **Serveurs** : `{str(servers_count)}`
    > » **Utilisateurs** : `{total_members}`
    > » **Commandes** : `31`''', inline = False)

    embed.add_field(name = '''\🔧 Informations sur Système''', value = f'''> » **Hébergeur** : [`Panel.XAVRDTP`](https://panel.xavrdtp.fr/server/9246e162)
    > » **Plateforme** : `VPS Linux - 04`
    > » **Processeur** : `3.30 GHz 2 vCore(s) Xeon® E5`
    > » **Mémoire RAM** : `Undefined / 4000.00 MB`''', inline = False)

    embed.add_field(name = '''\👾 Informations sur le Bot''', value = f'''> » **Temps de Connexion** : `{str(uptime)}`
    > » **DataBase** : `Undefined`
    > » **Discord.py** : `{version}`
    > » **Version du Bot** : `V0.0.1`
    > » **ID** : `962051231973511318`''', inline = False)
    
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.set_footer(text = 'Developped by StabiloBleu © 2023 BlackPala Bot', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/botinfo`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# BOTINFO
# ------------------------------------------
# ------------------------------------------
# PALASTATS
# ------------------------------------------

#@tree.command(name='palastats', description='Affiche les informations sur Paladium.')
#async def palastats(interaction: discord.Interaction):
#    author_member: discord.Member = interaction.user
#
#    headers = {'Authorization': 'd921a5e8db4a35ae087fd4e434391c06'}
#
#    response = requests.get("https://api.mcsrvstat.us/2/mc.paladium-pvp.fr", headers=headers)
#
#    if response.status_code == 200:
#    data = response.json()
#    if 'attributes' in data:
#        resources = data['attributes'].get("resources", {})
#        ram_used = round(int(resources.get("memory_bytes", 0)) / (1024 * 1024), 2)
#
#
#        # Récupérez le nombre de joueurs connectés (exemple: 10 joueurs)
#        players_online = data.get("players", {}).get("online", 0)
#
#        # Créez un graphique avec le nombre de joueurs connectés
#        plt.figure(figsize=(6, 4))
#        plt.bar(['En ligne'], [players_online])
#        plt.title('Nombre de joueurs en ligne')
#        plt.ylabel('Nombre de joueurs')
#        plt.xlabel('Statistiques')
#
#        # Enregistrez le graphique dans un objet BytesIO
#        buffer = BytesIO()
#        plt.savefig(buffer, format='png')
#        buffer.seek(0)
#        plt.close()
#
#        # Créez un embed Discord avec le graphique inclus
#        embed = discord.Embed(
#            title=f'Temps de latence BlackPala',
#            color=0xEBB70E
#        )
#        embed.set_thumbnail(
#            url='https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
#
#        # Ajoutez le graphique en tant qu'image à l'embed
#        file = discord.File(buffer, filename='players_online.png')
#        embed.set_image(url='attachment://players_online.png')
#
#    else:
#        print("Key 'attributes' not found in the JSON response")
#        embed = discord.Embed(title="Une erreur est survenue")
#    else:
#    print("Erreur lors de la récupération des statistiques du serveur")
#    embed = discord.Embed(title="Une erreur est survenue")

# ------------------------------------------
# PALASTATS
# ------------------------------------------
# ------------------------------------------
# SETBLACKLIST
# ------------------------------------------

class button_actualisation(ui.View):
    @discord.ui.button(label = "", style = discord.ButtonStyle.secondary, custom_id = "reload", emoji = "<:Reload_Button:1148594902154883102>")
    async def button(self, interaction: Interaction, button: discord.ui.Button):
        pass

@tree.command(name = 'setblacklist', description = 'Affiche les informations sur Paladium.')
async def setblacklist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    embed = discord.Embed(title = f'» Blacklist',
                      description = f'''Pour faire une demande de blacklist, utilisez la commande `/report`, et remplissez les champs !
                      
                      > [Mael_360](https://fr.namemc.com/search?q=Mael_360) » **Raison :** `Trahison`

                      > [Exionne](https://fr.namemc.com/search?q=Exionne) » **Raison :** `Trahison`

                      > [BateauTigre](https://fr.namemc.com/search?q=BateauTigre) » **Raison :** `Trahisons`

                      > [Fan2Ryze](https://fr.namemc.com/search?q=Fan2Ryze) » **Raison :** `Trahison` ; `Double Faction`


                      ''',
                      color = 0xEBB70E)

    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.set_footer(text = '© 2023 BlackPala - Tous droits réservés', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed, view = button_actualisation())

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/setblacklist`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# SETBLACKLIST
# ------------------------------------------
# ------------------------------------------
# GUILDINFO
# ------------------------------------------

@tree.command(name='guildinfo', description='Affiche les informations du serveur.')
async def guildinfo(interaction: discord.Interaction):
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
    streaming_count = sum(activity.type == discord.ActivityType.streaming for member in guild.members for activity in member.activities)
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

    embed = discord.Embed(title = f'{guild.name} ({guild.id})',
                          description = f'''> » Salons Textuels : `{text_channels}` ; Salons Vocaux : `{voice_channels}` ; Fils : `{threads}` ; Rôles : `{num_roles}`''',
                          color = 0xEBB70E)

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
    embed.set_footer(text = '© 2023 BlackPala - Tous droits réservés', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/guildinfo`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# GUILDINFO
# ------------------------------------------
# ------------------------------------------
# SAY
# ------------------------------------------

@tree.command(name = 'say', description = 'Envoyer un message via le bot.')
@app_commands.default_permissions(ban_members = True)
async def say(interaction:discord.Interaction, channel: discord.TextChannel, message: str):
    author_member: discord.Member = interaction.user

    await channel.send(message)
    await interaction.response.send_message(f'Message envoyé dans le salon {channel.mention} !', ephemeral = True)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/say`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# SAY
# ------------------------------------------
# ------------------------------------------
# AVIS
# ------------------------------------------

@tree.command(name="avis", description="Donner votre avis sur notre projet !")
@app_commands.choices(
    note=[
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3),
        app_commands.Choice(name="4", value=4),
        app_commands.Choice(name="5", value=5)
    ]
)
async def avis(interaction: discord.Interaction, note: int, commentaire: str):
    author_member: discord.Member = interaction.user

    if note < 1 or note > 5:
        await interaction.response.send_message(
            f'\🔸 **La note doit être entre 1 et 5.**', ephemeral=True)
        return

    note_etoiles = '⭐' * note + '✰' * (5 - note)

    for i in range(1, 6):
        if i <= note:
            emoji = '⭐'
        else:
            emoji = '✰'

    channel = bot.get_channel(1147185790502309968)
    timestamp = datetime.utcnow().timestamp() + 2 * 60 * 60
    embed = discord.Embed(description = f'''<t:{int(timestamp)}:F> (<t:{int(timestamp)}:R>) 

    > » **Note** : `{note_etoiles}`

    > » **Commentaire :**
    ```yaml
    {commentaire}
    ```''', 
                          color = 0xEBB70E)
    try:
        embed.set_author(name=author_member, icon_url=interaction.user.avatar.url)
    except:
        embed.set_author(name=author_member)
    embed.set_footer(text=f'''» Laissez vous aussi un avis sur notre projet !''',
                     icon_url=f'''https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png''')
    embed.set_image(url='https://cdn.discordapp.com/attachments/1147164813731053650/1148621727786614844/Merci.png')

    message = await channel.send(embed=embed)
    await interaction.response.send_message(f'\🔹 **Votre avis à été envoyé correctement ! Merci \:D**', ephemeral = True)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/avis`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# AVIS
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
        await interaction.followup.send(f'\🔹 **`1` message à été supprimé !**')
    else:
        await interaction.followup.send(f'\🔹 **`{len(deleted)}` messages ont été supprimés !**')

    if len(deleted) > 0:
        embed = discord.Embed(title="Voici les messages qui ont été supprimés :", description="")
        for msg in deleted:
            embed.description += f'> *envoyé à* <t:{int(msg.created_at.timestamp())}:T> de {msg.author.mention} : `{msg.content}`\n'
        await author_member.send(embed=embed)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/clear`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# CLEAR
# ------------------------------------------
# ------------------------------------------
# GUILDLIST
# ------------------------------------------

@tree.command(name='guildlist', description='Afficher la liste des serveurs sur lesquels se trouvent le bot.')
@discord.app_commands.checks.has_role(1147168836131508224)
async def guildlist(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    role = discord.utils.get(author_member.guild.roles, id=1147168836131508224)

    if role in author_member.roles:
        guilds = sorted(interaction.client.guilds, key=lambda guild: guild.member_count, reverse=True)

        messages = []
        current_message = '**Liste des serveurs**\n\n'

        for guild in guilds:
            guild_name = guild.name
            guild_owner = guild.owner.mention
            guild_member_count = str(guild.member_count)

            # Check if adding this guild would exceed the message length limit
            if len(current_message) + len(guild_name) + len(guild_owner) + len(guild_member_count) + 13 > 2000:
                messages.append(current_message)
                current_message = ''

            current_message += f'» `{guild_name}` ({guild_owner}) (**{guild_member_count}** Membres)\n'

        messages.append(current_message)

        # Send the messages
        for i, message in enumerate(messages):
            if i == 0:
                await interaction.response.send_message(message, ephemeral=True)
            else:
                await interaction.followup.send(message, ephemeral=True)
        
    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/guildlist`''',
                               color = 0XDA3939)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# GUILDLIST
# ------------------------------------------
# ------------------------------------------
# BUGREPORT
# ------------------------------------------

@tree.command(name="bugreport", description="Donner votre avis sur notre projet !")
async def avis(interaction: discord.Interaction, note: int, commentaire: str):
    author_member: discord.Member = interaction.user

    if note < 1 or note > 5:
        await interaction.response.send_message(
            f'\🔸 **La note doit être entre 1 et 5.**', ephemeral=True)
        return

    note_etoiles = '⭐' * note + '✰' * (5 - note)

    for i in range(1, 6):
        if i <= note:
            emoji = '⭐'
        else:
            emoji = '✰'

    channel = bot.get_channel(1147185790502309968)
    timestamp = datetime.utcnow().timestamp() + 2 * 60 * 60
    embed = discord.Embed(description = f'''<t:{int(timestamp)}:F> (<t:{int(timestamp)}:R>) 

    > » **Note** : `{note_etoiles}`

    > » **Commentaire :**
    ```yaml
    {commentaire}
    ```''', 
                          color = 0xEBB70E)
    try:
        embed.set_author(name=author_member, icon_url=interaction.user.avatar.url)
    except:
        embed.set_author(name=author_member)
    embed.set_footer(text=f'''» Laissez vous aussi un avis sur notre projet !''',
                     icon_url=f'''https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png''')
    embed.set_image(url='https://cdn.discordapp.com/attachments/1147164813731053650/1148621727786614844/Merci.png')

    message = await channel.send(embed=embed)
    await interaction.response.send_message(f'\🔹 **Votre avis à été envoyé correctement ! Merci \:D**', ephemeral = True)

    # Logging

    channel_log = bot.get_channel(1147165529782620253)
    embed_logs = discord.Embed(description = f'''**{author_member}** à utiliser la commande `/avis`''',
                               color = 0X8A39dA)
    
    embed_logs.add_field(name = 'ID', value = f'''```yaml
User = {author_member.id}
Channel = {interaction.channel_id}
GuildName = {interaction.guild.name}
```''')
    
    embed_logs.set_author(name = author_member.name, icon_url = author_member.avatar.url)
    embed_logs.set_footer(text = 'BlackPala (Tests)#6732', icon_url = 'https://cdn.discordapp.com/attachments/1147147088182906972/1148161333011959858/avatar.png')
    embed_logs.timestamp = datetime.utcnow()

    await channel_log.send(embed = embed_logs)

# ------------------------------------------
# BUGREPORT
# ------------------------------------------

bot.run(TOKEN)