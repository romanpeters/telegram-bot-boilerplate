#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot commands
"""
from bot import registry

import logging
import config

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

command = registry.Command()


@command.register(command=["start"], description="Show commands")
def start(update, context):
    with open("bot/templates/commands.txt", "r") as f:
        text = f.read()
    update.message.reply_text(text)
