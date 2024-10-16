import discord, asyncio, json, re, time, random, requests, typing, json, os, uuid, psutil, datetime, pytz
import warnings
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

def read_file(file):
    with open(file, "r") as f:
        return json.load(f)

def write_file(file, var):
    with open(file, 'w') as f:
        json.dump(var, f, indent = 2)

PERM_ADMIN_ID = 1183205593381601380
guild_id = 1180817795064274967

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

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
            print('bio ✔️')
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

@tasks.loop(seconds = 4)
async def bio():
    await bot.wait_until_ready()
    total_members = 0
    for guild in bot.guilds:
        total_members = total_members + guild.member_count
        k_number = "{:.2f}k".format(total_members / 1000)
    status = ['Préfix : /', f'V0.1', f'/help', 'Support 24h/24 7j/7']
    for i in status:
        await bot.change_presence(activity = discord.Game(str(i)))
        await asyncio.sleep(4)

# ------------------------------------------
# description / bio
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
            welcome_channel = guild.get_channel(1180904738078863431)
            await welcome_channel.send(
                f'''Bienvenue {member.mention} sur **Noodle Support** ! Grâce à toi, nous sommes `{guild.member_count}`.''')

# ------------------------------------------
# on_member_join
# ------------------------------------------
#
#
#
        
class select_support_option(discord.ui.View):
    @discord.ui.select(placeholder="Choisir une catégorie...", custom_id="select_support_option", options=[

        SelectOption(label="Partenariats", 
                     value="partenariat",
                     emoji="<:discotoolsxyzicon:1183473665921265816>", 
                     description="Faire une demande de partenariat."),

        SelectOption(label="Aide / Questions", 
                     value="aide", 
                     emoji="<:discotoolsxyzicon7:1183473615015002262>",
                     description="Une question sur le Bot ? Le Discord ? C'est ici !"),

        SelectOption(label="Report Bug", 
                     value="grades", 
                     emoji="<:discotoolsxyzicon24:1183473540356374589>",
                     description="Vous trouvez un bug ? Signalez le ici."),

        SelectOption(label="Récompenses", 
                     value="recompense", 
                     emoji="<:discotoolsxyzicon2:1183473664079953991>",
                     description="Récupérez une récompense que vous avez gagné.")
    ])
    async def callback(self, interaction: Interaction, select: discord.ui.Select):
        pass


@tree.command(name="panel_support", description="Panel de support")
@discord.app_commands.checks.has_role(1180819110133764147)
async def panel_support(interaction: Interaction):
    role_support = discord.utils.get(interaction.guild.roles, id=1183204421795065897)

    embed = discord.Embed(
        color=0XFFFFFF,
        title="\🔧 Ouvrir un Ticket de Support",
        description=f"""**Support NoodleBot**

        Pour toute demande nécessitant l'intervention du <@&1183204421795065897>, n'hésitez pas à créer un ticket en cliquant sur l'une des catégories correspondantes !*
        
        > `Attention :` *Tout abus de demande de support sera sanctionné.*"""
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1181292316892348429/1185332824270716968/Frame_8.png?ex=658f3a37&is=657cc537&hm=c8f396a4ad8bb4ee125f65b6dbc585dbd690d1956b9d1c1aa3a591bf2a998460&")
    await interaction.response.send_message("Embed envoyé !", ephemeral=True)
    await interaction.channel.send(embed=embed, view=select_support_option())


class button_close(ui.View):
    @discord.ui.button(label="Fermer", style=discord.ButtonStyle.red, custom_id="close_support", emoji="<:discotoolsxyzicon22:1183473542692618362>")
    async def button(self, interaction: Interaction, button: discord.ui.Button):
        pass


class modal_partenariat(ui.Modal, title="Partenariats"):
    mention = ui.TextInput(label="Quelle mention souhaitez-vous ?", style=discord.TextStyle.short,
                           placeholder="Ex: @everyone", required=True, max_length=32)
    giveaway = ui.TextInput(label="Voulez-vous faire un giveaway ?", style=discord.TextStyle.short,
                            placeholder="Oui / Non", required=True, max_length=3)
    gain = ui.TextInput(label="Si oui, quel en serait le gain ?", style=discord.TextStyle.short,
                        placeholder="Ex: x1 Nitro Boost (9,99€)", required=False, max_length=32)
    duration = ui.TextInput(label="Si oui, quelle en serait la durée ?", style=discord.TextStyle.short,
                            placeholder="Ex: 7 jours", required=False, max_length=32)
    lien = ui.TextInput(label="Lien de votre serveur", style=discord.TextStyle.short,
                        placeholder="Ex: discord.gg/noodlesupport discord.gg/noodlebetter", required=True, max_length=32)

    async def on_submit(self, interaction: discord.Interaction):
        role_support = discord.utils.get(interaction.guild.roles, id=1183204421795065897)
        role_moderator = discord.utils.get(interaction.guild.roles, id=1183204421795065897)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role_support: discord.PermissionOverwrite(read_messages=True),
            role_moderator: discord.PermissionOverwrite(read_messages=True)
        }

        category = bot.get_channel(1183203095178653706)

        channel = await interaction.guild.create_text_channel(name=f"📜・{interaction.user.name}", overwrites=overwrites,
                                                              category=category)

        embed = discord.Embed(
            color=0XFFFFFF,
            title="<:discotoolsxyzicon:1183473665921265816> Partenariat & Promotions",
            description=f"""> Voici les données transmises de {interaction.user.mention}

            > \- **Mention souhaitée :** `{self.mention.value} `
            > \- **Giveaway ?** `{self.giveaway.value} `
            > \- **Lot :** `{self.gain.value} `
            > \- **Durée :** `{self.duration.value} `
            > \- **Lien du serveur :** `{self.lien.value} `"""
        )

        await channel.send(f"{interaction.user.mention}", embed=embed, view=button_close())

        await interaction.response.edit_message()


