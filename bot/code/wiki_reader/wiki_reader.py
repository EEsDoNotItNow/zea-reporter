
from dateutil.parser import parse
import asyncio
import datetime
import discord
import feedparser
import re

from ..client_mgr import client

class Wiki_Reader:

    def __init__(self):
        client.loop.create_task(self.check_atom())
        self.last_check = datetime.datetime.utcnow()
        pass


    async def check_atom(self):
        await asyncio.sleep(5)
        new_last_check = datetime.datetime.utcnow()
        # print("\nChecking RSS")
        d = feedparser.parse("http://192.243.108.252/w/api.php?hidebots=1&urlversion=1&days=7&limit=50&action=feedrecentchanges&feedformat=atom")
        for entry in d['entries']:
        
            """
            Valid keys are:
                id
                guidislink
                link
                title
                title_detail
                links
                updated
                updated_parsed
                summary
                summary_detail
                authors
                author_detail
                author
            """

            date_of_entry = parse(entry['updated'], ignoretz=True)

            if date_of_entry > self.last_check:
                for key in entry:
                    print(f"{key}:{entry[key]}")
                                
                color = discord.colour.Color(0).teal()


                message = discord.Embed(title=entry['title'],
                    colour=color,
                    timestamp=date_of_entry,
                    url=entry['link'])

                message.add_field(name="Author",value=entry['author'])

                summary = re.match("<p>(.{1,})</p>", entry['summary_detail']['value'])
                if summary:
                    print("Add a summery!")
                    print(summary.groups(0)[0])
                    message.add_field(name="Summary", value=summary.groups(0)[0])

                channel = client.get_channel("439882864247570435")
                
                await client.send_message(destination=channel, embed=message)



        self.last_check = new_last_check
        client.loop.create_task(self.check_atom())
        
