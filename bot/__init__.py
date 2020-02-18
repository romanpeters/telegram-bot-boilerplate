#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram bot
"""
import os
import logging
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters

from bot import noncommand
from bot.commands import command_list

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def run(bot_token):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    [dp.add_handler(CommandHandler(c.__name__, c)) for c in command_list]

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, noncommand.echo))
    dp.add_handler(InlineQueryHandler(noncommand.inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # write documentation
    man = "\n".join([f"/{c.__name__} - {c.__doc__}" for c in command_list])
    print(man)
    # Ensure bot/templates
    template_dir = "bot/templates"
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    with open(f"{template_dir}/commands.txt", "w+") as f:
        f.write(man)

    # Start the Bot
    print("Listening...")
    updater.start_polling()
    updater.idle()