class modal_aide(ui.Modal, title="Aide"):
    subject = ui.TextInput(label="Quel est le sujet d'ouverture du ticket ?", style=discord.TextStyle.paragraph,
                           required=True, max_length=1024)
    details = ui.TextInput(label="Détails supplémentaires", style=discord.TextStyle.paragraph,
                           placeholder="Images, Vidéos, Liens externes...", required=False, max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        role_support = discord.utils.get(interaction.guild.roles, id=1183204421795065897)
        role_moderator = discord.utils.get(interaction.guild.roles, id=1183204421795065897)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role_support: discord.PermissionOverwrite(read_messages=True),
            role_moderator: discord.PermissionOverwrite(read_messages=True)
        }

        category = bot.get_channel(1183203095178653706)

        channel = await interaction.guild.create_text_channel(name=f"🔗・{interaction.user.name}", overwrites=overwrites,
                                                              category=category)

        embed = discord.Embed(
            color=0XFFFFFF,
            title="<:discotoolsxyzicon7:1183473615015002262> Aide / Question",
            description=f"""> Voici les données transmises de {interaction.user.mention}"""
        )
        embed.add_field(name="Quel est le sujet d'ouverture du ticket ?", value=f"```{self.subject.value} ```",
                        inline=False)
        embed.add_field(name="Détails supplémentaires", value=f"```{self.details.value} ```", inline=False)

        await channel.send(f"{interaction.user.mention}", embed=embed, view=button_close())

        await interaction.response.edit_message()


class modal_grades(ui.Modal, title="Achat Grade"):
    grade = ui.TextInput(label="Type de bug", style=discord.TextStyle.short,
                         placeholder="Serveur Support, Bot, BotSupport..", required=True, max_length=128)
    duration = ui.TextInput(label="En quoi consiste le bug ?", style=discord.TextStyle.short,
                            placeholder="En mois", required=True, max_length=32)

    async def on_submit(self, interaction: discord.Interaction):
        role_support = discord.utils.get(interaction.guild.roles, id=1183204421795065897)
        role_moderator = discord.utils.get(interaction.guild.roles, id=1183204421795065897)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role_support: discord.PermissionOverwrite(read_messages=True),
            role_moderator: discord.PermissionOverwrite(read_messages=True)
        }

        category = bot.get_channel(1183203095178653706)

        channel = await interaction.guild.create_text_channel(name=f"🔗・{interaction.user.name}", overwrites=overwrites,
                                                              category=category)

        embed = discord.Embed(
            color=0XFFFFFF,
            title="<:discotoolsxyzicon24:1183473540356374589> Report Bug",
            description=f"""> Voici les données transmises de {interaction.user.mention}

            > \-**Type de Bug :** `{self.grade.value} `
            > \-**Description :** `{self.duration.value} `"""
        )

        await channel.send(f"{interaction.user.mention}", embed=embed, view=button_close())

        await interaction.response.edit_message()


