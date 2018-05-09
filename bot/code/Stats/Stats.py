
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
        self.log.info("Message processed")


    async def process_message(self, message):
        stats_dict = {}
        stats_dict['words'] = len(message.content.split(' '))
        stats_dict['letters'] = len(message.content.replace(" ",""))
        stats_dict['numbers'] = len(re.findall("\d+", message.clean_content))

        # Track URLs and Pictures
        stats_dict['total_urls'] = 0
        stats_dict['total_pictures'] = 0
        stats_dict['total_pixels'] = 0
        stats_dict['total_bytes'] = 0

        for embed in message.embeds:
            if 'url' in embed:
                stats_dict['total_urls'] += 1
                if 'thumbnail' in embed:
                    stats_dict['total_pictures'] += 1
                    stats_dict['total_pixels'] += embed['thumbnail']['width'] * embed['thumbnail']['height']

        for attachment in message.attachments:
            if 'width' in attachment and 'height' in attachment:
                total_pictures += 1
                total_pixels += attachment['width'] * attachment['height']

            if 'size' in attachment:
                total_bytes += attachment['size']
        
        stats_dict['mentions'] = 0
        if len(message.mentions):
            stats_dict['mentions'] += len(message.mentions)
        
        self.log.info(f"Saw {stats_dict['words']} words")
        self.log.info(f"Saw {stats_dict['letters']} letters")
        self.log.info(f"Saw {stats_dict['numbers']} numbers")
        self.log.info(f"Saw {stats_dict['mentions']} mentions")
        self.log.info(f"Saw {stats_dict['total_urls']} total_urls")
        self.log.info(f"Saw {stats_dict['total_pictures']} total_pictures")
        self.log.info(f"Saw {stats_dict['total_pixels']} total_pixels")
        self.log.info(f"Saw {stats_dict['total_bytes']} total_bytes")

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
