

import discord
import asyncio

from ..Log import Log

class Quote:


    def __init__(self):
        self.log = Log()


    async def on_message(self, message):
        self.log.debug("on_message")

        # Check if we were given a command
        """
            Add a new quote:@bot quote @user the quote
            Quote randomly from a user: @bot quote @user 
            Say a specific quote: @bot quote ####
        """
