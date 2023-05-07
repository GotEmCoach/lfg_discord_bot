import discord
import os

TOKEN = os.getenv("TOKEN")
THREE_NEED = ["dungeons", "hunts", "nightfalls", "seasonal-content", "strikes", "exotic-quests"]
SIX_NEED = ["root-of-nightmares"]

class lfg_bot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('--------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith("lfg"):
            if message.channel.name in THREE_NEED:
                await message.reply("Setting you up with group now, please wait for private thread")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = lfg_bot(intents=intents)
client.run(TOKEN)