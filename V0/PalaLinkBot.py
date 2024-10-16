import discord, asyncio, json, re
import time
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha
from discord.utils import get
import random
from discord import File
from discord.ext import commands
from typing import Optional
import requests
import typing

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents)
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
            global startTime 
            startTime = time.time()
#           stats_channels.start()
            self.add_view(mainBlacklist())
        print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️     │
    │                                             │
    │  {self.user} is  Online ==> ✔️        │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛''')

bot = client()
tree = app_commands.CommandTree(bot)

@tasks.loop(seconds = 4)
async def bio():
    await bot.wait_until_ready()
    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
    status = [f'{str(len(bot.guilds))}/75 Serveurs', 'Préfix : /', f'{total_members} Utilisateurs', f'V0.0.5', f'/help']
    for i in status:
        await bot.change_presence(activity = discord.Game(str(i)))
        await asyncio.sleep(4)

def convert(sec):
    min, hour = 0,0
    while sec > 60:
        if sec > 60:
            min = min + 1
            sec = sec - 60
        if min > 60:
            hour = hour + 1
            min = min - 60
    return str(round(hour)) + " heures " + str(round(min)) + " minutes " + str(round(sec))


# Type : Command
# Name : Help
# --- Start Here --- #

@tree.command(name = 'help', description = 'Afficher la liste des commandes.')
async def help(interaction:discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(description = f'''Pour plus d'informations sur le bot, cliquez __[`ici`](https://palalink.fr/help-bot)__.
    » **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes** : `52`
    » **Préfix** : `/<commande>`
    
    *Ne manquez pas l'opportunité de découvrir notre __[`Site Internet`](https://palalink.fr/)__.*''', color = 0x5865F2)

    embed.set_author(name = f'Commande " Help "', icon_url = f'{author_member.avatar.url}')
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.timestamp = datetime.utcnow()

    embed.add_field(name = '''\📌 Administration''', value = '''> • `note` ; `pingall` ; `webstatus` ; `uptime` ; `presence`.''', inline = False)
    embed.add_field(name = '''\🛠️ Utilitaire''', value = '''> • `help` ; `msg` ; `ping` ; `say` ; `serverinfo` ; `botinfo` ; `userinfo` ; `suggestion` ; `bugreport` ; `embedbuilder` ; `back` ; `avis`.''', inline = True)
    embed.add_field(name = '''\📒 Profils''', value = '''> • `profil` ; `edit` ; `remove` ; `phelp`.''', inline = False)
    embed.add_field(name = '''\🎲 Minis-Jeux''', value = '''> • `joke` ; `8ball` ; `roulette` ; `dé` ; `slap` ; `hug` ; `tictactoe` ; `shifoumi` ; `guessthenumber`.''', inline = False)
    embed.add_field(name = '''\🚨 Modération''', value = '''> • `ban` ; `tempban` ; `unban` ; `kick` ; `timeout` ; `untimeout` ; `mute` ; `tempmute` ; `unmute` ; `clear` ; `lock` ; `unlock` ; `assignall` : `removeall`.''', inline = False)
    embed.add_field(name = '''\🎮 Paladium''', value = '''> • `palainfo` ; `palastatus` ; `palalinks` ; `status`.''', inline = False)
    embed.add_field(name = '''\🚫 Blacklist''', value = '''> • `setbl` ; `blinfo` ; `setbl2` ; `bhelp`.''', inline = False)


    await interaction.response.send_message(embed = embed, ephemeral=False)


    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/help` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

@tree.command(name = 'embed_exemple_bl', description = '''Exemble d'embed''')
async def add_bl(interaction: discord.Interaction):

    embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)

    embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
    await interaction.response.send_message(embed = embed, ephemeral = False, view=mainBlacklist2())

class mainBlacklist2(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "Rafraîchir", style = discord.ButtonStyle.red, custom_id="rafraîchir_button")
    async def rafraîchir_button(self, interaction: discord.Interaction, button):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)
        list_ = ""
        for i in blacklist:
            list_ += f"- {blacklist[i]['membre']} `(id discord : {i})`\nRaison : `{blacklist[i]['reason']}`\n"
        embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)

        embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
        await interaction.message.edit(embed=embed, view=mainBlacklist2())
        await interaction.response.send_message(f"**Le panel de Blacklist a bien été rafraîchi !**", ephemeral = True)

    @discord.ui.button(label = "⬅️", style = discord.ButtonStyle.blurple, custom_id="right_button")
    async def right_button(self, interaction: discord.Interaction, button):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)
        list_ = ""
        for i in blacklist:
            list_ += f"- {blacklist[i]['membre']} `(id discord : {i})`\nRaison : `{blacklist[i]['reason']}`\n"
        embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)

        embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
        await interaction.message.edit(embed=embed, view=mainBlacklist2())
        await interaction.response.send_message(f"**Page changée !**", ephemeral = True)

    @discord.ui.button(label = "➡️", style = discord.ButtonStyle.blurple, custom_id="left_button")
    async def left_button(self, interaction: discord.Interaction, button):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)
        list_ = ""
        for i in blacklist:
            list_ += f"- {blacklist[i]['membre']} `(id discord : {i})`\nRaison : `{blacklist[i]['reason']}`\n"
        embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)

        embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        await interaction.message.edit(embed=embed, view=mainBlacklist2())
        await interaction.response.send_message(f"**Il n'y a pas assez de membre blacklisté pour faire une 2ème Page !**", ephemeral = True)


# Type : Command, Button
# Name : blacklist
# --- Start Here --- #

@tree.command(name = 'blacklist', description = 'Permets d\'afficher le panel de blacklist.')
async def blacklist(interaction:discord.Interaction):
    with open('blacklist.json', 'r') as f:
        blacklist = json.load(f)
    list_ = ""
    for i in blacklist:
        list_ += f"- {blacklist[i]['membre']} `(id discord : {i})`\nRaison : `{blacklist[i]['reason']}`\n"
    embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)

    embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
    await interaction.response.send_message(embed = embed, view=mainBlacklist2())

class mainBlacklist(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout = None)

    @discord.ui.button(label = "Rafraîchir", style = discord.ButtonStyle.green, custom_id="rafraîchir_button")
    async def rafraîchir_button(self, interaction: discord.Interaction, button):
        with open('blacklist.json', 'r') as f:
            blacklist = json.load(f)
        list_ = ""
        for i in blacklist:
            list_ += f"- {blacklist[i]['membre']} `(id discord : {i})`\nRaison : `{blacklist[i]['reason']}`\n"
        embed = discord.Embed(description = f'''> **[`Mikinouche`](https://fr.namemc.com/profile/Mikinouche.1)** » **Scam TP Spawner** *Discord Inconnu*.
        
        > **[`Luffytaro`](https://fr.namemc.com/profile/Luffytaro.2)** » **Trahison** *Discord Inconnu*.
        
        > **[`bozoo_`](https://fr.namemc.com/profile/bozoo_.2)** » **Scam Texture Pack** *Discord Inconnu*.''',
                              color = 0xff5b5e)
    
        embed.set_author(name = f'''Blacklist InterServeur @PalaLink''', icon_url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
        embed.set_footer(text = f'© 2023 PalaLink - Tous droits réservés', icon_url = interaction.guild.icon.url)
        await interaction.message.edit(embed=embed, view=mainBlacklist())
        await interaction.response.send_message(f"**Le panel de Blacklist a bien été rafraîchi !**", ephemeral = True)

@tree.command(name = 'add-bl', description='Permet d\'ajouté des membres a la blacklist.')
async def add_bl(interaction: discord.Interaction, membre: discord.Member, reason: str):
    with open(r'blacklist.json', 'r') as f: comm = json.load(f)
    if membre.id in comm:
        return await interaction.response.send_message("Ce joueur a déjà été ajouter !")
    comm[membre.id] = {
        "membre": f"<@{membre.id}>",
        "reason": reason
}
    with open(r'blacklist.json', 'w') as f: json.dump(comm, f, indent=2)
    return await interaction.response.send_message(f"**L'utilisateur {membre} `(id : {membre.id})` a bien était ajouter a la blacklist !**\n**Raison : {reason}**")

# --- End Here --- #


# Type : Command
# Name : msg
# --- Start Here --- # 

# PROBLEM : ❌❌❌ Le couldown ne marche pas ❌❌❌

@tree.command(name='msg', description='Envoyer un message privé à un membre du serveur.')
@commands.cooldown(1, 3600, commands.BucketType.user)
async def msg(interaction:discord.Interaction, destinataire:discord.Member, message:str):
    author_member: discord.Member = interaction.user

    await destinataire.send(f'''{message}''')
    await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : Message correctement envoyé à {destinataire.mention} !', ephemeral=True)

    embed_log_commande = discord.Embed(description = f'''» **Envoyeur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Destinataire** : **{destinataire}** __{destinataire.mention}__ `{destinataire.id}`
    » **Message** : `{message}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " Msg "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/msg` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

@msg.error
async def msg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
         await ctx.send(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne devez attendre {error.retry_after:.0f} avant de pouvoir réutiliser la commande !''', ephemeral = False)

# --- End Here --- #


# Type : Command
# Name : Help
# --- Start Here --- #

@tree.command(name = 'ping', description = 'Afficher la latence du Bot')
async def ping(interaction:discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(description = f'''» **Ping** : `{round(bot.latency * 1000)}ms` <a:Load:1081370281194553365>''', color = 0x5865F2)

    embed.set_author(name = f'Commande " Ping "', icon_url = f'{author_member.avatar.url}')
    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed = embed, ephemeral=True)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/ping` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #


