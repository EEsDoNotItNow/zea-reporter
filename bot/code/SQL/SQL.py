
import asyncio

from ..Singleton import Singleton
from ..Log import Log

class SQL(metaclass=Singleton):

    def __init__(self, db_name):
        self.db_name = db_name
        self.log = Log()
        self._commit_in_progress = False


    async def commit(self, now=False):
        # Schedule a commit in the future
        # Get loop from the client, schedule a call to _commit and return
        pass


    async def _commit(self, now=False):

        if self._commit_in_progress:
            return
        self._commit_in_progress = True
        asyncio.sleep(30)
        # Commit SQL
        self._commit_in_progress = False


