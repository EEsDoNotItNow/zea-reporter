
from dateutil.parser import parse
import asyncio
import datetime
import discord
import feedparser
import re

from ..Log import Log
from ..Client import Client

class WikiReader:

    def __init__(self, args):
        self.log = Log()
        self.client = Client()
        self.args = args

        self.channels = ("439882864247570435","439985698133639168") 
        self.last_check = datetime.datetime.utcnow()
        # client.loop.create_task(self.loop())\


    async def on_ready(self):
        self.log.info("Creating atom checking loop")
        self.client.loop.create_task(self.atom_loop())


    async def atom_loop(self):
        while 1:

            await asyncio.sleep(5)
            new_last_check = datetime.datetime.utcnow()

            # Handle all errors here, we don't want to stop this ever. 
            try:
                await self.check_atom()
            except KeyboardInterrupt:
                self.log.exception("ctrl+c received, die!")
                raise
            except:
                self.log.exception("ckeck_atom threw an error.")

            self.last_check = new_last_check


    async def check_atom(self):
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
                self.log.info("Saw page update, parse and send!")
                # for key in entry:
                #     print(f"{key}:{entry[key]}")
                                
                color = discord.colour.Color(0).teal()


                message = discord.Embed(title=entry['title'],
                    colour=color,
                    timestamp=date_of_entry,
                    url=entry['link'])

                message.add_field(name="Author",value=entry['author'])

                summary = re.match("<p>(.{1,})</p>", entry['summary_detail']['value'])
                if summary:
                    message.add_field(name="Summary", value=summary.groups(0)[0])

                for channel in self.channels:
                    channel = self.client.get_channel(channel)
                    self.log.info(f"Send to {channel}")
                    try:
                        await self.client.send_message(destination=channel, embed=message)
                    except KeyboardInterrupt:
                        self.log.exception("ctrl+c received, die!")
                        raise
                    except:
                        self.log.exception("Error was received, continue!")

