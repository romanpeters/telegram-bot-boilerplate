#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram bot
"""
import os
import logging
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

import config
import bot.commands
import bot.features
from bot import registry

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.info(update)
    logger.warning(context.error)


def run():
    """Start the bot."""
    bot_token = config.BOT_TOKEN

    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands
    [dp.add_handler(CommandHandler(command=key, callback=value["callback"])) for key, value in registry.Command.all.items()]

    # message text actions
    [dp.add_handler(MessageHandler(filters=Filters.regex(value["regex"]), callback=value["callback"])) for value in registry.MessageText.all.values()]

    # on inline queries
    [dp.add_handler(InlineQueryHandler(pattern=value["pattern"], callback=value["callback"])) for value in registry.InlineQuery.all.values()]

    # on callback queries
    [dp.add_handler(CallbackQueryHandler(pattern=value["pattern"], callback=value["callback"])) for value in registry.CallbackQuery.all.values()]

    # log all errors
    dp.add_error_handler(error)

    # write documentation
    man = "\n".join([f"/{key} - {value['description']}" for key, value in registry.Command.all.items()])

    # Ensure bot/templates
    template_dir = "bot/templates"
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    with open(f"{template_dir}/commands.txt", "w+") as f:
        f.write(man)

    logger.info(f"Commands {list(registry.Command.all.keys())}")
    logger.info(f"MessageTexts {list(registry.MessageText.all.keys())}")
    logger.info(f"InlineQueries {list(registry.InlineQuery.all.keys())}")
    logger.info(f"Callbacks {list(registry.CallbackQuery.all.keys())}")

    # Start the Bot

    updater.start_polling()
    logger.info("~BOT IS ONLINE!~")
    updater.idle()