# Type : Command
# Name : Presence
# --- Start Here --- #

# PROBLEM : ❌❌❌ Contenu de l'embed trop gros pour que le message soit envoyé ❌❌❌

@tree.command(name='presence', description='Afficher la liste des serveurs sur lesquels se trouvent le bot.')
@discord.app_commands.checks.has_role(1081272403465875516)
async def presence(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    role = discord.utils.get(author_member.guild.roles, id=1081272403465875516)

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

            current_message += f'**Nom**: `{guild_name}` **Créateur**: {guild_owner} **Membres**: {guild_member_count}\n'

        messages.append(current_message)

        # Send the messages
        for i, message in enumerate(messages):
            if i == 0:
                await interaction.response.send_message(message, ephemeral=True)
            else:
                await interaction.followup.send(message, ephemeral=True)

        # Send log message
        channel_log = interaction.bot.get_channel(1081294415760474193)
        await channel_log.send(f'''> `/presence` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')
    else:
        await interaction.response.send_message("Vous n'avez pas le rôle nécessaire pour exécuter cette commande.", ephemeral=True)

# --- End Here --- #


# Type : Command
# Name : Back
# --- Start Here --- #

@tree.command(name = 'back', description = 'On passe de TheReference à PalaLink ! On vous explique...')
async def back(interaction:discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(description = f'''Hey {author_member.mention} !
    Alors comme ça, tu as connus `TheReference` ? Super ! Cela va me faire gagner du temps...
    
    > Nous avons **décidé depuis début Février** de **reprendre le projet**. Tout en le "**boostant**" et en l'**améliorant** pour qu'on ai même pas besoin de faire une "MAJ Majeure".
    
    Nous avons changés de nom, en effet maintenant c'est `PalaLink`. Tout comme nous avons changé de [Serveur Discord](https://discord.gg/qsPrUjVCn5).
    
    Les **buts n'ont pas changés** comparé à TheReference, seulement **les équipes sont différentes**, le **fonctionnement aussi**. Avec des **Objectifs** et des **fonctionnalités en +**...
    
    **Pour les Chefs de Faction** : Notre site est conçu spécialement pour les Chefs de Faction, pour les aider à recruter les meilleurs joueurs. Nous offrons une plateforme de référencement où les joueurs peuvent s'inscrire et mettre en avant leurs compétences et leurs réalisations dans le jeu. Les Chefs de Faction peuvent parcourir notre liste de joueurs et trouver ceux qui conviennent le mieux à leur faction, et également plus de fonctionnalité en ajoutant le bot sur votre serveur.

    **Pour les Gérants de Market** : Si vous êtes un Gérant de Market/Shop sur Paladium, vous savez à quel point il est important de trouver les meilleurs prix, des vendeurs performants ainsi que des modérateurs fiables, https://palalink.com/ ||**Site temporairement non - accessible|| peut vous aider dans cette tâche ! Notre site de référencement est également un excellent moyen de trouver des vendeurs de qualité pour votre marché.

    __En espérant vous avoir convaincu, merci de nous faire, et de nous avoir fait confiance !__
    Cordialement, l'équipe création du PalaLink''', color = 0x5865F2)


    embed.set_author(name = f'Commande " Back "', icon_url = f'{author_member.avatar.url}')
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.timestamp = datetime.utcnow()


    await interaction.response.send_message(embed = embed, ephemeral=True)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/back` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

# Type : Event
# Name : on_guild_join
# --- Start Here --- #

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
                          color=0x5865F2)

    embed.set_author(name = f'Nouveau Serveur !', icon_url = f'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_thumbnail(url = f'{guild.icon.url}')
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

    embed.set_thumbnail(url=guild.icon.url)

    channel = bot.get_channel(1081377004026335372)
    await channel.send(embed = embed)
    channel_admin = bot.get_channel(1081377004026335372)
    await channel_admin.send(invite)

# --- End Here --- #

# Type : Event
# Name : on_guild_remove
# --- Start Here --- #

@bot.event
async def on_guild_remove(guild):

    embed = discord.Embed(description = f'''» **Nom du Serveur** : `{guild.name}` *{guild.id}*
    » **Membres** : **{guild.member_count}**
    » **Créateur** : `{guild.owner}` ||{guild.owner.id}||''', color = 0xF25858)

    embed.set_author(name = f'Event " on_guild_remove "', icon_url = f'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.set_thumbnail(url = f'{guild.icon.url}')
    embed.timestamp = datetime.utcnow()


    channel = bot.get_channel(1081377004026335372)
    await channel.send(embed = embed)

# --- End Here --- #

# Type : Task Loop
# Name : stats_channels
# --- Start Here --- #

@tasks.loop(seconds = 600)
async def stats_channels():
    l = []
    total_members = 0
    for guild in bot.guilds:
        l.append(str(guild.name) + str(guild.member_count))
        total_members = total_members + guild.member_count

        if total_members > 1000:
            k_number = "{:.2f}k".format(guild.member_count / 1000)
            users_voc_channel = bot.get_channel(1081343822149193828)
            await users_voc_channel.edit(name = "🧸 ・Utilisateurs : " + f'{k_number}')
        else:
            await users_voc_channel.edit(name = "🧸 ・Utilisateurs : " + f'{k_number}')
    guild_voc_channel = bot.get_channel(1081343868336885852)
    await guild_voc_channel.edit(name = "🎉・Serveurs : " + f'{len(bot.guilds)}')

# --- End Here --- #

# Type : Command
# Name : ban
# --- Start Here --- #

@tree.command(name = 'ban', description = 'Bannir un membre du serveur.')
@app_commands.default_permissions(ban_members = True)
async def ban(interaction:discord.Interaction, membre: discord.Member, reason: str = '''Aucune raison n'a été précisée'''):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas vous bannir vous - même !''', ephemeral = False) 
          
    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas bannir cette personne car elle est à un rôle supérieur à vous !''', ephemeral = False) 
    
    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Cette personne est un Modérateur du serveur, je ne peux pas faire cela !''', ephemeral = False) 
    
    try:
        await interaction.guild.ban(membre, reason = reason)
        await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : {membre} a été banni ! `[{reason}]`', ephemeral = False)

    except:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Je n'arrive pas à bannir ce membre !''', ephemeral = False) 


    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Sanctionné** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " Ban "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/ban` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

# --- End Here --- #

# Type : Command
# Name : unban
# --- Start Here --- #

@tree.command(name = 'unban', description = '''Débannir un utilisateur du serveur''')
@app_commands.default_permissions(ban_members = True)
async def unban(interaction:discord.Interaction, membre: discord.User, reason: str = "Aucune raison n'a été précisée"):
    author_member: discord.Member = interaction.user

    try:
        await interaction.guild.unban(membre, reason = reason)
        await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : {membre} a été débanni ! `[{reason}]`', ephemeral = False)
    except:
        await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Cette utilisateur n'est pas banni !''', ephemeral = False) 


    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Pardonné** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " Ban "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()


    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/unban` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

# --- End Here --- #

# Type : Command
# Name : kick
# --- Start Here --- #

@tree.command(name = 'kick', description = 'Expulser un membre du serveur')
@app_commands.default_permissions(kick_members = True)
async def kick(interaction:discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée"):
    author_member: discord.Member = interaction.user


    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas vous expulser vous - même !''', ephemeral = False)     
    
    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas expulser cette personne car elle est à un rôle supérieur à vous !''', ephemeral = False) 
    
    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Cette personne est un Modérateur du serveur, je ne peux pas faire cela !''', ephemeral = False) 
    
    try:
        await interaction.guild.kick(membre, reason=reason)
        await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : {membre} a été expulsé ! `[{reason}]`', ephemeral = False)

    except:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Je n'arrive pas à expulser ce membre !''', ephemeral = False) 
    

    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Expulsé** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " Kick "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()


    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/kick` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

