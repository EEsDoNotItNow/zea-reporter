
import asyncio
import datetime
import feedparser

from ..client_mgr import client

class Wiki_Reader:

    def __init__(self):
        client.loop.create_task(self.check_atom())
        self.last_check = datetime.datetime.now()
        pass


    async def check_atom(self):
        await asyncio.sleep(5)
        print("Check...")
        client.loop.create_task(self.check_atom())
        
