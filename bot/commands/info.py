#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot commands
"""
import logging
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context
def start(update, context):
    """Which commands are there?"""
    with open("bot/templates/commands.txt", "r") as f:
        text = f.read()
    update.message.reply_text(text)
