
from dateutil.parser import parse
import asyncio
import datetime
import discord
import re

from ..Log import Log
from ..Client import Client

class Stats:


    def __init__(self, args):
        self.log = Log()
        self.client = Client()
        self.args = args


    async def on_message(self, message):
        self.log.info("Processing message")
        await self.process_message(message)
        self.log.info("Message processed")


    async def process_message(self, message):
        words = len(message.content.split(' '))
        letters = len(message.content.replace(" ",""))
        numbers = len(re.findall("\d+", message.clean_content))

        # Track URLs and Pictures
        total_urls = 0
        total_pictures = 0
        total_pixels = 0
        total_bytes = 0

        for embed in message.embeds:
            if 'url' in embed:
                total_urls += 1
                if 'thumbnail' in embed:
                    total_pictures += 1
                    total_pixels += embed['thumbnail']['width'] * embed['thumbnail']['height']

        for attachment in message.attachments:
            if 'width' in attachment and 'height' in attachment:
                total_pictures += 1
                total_pixels += attachment['width'] * attachment['height']

            if 'size' in attachment:
                total_bytes += attachment['size']
        
        mentions = 0
        if len(message.mentions):
            mentions += len(message.mentions)
        
        self.log.info(f"Saw {words} words")
        self.log.info(f"Saw {letters} letters")
        self.log.info(f"Saw {numbers} numbers")
        self.log.info(f"Saw {mentions} mentions")
        self.log.info(f"Saw {total_urls} total_urls")
        self.log.info(f"Saw {total_pictures} total_pictures")
        self.log.info(f"Saw {total_pixels} total_pixels")
        self.log.info(f"Saw {total_bytes} total_bytes")