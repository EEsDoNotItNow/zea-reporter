
import asyncio
import datetime
import feedparser
from dateutil.parser import parse

from ..client_mgr import client

class Wiki_Reader:

    def __init__(self):
        client.loop.create_task(self.check_atom())
        self.last_check = datetime.datetime.utcnow()
        pass


    async def check_atom(self):
        await asyncio.sleep(10)
        new_last_check = datetime.datetime.utcnow()
        print("\nChecking RSS")
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
                message = f"{entry['title']} updated by {entry['author']} on {entry['updated']} at {entry['link']}"
                general = client.get_channel("439882864247570435")
                await client.send_message(general, message)


        self.last_check = new_last_check
        client.loop.create_task(self.check_atom())
        
