
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
        stats_dict = {}
        stats_dict['words'] = len(message.content.split(' '))
        stats_dict['letters'] = len(message.content.replace(" ",""))
        stats_dict['numbers'] = len(re.findall("\d+", message.clean_content))

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
        
        self.log.info(f"Saw {stats_dict['words']} words")
        self.log.info(f"Saw {stats_dict['letters']} letters")
        self.log.info(f"Saw {stats_dict['numbers']} numbers")
        self.log.info(f"Saw {mentions} mentions")
        self.log.info(f"Saw {total_urls} total_urls")
        self.log.info(f"Saw {total_pictures} total_pictures")
        self.log.info(f"Saw {total_pixels} total_pixels")
        self.log.info(f"Saw {total_bytes} total_bytes")

        user = User(message.author)
        user.update(stats_dict)


class User:

    def __init__(self, user):
        self.user = user


    def update(self, stats_dict):
        """Given a stats dictionary, update the values in the JSON

        Note that this function is NOT ASYNC! This lets us guarentee that the read/write cycle is single threaded!
        """

        # Attempt to load file, or make a new one
        # TODO: We could check to see if we are talking to a member, and if so, get user.server.id to call it up. 
        # This would also mean we need to handle creation of folders, which means we should proabably detect
        # where we are in the file system before blasting those out.
        user_file = Path(f"users/stats/{self.user.id}.json")

        if user_file.is_file():
            # Load stats from file
            with open(user_file,'r') as fp:
                user_data = json.load(fp)
        else:
            user_data = {}
            user_data['name'] = user.name
            user_data['discriminator'] = user.discriminator
            user_data['created_at'] = user.created_at
            user_data['display_name'] = user.display_name
            user_data['stats'] = {}

        # Update values as needed
        for key in stats_dict:

            if key in user_data['stats']:
                user_data['stats'][key] += stats_dict[key]
            else:
                user_data['stats'][key] = stats_dict[key]

        # Write file back to disc
        # TODO: How can we make this safer?
        with atomic_write(user_file, overwrite=True) as fp:
            json.dump(user_data,fp,indent=4)




