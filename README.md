## Telegram bot

Python telegram bot template

Inspired by Flask, this template uses decorators to route commands.
The template also provides Docker/docker-compose support, database integration, user registration and access level restrictions.
You can add your commands to a Python file in the `bot/commands` directory.
```
from bot.registry import Command, WHITELISTED

command = Command()

@command.register(command=["beep"], access=WHITELISTED)
def boop(update, context):
    """Boops if you beep, but only if you're whitelisted"""
    update.message.reply_text("boop")
```
