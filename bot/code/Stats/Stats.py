
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
        cur = self.sql.cur
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='user_stats'"
        if not cur.execute(cmd).fetchone():
            self.log.warning("Didn't find our table, create it!")



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
        
        mentions = 0
        if len(message.mentions):
            mentions += len(message.mentions)
        
        self.log.info(f"Saw {stats_dict['words']} words")
        self.log.info(f"Saw {stats_dict['letters']} letters")
        self.log.info(f"Saw {stats_dict['numbers']} numbers")
        self.log.info(f"Saw {stats_dict['mentions']} mentions")
        self.log.info(f"Saw {stats_dict['total_urls']} total_urls")
        self.log.info(f"Saw {stats_dict['total_pictures']} total_pictures")
        self.log.info(f"Saw {stats_dict['total_pixels']} total_pixels")
        self.log.info(f"Saw {stats_dict['total_bytes']} total_bytes")

        # Get stats from the SQL db
        # Update them
        # commit them

