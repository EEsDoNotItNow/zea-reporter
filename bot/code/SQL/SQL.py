
import asyncio
import sqlite3

from ..Singleton import Singleton
from ..Log import Log
from ..Client import Client

class SQL(metaclass=Singleton):
    """Manage SQL connection, as well as basic user information
    """

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = self.dict_factory
        self.cur = self.conn.cursor()
        self.log = Log()
        self.client = Client()
        self._commit_in_progress = False


    async def on_ready(self):
        self.log.info("SQL registered to recieve commands!")

        if not await self.table_exists('users'):
            self.log.warning("Users table not found, creating")
            await self._create_user_table()
            
        if not await self.table_exists('servers'):
            self.log.warning("Servers table not found, creating")


    async def on_message(self, message):
        self.log.debug(f"Got message: {message.content}")
        self.log.debug(f"       From: {message.author.name} ({message.author.id})")
        if message.server:
            self.log.debug(f"         On: {message.server} ({message.server.id})")


    async def commit(self, now=False):
        # Schedule a commit in the future
        # Get loop from the client, schedule a call to _commit and return
        self.log.info("Start a commit()")
        asyncio.ensure_future(self._commit(now))
        self.log.info("Finsihed a commit()")


    async def _commit(self, now=False):
        self.log.info("Start a _commit()")
        if self._commit_in_progress:
            self.log.info("Skipped a _commit()")
            return
        self._commit_in_progress = True
        await asyncio.sleep(30)
        # Commit SQL
        self.conn.commit()
        self._commit_in_progress = False
        self.log.info("Finished a _commit()")


    async def _create_user_table(self):
        cmd = """    
                CREATE TABLE IF NOT EXISTS users
                (
                    name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    discriminator TEXT,
                    avatar TEXT,
                    bot BOOLEAN,
                    avatar_url TEXT,
                    default_avatar TEXT,
                    default_avatar_url TEXT,
                    mention TEXT,
                    created_at INTEGER
                )"""
        self.cur.execute(cmd)
        await self.commit()


    async def table_exists(self, table_name):
        cmd = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        if self.cur.execute(cmd).fetchone():
            return True
        return False


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
