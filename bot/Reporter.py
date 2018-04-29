#!/usr/bin/env python

from code.client_mgr import client

from code.discord_api import on_ready

from code.wiki_reader import Wiki_Reader

import os

reader = Wiki_Reader()

client.run(os.environ['CLIENT_TOKEN'])
