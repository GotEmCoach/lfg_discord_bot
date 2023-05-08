import discord
import os
import re

TOKEN = os.getenv("TOKEN")
THREE_NEED = [
    "dungeons",
    "hunts",
    "nightfalls",
    "seasonal-content",
    "strikes",
    "exotic-quests"
    ]
SIX_NEED = [
    "root-of-nightmares",
    "kings-fall",
    "vow-of-the-disciple",
    "vault-of-glass",
    "deep-stone-crypt",
    "lastwish",
    "dares-of-eternity"
    ]
PLAYER_TYPES_RE = re.compile(r"titan|hunter|warlock|[ ]w[ ]|[ ]t[ ]|[ ]h[ ]", re.IGNORECASE)
POWER_TYPES_RE = re.compile(r"void|solar|arc|strand|stasis|[ ]v[ ]|[ ]s[ ]|[ ]a[ ]|[ ]str[ ]|[ ]sta[ ]", re.IGNORECASE)
DIFF_TYPES_RE = re.compile(r"normal|hero|legend|master|grandmaster|[ ]1[ ]|[ ]2[ ]|[ ]3[ ]|[ ]4[ ]", re.IGNORECASE)
KEYWORDS_RE = re.compile(r"only|new|stage \S.+\s|teaching|learning|challenge|veteran", re.IGNORECASE)

class lfg_bot(discord.Client):    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('--------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith("lfg"):
            if message.channel.name in THREE_NEED:
                player = build_persona(message, 3)

    async def build_persona(message: discord.Message, member_count):
        player = {}
        player_type = re.match(PLAYER_TYPES_RE, message.content.split("wants")[0])
        wants = re.findall(PLAYER_TYPES_RE, message.content.split("wants")[1])



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = lfg_bot(intents=intents)
client.run(TOKEN)