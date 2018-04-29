
import discord
import asyncio

from ..Log import Log

class Client(discord.Client):

    # No __init__ given, just use the base classes one!

    _shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self._shared_state

        self.log = Log()

        # We only init ONCE
        if not hasattr(self, '_inited'):
            super().__init__(*args, **kwargs)
            self.registry = []
            self._inited = True


    
    def register(self, cls):
        """Register a class with our client.
        """
        #TODO: Check if this class is here or not!
        self.registry.append(cls)


    async def on_channel_create(self, channel):
        pass


    async def on_channel_delete(self, channel):
        pass


    async def on_channel_update(self, before, after):
        pass


    async def on_error(self, event, *args, **kwargs):
        pass


    async def on_group_join(self, channel, user):
        pass


    async def on_group_remove(self, channel, user):
        pass


    async def on_member_ban(self, member):
        pass


    async def on_member_join(self, member):
        pass


    async def on_member_remove(self, member):
        pass


    async def on_member_unban(self, server, user):
        pass


    async def on_member_update(self, before, after):
        pass


    async def on_message(self, message):
        self.log.debug("Saw a message")
        pass


    async def on_message_delete(self, message):
        self.log.debug("Saw a message get deleted")
        pass


    async def on_message_edit(self, before, after):
        self.log.debug("Saw a message get edited")
        pass


    async def on_reaction_add(self, reaction, user):
        self.log.debug("Saw a reaction get added")
        pass


    async def on_reaction_clear(self, message, reactions):
        self.log.debug("Saw a reaction get cleared")
        pass


    async def on_reaction_remove(self, reaction, user):
        self.log.debug("Saw a reaction get removed")
        pass


    async def on_ready(self):
        self.log.debug("Ready")
        for module in self.registry:
            try:
                await module.on_ready()
            except:
                pass


    async def on_resumed(self, ):
        self.log.debug("Resumed")
        pass


    async def on_server_available(self, server):
        self.log.debug("Saw a server become available")
        pass


    async def on_server_emojis_update(self, before, after):
        pass


    async def on_server_join(self, server):
        pass


    async def on_server_remove(self, server):
        pass


    async def on_server_role_create(self, role):
        pass


    async def on_server_role_delete(self, role):
        pass


    async def on_server_role_update(self, before, after):
        pass


    async def on_server_unavailable(self, server):
        pass


    async def on_server_update(self, before, after):
        pass


    async def on_socket_raw_receive(self, msg):
        pass


    async def on_socket_raw_send(self, payload):
        pass


    async def on_typing(self, channel, user, when):
        self.log.debug("Saw some typeing")
        pass


    async def on_voice_state_update(self, before, after):
        pass

