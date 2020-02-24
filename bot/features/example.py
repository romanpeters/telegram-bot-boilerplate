#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot features that aren't commands
"""
import logging
from bot import registry
from bot.registry import ADMIN, WHITELISTED
import config


logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

message_text = registry.MessageText()  # decorator for message actions


@message_text.register(regex=r"^.*?.*$", access=ADMIN)  # regex match if '?' in message
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
