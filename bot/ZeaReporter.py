#!/usr/bin/env python

import os
import argparse

from . import __version__

from .code.Client import Client
from .code.WikiReader import WikiReader
from .code.Log import Log

parser = argparse.ArgumentParser(description='Basic Bot Demo')
parser.add_argument('--name',
                    default="Zea Reporter",
                    help='Name of this bot')
parser.add_argument('--token',
                    help='Token to use to login')

args = parser.parse_args()

log = Log(args)

log.info(args)

log.info(f"Booting under version {__version__}")

# We break normal patterns here, and begin importing the rest of the bot after logging and parsing is done!


x = Client()

#################################
### Register all modules here ###
#################################

x.register(WikiReader(args))


if args.token:
    log.info("Using token from args")
    x.run(args.token)
elif os.environ.get('CLIENT_TOKEN', None):
    log.info("Using token from ENV")
    x.run(os.environ['CLIENT_TOKEN'])
else:
    log.critical("No token was given in the arguments or the ENV!")
    raise RuntimeError("No valid token given, cannot start bot!")
