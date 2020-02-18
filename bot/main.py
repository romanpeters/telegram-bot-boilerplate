#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Telegram bot
"""
import logging
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters

from bot import noncommand, command
from bot.redacted import BOT_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    [dp.add_handler(CommandHandler(value, key)) for value, key in command.commands.items()]
    dp.add_handler(CommandHandler("help", command.start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, noncommand.echo))
    dp.add_handler(InlineQueryHandler(noncommand.inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print("Listening...")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
