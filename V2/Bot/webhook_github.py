import discord, json
from flask import Flask, request
from discord.ext import commands, tasks
from discord import ui, app_commands, Interaction, SelectOption, SelectMenu, ButtonStyle, ActionRow, Button
from discord.app_commands import Choice

app = Flask(__name__)
webhook_url = "https://discord.com/api/webhooks/1198551019328634903/YTwKEPvvJThB1k9hW7A-jj5hNm5AJH8IxuAsq1HR9Re9bz5tPWwojnHdttla_LUOlLAv"

target_channel_id = 1198550943462068254

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '/', intents = discord.Intents.all())
bot.remove_command('help')

if __name__ == '__main__':
    app.run(port=8080)
    bot.run('TOKEN')

class client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True

        print(f'''
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    │  Logged in as {self.user.id} ==> ✔️      │
    │                                             │
    │  {self.user} is  Online ==> ✔️            │
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛''')

bot = client()
tree = app_commands.CommandTree(bot)


@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = json.loads(request.data)
    if 'commits' in data:
        for commit in data['commits']:
            message = f"New commit by {commit['author']['name']} on {data['repository']['name']}:\n{commit['message']}"
            send_discord_message(message)
    return '', 200

def send_discord_message(message):
    bot.loop.create_task(send_message(message))

async def send_message(message):
    await bot.wait_until_ready()

    channel = bot.get_channel(target_channel_id)

    if channel:
        await channel.send(message)
    else:
        print(f"Le canal avec l'ID {target_channel_id} n'a pas été trouvé.")

if __name__ == '__main__':
    app.run(port=5000)

bot.run('TOKEN')