# --- End Here --- #


# Type : Command
# Name : tempban
# --- Start Here --- #

@tree.command(name = 'tempban', description = 'Banni temporairement un membre du serveur')
@app_commands.default_permissions(ban_members = True)
async def tempban(interaction:discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée", days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    author_member: discord.Member = interaction.user


    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas vous bannir temporairement vous - même !''', ephemeral = False)     
    
    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Vous ne pouvez pas bannir temporairement cette personne car elle est à un rôle supérieur à vous !''', ephemeral = False) 
    
    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'''<a:No:1081720631390916778>  `FAILURE` : Cette personne est un Modérateur du serveur, je ne peux pas faire cela !''', ephemeral = False) 
    
    with open('data.json', 'r', encoding = "utf-8") as f:
        data = json.load(f)
    times = (60 * 60 * 24 * days) + (60 * 60 * hours) + (60 * minutes) + seconds
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    data['tempban'][str(membre.id)] = {}
    data['tempban'][str(membre.id)]['id'] = int(membre.id)
    data['tempban'][str(membre.id)]['time'] = time.time() + times
    data['tempban'][str(membre.id)]['reason'] = reason

    with open('data.json', 'w') as f:
        json.dump(data, f)

    await interaction.guild.ban(membre, reason=f"{reason} | Modérateur: {author_member.display_name}", delete_message_days=days)

    await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : {membre} a été temporairement banni ({duration}) ! `[{reason}]`', ephemeral = False)

    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Temporairement Ban** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`
    » **Durée** : `{duration}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " TempBan "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/tempban` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)


# --- End Here --- #

# Type : Command
# Name : timeout
# --- Start Here --- #

@tree.command(name='timeout', description='Exclure temporairement un membre du serveur')
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée", days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    author_member: discord.Member = interaction.user

    if membre.id == interaction.user.id:
        return await interaction.response.send_message(f'<a:No:1081720631390916778> `FAILURE` : Vous ne pouvez pas vous exclure temporairement vous - même !', ephemeral=False)

    if membre.top_role.position > interaction.user.top_role.position:
        return await interaction.response.send_message(f'<a:No:1081720631390916778> `FAILURE` : Vous ne pouvez pas exclure temporairement cette personne car elle est à un rôle supérieur à vous !', ephemeral=False)

    if membre.guild_permissions.ban_members:
        return await interaction.response.send_message(f'<a:No:1081720631390916778> `FAILURE` : Cette personne est un Modérateur du serveur, je ne peux pas faire cela !', ephemeral=False)

    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if duration >= timedelta(days=28):
        return await interaction.response.send_message(f'<a:No:1081720631390916778> `FAILURE` : La durée d\'exclusion doit être inférieure à **28 jours** !', ephemeral=False)

    await membre.timeout(duration, reason=reason)

    await interaction.response.send_message(f'<a:Yes:1081365228173938808> `SUCCESS` : {membre} a été temporairement exclu ({duration}) ! `[{reason}]`', ephemeral=False)

    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Temporairement Expulsé** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`
    » **Durée** : `{duration}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " TimeOut "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/timeout` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)


