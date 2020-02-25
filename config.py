try:
    import redacted
except ImportError:
    print("No redacted.py found. Create your own, or add your values to config.py")
import logging

BOT_TOKEN = redacted.BOT_TOKEN
ADMINS = []
WHITELIST_CHATS = []
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO
