
from atomicwrites import atomic_write
from dateutil.parser import parse
from pathlib import Path
import asyncio
import datetime
import discord
import json
import re

from ..Client import Client
from ..Log import Log
from ..SQL import SQL

class Stats:


    def __init__(self, args):
        self.log = Log()
        self.client = Client()
        self.args = args
        self.sql = SQL()

        # check to see if we have our table or not


    async def on_ready(self):
        if not await self.sql.table_exists('stats'):
            self.log.warning("Stats table not found, creating")
            await self._create_stats_table()
    

    async def on_message(self, message):
        self.log.info("Processing message")
        await self.process_message(message)

        # Did this mention us? Maybe it's a command!      
        self.log.info(f"Regexing content of: {message.content}")
        match_obj = re.match("<@!?(?P<id>\d+)>", message.content)
        if match_obj and match_obj.group('id')==self.client.user.id:
            command = re.sub("^<@!?\d+> *", "", message.content)
            self.log.info(f"Saw a command request: {command}")
            if command.startswith("stats"):
                await self.command_stats(message,command)
            
        self.log.info("Message processed")


    async def process_message(self, message):
        stats_dict = {}
        stats_dict['words'] = len(message.content.split(' '))
        stats_dict['letters'] = len(message.content.replace(" ",""))
        stats_dict['numbers'] = len(re.findall("\d+", message.clean_content))

        # Track URLs and Pictures
        stats_dict['urls'] = 0
        stats_dict['pictures'] = 0
        stats_dict['pixels'] = 0
        stats_dict['bytes'] = 0

        for embed in message.embeds:
            if 'url' in embed:
                stats_dict['urls'] += 1
                if 'thumbnail' in embed:
                    stats_dict['pictures'] += 1
                    stats_dict['pixels'] += embed['thumbnail']['width'] * embed['thumbnail']['height']

        for attachment in message.attachments:
            if 'width' in attachment and 'height' in attachment:
                stats_dict['pictures'] += 1
                stats_dict['pixels'] += attachment['width'] * attachment['height']

            if 'size' in attachment:
                stats_dict['bytes'] += attachment['size']
        
        stats_dict['mentions'] = 0
        if len(message.mentions):
            stats_dict['mentions'] += len(message.mentions)
        
        self.log.info(f"Saw {stats_dict['words']} words")
        self.log.info(f"Saw {stats_dict['letters']} letters")
        self.log.info(f"Saw {stats_dict['numbers']} numbers")
        self.log.info(f"Saw {stats_dict['mentions']} mentions")
        self.log.info(f"Saw {stats_dict['urls']} urls")
        self.log.info(f"Saw {stats_dict['pictures']} pictures")
        self.log.info(f"Saw {stats_dict['pixels']} pixels")
        self.log.info(f"Saw {stats_dict['bytes']} bytes")

        # Get stats from the SQL db
        cur = self.sql.cur
        cmd = "SELECT * FROM stats WHERE user_id=:user_id AND server_id=:server_id"
        user = cur.execute(cmd,{"server_id":message.server.id,"user_id":message.author.id}).fetchone()
        if not user:
            # Create out new user!
            self.log.info(f"New user creation event: {message.author.name}")
            cmd = "INSERT INTO stats (user_id, server_id) VALUES (:user_id, :server_id)"
            cur.execute(cmd, {"server_id":message.server.id,"user_id":message.author.id})
            await self.sql.commit()
            cmd = "SELECT * FROM stats WHERE user_id=:user_id AND server_id=:server_id"
            user = cur.execute(cmd,{"server_id":message.server.id,"user_id":message.author.id}).fetchone()

        self.log.info(user)
        # Update them
        for key in stats_dict:
            if key in user:
                self.log.info(f"Update {key}!")
                user[key] += stats_dict[key]
        # commit them
        #self.log.info(f"Keys: {user.keys()}")
        #self.log.info(f"Values: {user.values()}")
        cmd = """
            UPDATE stats 
            SET
                messages = messages + 1,
                words = :words,
                letters = :letters,
                numbers = :numbers,
                mentions = :mentions,
                mentioned = :mentioned,
                urls = :urls,
                pictures = :pictures,
                pixels = :pixels,
                bytes = :bytes
            WHERE
                user_id = :user_id AND server_id = :server_id
                """
        cur.execute(cmd,user)
        await self.sql.commit()


    async def _create_stats_table(self):
        cmd = """    
            CREATE TABLE IF NOT EXISTS stats
            (
                user_id TEXT,
                server_id TEXT,
                messages INTEGER DEFAULT 0,
                words INTEGER DEFAULT 0,
                letters INTEGER DEFAULT 0,
                numbers INTEGER DEFAULT 0,
                mentions INTEGER DEFAULT 0,
                mentioned INTEGER DEFAULT 0,
                urls INTEGER DEFAULT 0,
                pictures INTEGER DEFAULT 0,
                pixels INTEGER DEFAULT 0,
                bytes INTEGER DEFAULT 0,
                UNIQUE(user_id,server_id)
            )"""

        cur = self.sql.cur
        cur.execute(cmd)
        await self.sql.commit()


    async def command_stats(self, message, command):
        self.log.info("Process the stats command")

        match_list = re.findall("<@!?(\d+)>", message.content)
        self.log.info(match_list)

        if len(match_list) == 1:
            # If we didn't get a list, give the authors stats back
            match_list.append(message.author.id)

        # Process the list
        for _id in match_list[1:]:
            self.log.info(f"Find stats for {_id}")
            cur = self.sql.cur
            cmd = "SELECT * FROM stats WHERE user_id=:user_id AND server_id=:server_id"
            user = cur.execute(cmd,{"server_id":message.server.id,"user_id":_id}).fetchone()

            if user is None:
                self.log.warning("We cannot pull stats from a user that doesn't exist!")
                continue

            self.log.info(user)

            user_obj = await self.client.get_user_info(_id)

            embed = discord.Embed(title=user_obj.name, description="User Stats")

            embed.add_field(name="Messages", value=user['messages'], inline=True)
            embed.add_field(name="Words", value=user['words'], inline=True)
            embed.add_field(name="Letters", value=user['letters'], inline=True)
            embed.add_field(name="Numbers", value=user['numbers'], inline=True)
            embed.add_field(name="mentions", value=user['mentions'], inline=True)
            # embed.add_field(name="mentioned", value=user['mentioned'], inline=True)
            embed.add_field(name="urls", value=user['urls'], inline=True)
            embed.add_field(name="pictures", value=user['pictures'], inline=True)
            embed.add_field(name="pixels", value=user['pixels'], inline=True)
            embed.add_field(name="bytes", value=user['bytes'], inline=True)

            await self.client.send_message(message.channel, embed=embed)