# --- End Here --- #

# Type : Command
# Name : untimeout
# --- Start Here --- #

@tree.command(name = 'untimeout', description = '''Supprimer le timeout d'un membre''')
@app_commands.default_permissions(moderate_members = True)
async def untimeout(interaction:discord.Interaction, membre: discord.Member, reason: str = "Aucune raison n'a été précisée"):
    author_member: discord.Member = interaction.user

    
    await membre.timeout(None, reason = reason)
    await interaction.response.send_message(f'''<a:Yes:1081365228173938808>  `SUCCESS` : {membre} n'est plus timeout !''', ephemeral = False)

    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Membre Pardonné** : **{membre}** __{membre.mention}__ `{membre.id}`
    » **Raison** : `{reason}`''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " UnTimeOut "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/untimeout` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

# --- End Here --- #

# Type : Task
# Name : check_ban_end
# --- Start Here --- #

@tasks.loop(seconds = 2)
async def check_ban_end():
    with open('data.json', 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    for user in data['tempban']:
        times = int(data['tempban'][user]['time'])
        a_time = int(time.time())
        if a_time > times:
            guild = bot.get_guild(1080595360247980032)
            user_ = guild.get_member(data['tempban'][user]['id'])
            await guild.unban(user_)
            del data['tempban'][user]
            with open('data.json', 'w') as f:
                json.dump(data, f)
            return print(f'[TEMP_BAN] Utilisateur {user_} débanni.')
        
# --- End Here --- #

# Type : Command
# Name : Clear
# --- Start Here --- #

@tree.command(name='clear', description='Pour supprimer un nombre X de messages')
@app_commands.default_permissions(moderate_members=True)
async def clear(interaction: discord.Interaction, number: int):
    author_member: discord.Member = interaction.user
    await interaction.response.defer(ephemeral=True)

    deleted = await interaction.channel.purge(limit=number, check=lambda msg: not msg.pinned)

    if number == 1:
        await interaction.followup.send(f'<a:Yes:1081365228173938808>  `SUCCESS` : **1 message** à été supprimé !', ephemeral=False)
    else:
        await interaction.followup.send(f'<a:Yes:1081365228173938808>  `SUCCESS` : **{len(deleted)} messages** ont été supprimés !', ephemeral=False)

    if len(deleted) > 0:
        embed = discord.Embed(title="Voici les messages qui ont été supprimés :", description="")
        for msg in deleted:
            embed.description += f'> <t:{int(msg.created_at.timestamp())}:T> __{msg.author.mention}__ : *{msg.content}*\n'
        await author_member.send(embed=embed)

    embed_log_commande = discord.Embed(description = f'''» **Modérateur** : **{author_member}** __{author_member.mention}__ `{author_member.id}`
    » **Nombre de Messages Clear** : **{len(deleted)}** messages.''', color = 0x5865F2)

    embed_log_commande.set_author(name = f'Commande " Clear "', icon_url = f'{author_member.avatar.url}')
    embed_log_commande.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed_log_commande.timestamp = datetime.utcnow()

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/clear` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''', embed = embed_log_commande)

# --- End Here --- #

# Type : Command
# Name : ServeurInfo
# --- Start Here --- #

@tree.command(name='serveurinfo', description='Affiche les informations du serveur.')
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
                          description=f'''> Salons Textuels : `{text_channels}` ; Salons Vocaux : `{voice_channels}` ; Fils : `{threads}` ; Rôles : `{num_roles}`''',
                          color=0x5865F2)

    embed.add_field(name='Propriétaire', value=f'''{guild.owner.mention} ||{guild.owner.id}||''', inline=False)
    embed.add_field(name='Membres', value=member_count, inline=True)
    embed.add_field(name='Boosts', value=f"{boost_count} boost(s) (Palier {boost_level})", inline=True)
    embed.add_field(name='Niveau de Verif\'', value=verification_level, inline=True)

    if num_roles > 20:
        role_mentions = [role.mention for role in roles]
        role_mentions.append("...")
    else:
        role_mentions = [role.mention for role in roles]

    embed.add_field(name='Rôles', value=" ; ".join(role_mentions), inline=False)
    embed.add_field(name='Online', value=online_count, inline=True)
    embed.add_field(name='Offline', value=offline_count, inline=True)
    embed.add_field(name='Ne pas Déranger', value=dnd_count, inline=True)
    embed.add_field(name=f'Emojis ({num_emojis})', value=f"{emojis_str}", inline=False)
    embed.add_field(name="Date de création", value=f'<t:{int(datetime.timestamp(guild.created_at))}:D>', inline=False)
    embed.add_field(name="Rejoint le", value=f'<t:{int(guild.me.joined_at.timestamp())}:D>', inline=False)

    embed.set_thumbnail(url=guild.icon.url)

    await interaction.response.send_message(embed = embed)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/serveurinfo` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')


# --- End Here --- #

# Type : Command
# Name : BotInfo
# --- Start Here --- #


@tree.command(name='botinfo', description='Affiche les informations du bot.')
async def botinfo(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

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

    embed = discord.Embed(title=f'Informations sur le Bot', 
                          description = f'''> Pour plus d'informations sur le bot, cliquez __[`ici`](https://palalink.fr/help-bot)__.
    » **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes** : `52`
    » **Préfix** : `/`
    
    __[`Serveur Discord`](https://discord.gg/qsPrUjVCn5)__''', color=0x5865F2)

    embed.add_field(name = '''\📌 Informations Générales''', value = f'''> » **Créateur** : `Sirop2Menthe_#9999`
    > » **Développeurs** : `Sirop2Menthe_#9999` ; `berchbrown#4507`.''', inline = True)

    embed.add_field(name = '''\📊 Statistiques''', value = f'''> » **Serveurs** : `{str(servers_count)}`
    > » **Utilisateurs** : `{total_members}`
    > » **Commandes** : `52`''', inline = False)

    embed.add_field(name = '''\🔧 Informations sur Système''', value = f'''> » **Hébergeur** : [`OuiHeberg`](https://www.ouiheberg.com/)
    > » **Plateforme** : `VPS Linux - 04`
    > » **Processeur** : `3.30 GHz 2 vCore(s) Xeon® E5`
    > » **Mémoire RAM** : `Undefined / 4000.00 MB`''', inline = False)

    embed.add_field(name = '''\👾 Informations sur le Bot''', value = f'''> » **Temps de Connexion** : `{str(uptime)}`
    > » **DataBase** : `Undefined`
    > » **Discord.py** : `V2.2.0`
    > » **Version du Bot** : `V0.0.5`
    > » **ID** : `962051231973511318`''', inline = False)
    
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.timestamp = datetime.utcnow()
    await interaction.response.send_message(embed = embed)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/botinfo` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

# Type : Command
# Name : UpTime
# --- Start Here --- #

@tree.command(name='uptime', description='Affiche le temps de Connexion du bot.')
async def uptime(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    if not author_member.roles or 1081272403465875516 not in [role.id for role in author_member.roles]:
        await interaction.response.send_message(f'''<a:No:1081720631390916778> `FAILURE` : Vous n'avez pas la permission d'utiliser cette commande.''')
        return

    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count

    global startTime
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(timedelta(seconds=difference))

    embed = discord.Embed(title=f'Informations sur le Bot', 
                          description = f'''> Pour plus d'informations sur le bot, cliquez __[`ici`](https://palalink.fr/help-bot)__.
    » **Ping** : `{round(bot.latency * 1000)}ms`
    » **Commandes** : `52`
    » **Préfix** : `/`
    
    __[`Serveur Discord`](https://discord.gg/qsPrUjVCn5)__''', color=0x5865F2)

    embed.add_field(name = '''\👾 Informations sur le Bot''', value = f'''> » **Temps de Connexion** : `{str(uptime)}`
    > » **DataBase** : `Undefined`
    > » **Discord.py** : `V2.2.0`
    > » **Version du Bot** : `V0.0.5`
    > » **ID** : `962051231973511318`''', inline = False)
    
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/1080595360247980032/b666845d51300504e7a4551258c39712.png?size=128')
    embed.timestamp = datetime.utcnow()
    await interaction.response.send_message(embed = embed)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/uptime` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

# Type : Command
# Name : UserInfo
# --- Start Here --- #

@tree.command(name='userinfo', description='Donne des informations sur un membre du serveur.')
async def userinfo(interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
    if member is None:
        author_member = interaction.user
    else:
        author_member = member

    user_flags = author_member.public_flags

    badges = []
    if user_flags.hypesquad_bravery:
        badges.append("<:HypeSquad_Bravery:1081778251078316154>")
    if user_flags.hypesquad_brilliance:
        badges.append("<:Hypesquad_Brilliance:1081778115262558260>")
    if user_flags.hypesquad_balance:
        badges.append("<:HypeSquad_Balance:1081778112154574898>")
    if user_flags.partner:
        badges.append("<:Partner:1081916590045544528>")
    if user_flags.bug_hunter:
        badges.append("<:BugHunter:1081916587596054633>")
    if user_flags.verified_bot:
        badges.append("<:BotVerif:1081916586375532594>")
    if author_member.premium_since is not None:
        badges.append("<a:NitroBoost:1081919862814814208>")

    embed = discord.Embed(title=f'Informations sur {author_member.name}', 
                          description = f'''> Créez vous un Profil sur notre site ! Cliquez __[`ici`](https://palalink.fr/profil)__.
    __[`Serveur Discord`](https://discord.gg/qsPrUjVCn5)__''', color=0x5865F2)

    embed.add_field(name = '''\📌 Informations Générales''', value = f'''> » **Pseudo** : `{author_member.name}#{author_member.discriminator}`
    > » **ID** : `{author_member.id}`.
    > » **Créé le** : <t:{int(author_member.created_at.timestamp())}:D>.
    > » **Badge(s)** : {" ".join(badges)}''', inline = True)

    embed.add_field(name = '''\⚡ Informations sur le Serveur''', value = f'''> » **Rôles ({len(author_member.roles) - 1})** : {", ".join([role.mention for role in author_member.roles[1:]]) if len(author_member.roles) > 1 else "Aucun"}
    > » **Rejoint le** : <t:{int(author_member.joined_at.timestamp())}:D>.
    > » **Surnom** : {author_member.nick if author_member.nick else "Aucun"}''', inline = False)

    embed.set_thumbnail(url=author_member.avatar.url)
    if author_member.banner:
        embed.set_image(url=author_member.banner.url)

    await interaction.response.send_message(embed=embed)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/userinfo` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')


# --- End Here --- #

# Type : Command
# Name : Suggestio
# --- Start Here --- #

@tree.command(name='suggestion', description='Suggérer une amélioration au Bot ou au Site.')
async def suggestion(interaction: discord.Interaction, suggestion: str):
    author_member: discord.Member = interaction.user
    suggestions_channel = interaction.guild.get_channel(1081294532781559881)
    
    embed = discord.Embed(
        title='Nouvelle suggestion', 
        description=f'''> » **Auteur** : `{author_member}`
    
    ```
    {suggestion}
    ```''', 
        color=0x5865F2
    )

    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=author_member.avatar.url)

    message = await suggestions_channel.send(embed=embed)
    await message.add_reaction('<a:Yes:1081365228173938808>')
    await message.add_reaction('<a:No:1081916591400308766>')

    if not interaction.responded:
        await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : Votre **suggestion** à été envoyée corractement ! Merci \:D', ephemeral=True)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/suggestion` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')


# --- End Here --- #

# Type : Command
# Name : BugReport
# --- Start Here --- #



# --- End Here --- #

# Type : Command
# Name : Avis
# --- Start Here --- #

@tree.command(name='avis', description='Laisser un avis global !')
async def avis(interaction: discord.Interaction, note: int, commentaire: str):
    author_member: discord.Member = interaction.user
    avis_channel = interaction.guild.get_channel(1081294505019461742)
    
    if note < 0 or note > 20:
        await interaction.response.send_message(f'<a:No:1081916591400308766>  `ERREUR` : La note doit être comprise entre 0 et 20.', ephemeral=True)
        return

    note_emojis = ''
    for i in range(1, 21):
        if i <= note:
            note_emojis += '\🟦'  
        else:
            note_emojis += '\⬜' 

    embed = discord.Embed(
        title='Nouvel avis',
        description=f'''> » **Auteur** : `{author_member}`
    
    **Note** : `{note}/20`
    {note_emojis}
    
    **Commentaire** :
    ```
    {commentaire}
    ```''',
        color=0x5865F2
    )

    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=author_member.avatar.url)

    message = await avis_channel.send(embed=embed)
    await interaction.response.send_message(f'<a:Yes:1081365228173938808>  `SUCCESS` : Votre **avis** a été envoyé correctement ! Merci \:D', ephemeral=True)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/avis` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')


# --- End Here --- #

# Type : Command
# Name : 8ball
# --- Start Here --- #

eight_ball_responses = [
    'C\'est certain.',
    'C\'est décidément ainsi.',
    'Sans aucun doute.',
    'Oui, définitivement.',
    'Vous pouvez vous y fier.',
    'Comme je le vois, oui.',
    'Plus que probablement.',
    'Les perspectives sont bonnes.',
    'Oui.',
    'Les signes pointent vers oui.',
    'Réponse floue, essayez à nouveau.',
    'Demandez à nouveau plus tard.',
    'Mieux vaut ne pas vous le dire maintenant.',
    'Je ne peux pas prédire maintenant.',
    'Concentrez-vous et demandez à nouveau.',
    'Ne compte pas dessus.',
    'Ma réponse est non.',
    'Mes sources disent non.',
    'Les perspectives ne sont pas si bonnes.',
    'Très douteux.'
]

@tree.command(name='8ball', description='Poser une question à la 8ball !')
async def avis(interaction: discord.Interaction, question: str):
    author_member: discord.Member = interaction.user
    
    response = random.choice(eight_ball_responses)
    await interaction.response.send_message(f'''> » **Question** : `{question}`
    > » **Réponse** : `{response}`''', ephemeral = False)

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/8ball` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

# Type : Command
# Name : PalaStatus
# --- Start Here --- #

@tree.command(name='palastatus', description='Affiche les statistiques détaillées du serveur Minecraft Paladium.')
async def palastatus(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    try:
        response = requests.get('https://api.minestat.net/1/paladium/minestat')

        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title='Statistiques détaillées du serveur Minecraft Paladium', color=0x5865F2)
            embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1254638423942996993/gTt8bTt9_400x400.jpg')
            embed.add_field(name='Joueurs en ligne', value=f"{data['current_players']} / {data['max_players']}", inline=False)
            embed.add_field(name='Version', value=data['version'], inline=False)
            embed.add_field(name='Latence', value=f"{data['latency']} ms", inline=False)
            embed.set_footer(text=f"Dernière mise à jour des statistiques: {data['last_online']}")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f'''<a:No:1081720631390916778> `FAILURE` : Désolé, une erreur s'est produite lors de la récupération des statistiques. Le code d'erreur HTTP est \n\n ```{response.status_code}```.''')

    except requests.exceptions.RequestException as e:
        await interaction.response.send_message(f'''<a:No:1081720631390916778> `FAILURE` : Désolé, une erreur s'est produite lors de la récupération des statistiques. Veuillez vérifier votre connexion internet et réessayer plus tard. Erreur détaillée : \n\n ``` 
        {str(e)} 
        ```''')

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/palastatus` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

@tree.command(name='raid', description='Pour lancer un RAID (Fake) !')
async def raid(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user
    guild = interaction.guild
    channel = interaction.channel

    # Envoyer le message initial
    message = await channel.send("Début du raid dans 70 secondes.")

    # Compteur de temps
    time_left = 70
    progress = 0

    while time_left > 0:
        time_left -= 1
        progress = int((1 - time_left / 70) * 100)
        if progress > 100:
            progress = 100
        progress_bar = '[' + '=' * (progress // 3) + ' ' * ((100 - progress) // 3) + ']'
        await message.edit(content=f"> Début du raid dans {time_left//60}:{time_left%60:02d} Progression en cours...({progress}%)\n{progress_bar}")
        await asyncio.sleep(1)

    await message.edit(content="C'était fake, hahaha !")

    channel_log = bot.get_channel(1081294415760474193)
    await channel_log.send(f'''> `/raid` | **{author_member}** ||{author_member.id}|| | __{interaction.channel.mention}__ | **{interaction.guild.name}** ||{interaction.guild.id}||''')

# --- End Here --- #

# Type : Command
# Name : Dé
# --- Start Here --- #

#@tree.command(name='dé', description='Lance un dé !')
#async def dé(interaction: discord.Interaction):
#    author_member: discord.Member = interaction.user
#    
#    # Envoi du message initial
#    message = await interaction.followup(content="Lancement du dé dans 5 secondes !")
#
#    # Compteur de temps
#    time_left = 5
#
#    # Mettre à jour le message toutes les secondes
#    while time_left > 0:
#        time_left -= 1
#        await message.edit(content=f"Lancement du dé dans {time_left} secondes...")
#        await asyncio.sleep(1)
#
#    # Lancer le dé
#    result = random.randint(1, 6)
#
#    # Envoyer le résultat
#    await message.edit(content=f"Le dé a été lancé et a donné {result} !")

# --- End Here --- #

# Type : Command
# Name : PalaInfo
# --- Start Here --- #

@tree.command(name='palainfo', description='Donne des informations sur le serveur Paladium.')
async def palainfo(interaction: discord.Interaction):
    author_member: discord.Member = interaction.user

    embed = discord.Embed(title='Paladium', description='''Le jeu Paladium est un serveur de jeu Minecraft en français qui est très populaire en France et dans d'autres pays francophones. Il s'agit d'un serveur multi-jeux avec une grande communauté active et une économie virtuelle développée.

Le serveur offre une variété de modes de jeu tels que la survie, le PvP, le Skyblock et bien plus encore. Les joueurs peuvent également participer à des événements organisés par les modérateurs et les administrateurs du serveur.

Le serveur Paladium est un lieu de rencontre pour les joueurs de tous âges et de tous horizons, offrant une expérience de jeu en ligne amusante et engageante pour tous ceux qui cherchent à passer du temps dans un environnement virtuel convivial.''', color=0xFF5C00)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1081351461021163631/1082023060045037598/AHadiUwxgaAkwAAAABJRU5ErkJggg.png')

    embed.add_field(name='» Nombre de joueurs', value='Plus de 150 000 joueurs uniques', inline=False)
    embed.add_field(name='» Mini - jeux', value='PvP Faction, Survie Moddée, PaintWars, Rush et bien d\'autres !', inline=False)
    embed.add_field(name='» Liens Utiles', value='__[`PalaWiki`](https://wiki.paladium-pvp.fr)__ ; __[`Discord Officiel`](https://discord.gg/paladium)__ ; __[`Support`](https://discord.gg/Rq2m5y2WCX)__ ; __[`SiteWeb`](https://paladium-pvp.fr)__ ; __[`StatsMinestats`](https://minestats.eu)__ ; __[`TeamSpeak`](tp.paladium-pvp.fr)__.''' , inline=False)

    await interaction.response.send_message(embed=embed)

import requests
from bs4 import BeautifulSoup

@tree.command(name='mc', description='''Affiche les informations d'un joueur minecraft.''')
async def mc(interaction: discord.Interaction, pseudo_minecraft:str):
    author_member: discord.Member = interaction.user

    pseudo_minecraft = 'Sirop2Menthe_'
    url = f'https://fr.namemc.com/search?q={pseudo_minecraft}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        profile = soup.find('div', class_='search-profiles__result')

        if profile:

            profile_url = profile.find('a', class_='search-profiles__result-link')['href']

            skin_url = profile.find('img', class_='search-profiles__result-skin')['src']

            created_at = profile.find('div', class_='search-profiles__result-created').text.strip()

            followers_count = profile.find('div', class_='search-profiles__result-followers').text.strip()


            embed = discord.Embed(title=f'Profil Minecraft de {pseudo_minecraft}', color=0x5865F2)
            embed.set_thumbnail(url=skin_url)
            embed.add_field(name='URL du profil', value=profile_url, inline=False)
            embed.add_field(name='Date de création du compte', value=created_at, inline=False)
            embed.add_field(name='Nombre de followers', value=followers_count, inline=False)
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message(f'''<a:No:1081720631390916778> `FAILURE` : Le profil Minecraft de {pseudo_minecraft} n'a pas été trouvé.''')
    else:
        await interaction.response.send_message(f'''<a:No:1081720631390916778> `FAILURE` : Désolé, une erreur s'est produite lors de la récupération des informations. Le code d'erreur HTTP est \n\n ```{response.status_code}```.''')


bot.run('TOKEN')