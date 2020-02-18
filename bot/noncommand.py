#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot features that aren't commands
"""
import logging
from telegram import InlineQueryResultArticle

logger = logging.getLogger(__name__)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

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