class modal_recompense(ui.Modal, title="Récompense"):
    lot = ui.TextInput(label="Quel est le lot gagné ?", style=discord.TextStyle.short, required=True, max_length=256)
    link = ui.TextInput(label="Lien du message de gain", style=discord.TextStyle.short, required=True, max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        role_support = discord.utils.get(interaction.guild.roles, id=1183204421795065897)
        role_moderator = discord.utils.get(interaction.guild.roles, id=1183204421795065897)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            role_support: discord.PermissionOverwrite(read_messages=True),
            role_moderator: discord.PermissionOverwrite(read_messages=True)
        }

        category = bot.get_channel(1183203095178653706)

        channel = await interaction.guild.create_text_channel(name=f"🎁・{interaction.user.name}", overwrites=overwrites,
                                                              category=category)

        embed = discord.Embed(
            color=0XFFFFFF,
            title="<:discotoolsxyzicon2:1183473664079953991> Récompense",
            description=f"""> Voici les données transmises de {interaction.user.mention}

            > \- **Lot gagné :** `{self.lot.value} `
            > \- **Lien du message :** `{self.link.value} `"""
        )

        await channel.send(f"{interaction.user.mention}", embed=embed, view=button_close())

        await interaction.response.edit_message()


class view_confirm_close(discord.ui.View):
    @discord.ui.button(label="Oui", style=discord.ButtonStyle.green)
    async def button_(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Vous n'avez pas la permission de faire ça", ephemeral=True)
        await interaction.channel.delete()

    @discord.ui.button(label="Non", style=discord.ButtonStyle.red)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Vous n'avez pas la permission de faire ça", ephemeral=True)
        await interaction.message.delete()

#
#
#

@tree.command(name='panel_notifs', description="Envoyer l'embed des notifs")
@discord.app_commands.checks.has_role(PERM_ADMIN_ID)
async def send_notifs_embed(interaction: discord.Interaction):
    e = discord.Embed(title='''\📚 Obtenir des "rôles notifications''',
                      description='''*Afin d'éviter que vous receviez un grand nombre de mentions non désirées, nous mettons en place un système de rôle de notifications.* <:discotoolsxyzicon24:1183473540356374589>''',
                    color=0xFFFFFF)
    e.set_footer(text="Passez une excellente journée sur le NoodleSupport. ")

    view = discord.ui.View()
    button = discord.ui.Button(label="🔧 Patch Notes", 
                               style=discord.ButtonStyle.secondary, 
                               custom_id=f"edit_role//enchere")
    view.add_item(button)
    button = discord.ui.Button(label="📨 News Discord", 
                               style=discord.ButtonStyle.secondary, 
                               custom_id=f"edit_role//events")
    view.add_item(button)
    button = discord.ui.Button(label="🧭 Actualités", 
                               style=discord.ButtonStyle.secondary, 
                               custom_id=f"edit_role//news")
    view.add_item(button)
    button = discord.ui.Button(label="🎉 Giveaways", 
                               style=discord.ButtonStyle.secondary,
                               custom_id=f"edit_role//giveaways")
    view.add_item(button)
    button = discord.ui.Button(label="📌 Annonces", 
                               style=discord.ButtonStyle.secondary,
                               custom_id=f"edit_role//annonces")
    view.add_item(button)
    await interaction.response.send_message("Embed sent !", ephemeral=True)
    await interaction.channel.send(embed=e, view=view)

# -------------------------------------
# INTERACTON EVENT
# -------------------------------------

@bot.event
async def on_interaction(interaction):
    try:
        custom_id = interaction.data['custom_id']
    except:
        custom_id = " "
    if custom_id.split("//")[0] == "edit_role":
        tableau = {
        "enchere": 1185338381937430609,
        "events": 1185338388308566077,
        "news": 1185338390976139375,
        "giveaways": 1185338393891184711,
        "annonces": 1185338398362320958
        }
        role_id = tableau[custom_id.split("//")[1]]
        role = discord.utils.get(bot.get_guild(guild_id).roles, id=role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"> » Le role {role.mention} vous a bien été retiré", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"> » Le role {role.mention} vous a bien été ajouté", ephemeral=True)

    # partie support
    if custom_id.split("//")[0] == "select_support_option":
        user = interaction.user

        if interaction.data["values"][0] == "partenariat":
            await interaction.response.send_modal(modal_partenariat())
        if interaction.data["values"][0] == "aide":
            await interaction.response.send_modal(modal_aide())
        if interaction.data["values"][0] == "grades":
            await interaction.response.send_modal(modal_grades())
        if interaction.data["values"][0] == "recompense":
            await interaction.response.send_modal(modal_recompense())

    if custom_id.split("//")[0] == "close_support":
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Vous n'avez pas la permission de faire ça", ephemeral=True)
        await interaction.response.send_message("Voulez-vous vraiment fermer le ticket ?", view=view_confirm_close())
  
bot.run('TOKEN')