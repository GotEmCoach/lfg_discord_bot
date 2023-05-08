import discord
import os
import re
from queue import Queue
from datetime import datetime
from collections import OrderedDict
from uuid import uuid4
import asyncio

TOKEN = os.getenv("TOKEN")
THREE_NEED = [
    "dungeons",
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
    def __init__(self):
        self.all_queues = {}
        self.player_roles = {}
        for activity in THREE_NEED:
            self.all_queues[activity] = Queue()
        for activity in SIX_NEED:
            self.all_queues[activity] = Queue()
        self.play_requests = OrderedDict()
        self.process_lock = asyncio.Lock()
        self.player_role_lock = asyncio.Lock()
        self.processing_groups = []

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('--------')

    async def setup_hook(self):
        self.loop.create_task(self.process_made_groups())

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith("lfg"):
            if message.channel.name in THREE_NEED:
                player = await self.build_persona(message)


        if message.content.startswith("setme"):
            player_type = re.search(PLAYER_TYPES_RE, message.content)
            async with self.player_role_lock:
                self.player_roles[message.author.id] = player_type

    async def build_persona(self, message: discord.Message, member_count=3):
        player_request = {}
        activity = message.channel.name
        player_id = message.author.id
        async with self.player_role_lock:
            if player_id not in self.player_roles.keys():
                await message.reply("You have not set your player role, please do via setme.")
                return
            else:
                player_request["roles"] = self.player_roles[player_id]
        difficulty = re.search(DIFF_TYPES_RE, message.content)
        if not difficulty:
            await message.reply("No difficulty indicated")
            return
        player_request["difficulty"] = difficulty
        type_wants = re.findall(PLAYER_TYPES_RE, message.content)
        player_request["type_wants"] = type_wants
        power_wants = re.findall(POWER_TYPES_RE, message.content)
        player_request["power_wants"] = power_wants
        options = re.findall(KEYWORDS_RE, message.content)
        unique_id = uuid4()
        player_request["user"] = player_id
        player_request["activity"] = activity
        if ("teaching") in options:
            player_request["teaching"] = True
            player_request["learning"] = False
            player_request["veteran"] = True
        elif ("learning") in options:
            player_request["teaching"] = False
            player_request["learning"] = True
            player_request["veteran"] = False
        elif ("veteran") in options:
            player_request["veteran"] = True
            player_request["teaching"] = False
            player_request["learning"] = False
        player_request["wants"] = wants
        async with self.process_lock:
            self.play_requests[unique_id] = player_request

    async def process_made_groups(self):


    async def make_groups(self):
        async with self.process_lock:
            for key, value in self.play_requests.items():
                player_request = value
                for processing_group in self.processing_groups:
                    for player in processing_group:
                        if player[]
                        


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = lfg_bot(intents=intents)
client.run(TOKEN)