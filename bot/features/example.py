#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot features that aren't commands
"""
import logging
from telegram import InlineQueryResultArticle
from bot import registry, access

logger = logging.getLogger(__name__)
message_text = registry.MessageText()  # decorator for message actions
inlinequery = registry.InlineQuery()  # decorator for inline queries


# The order of the decorators is important
# Decorators run in reverse order, so access first, then registry
@message_text.register(pattern="?")  # register a text message action
@access.admin  # restrict access to certain groups
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


@inlinequery.register(pattern="test")
def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    inline_results = []
    for i in range(5):
        result = InlineQueryResultArticle(
            id=i,
            title=i,
            description=query,
        )
        inline_results.append(result)

    update.inline_query.answer(inline_results)
