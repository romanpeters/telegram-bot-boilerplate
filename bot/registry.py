"""
This file contains some decorators used to register features to the bot and set access levels
"""
import logging
from functools import wraps
import bot.database as db
import config

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

NOBODY, ADMIN, WHITELISTED, ANYBODY = range(0, 4)
chat_cache = {}


def check_rank(chat_id: int, user) -> int:
    """Returns the user's rank"""
    if f"@{user.username}" in config.ADMINS:
        return ADMIN
    elif chat_id in config.WHITELIST_CHATS:
        return WHITELISTED
    else:
        session = db.Session()
        entry = session.query(db.User).filter_by(user_id=user.id).first()
        session.close()
        if entry:
            return entry.rank
    return ANYBODY


def add_user(chat_id, user) -> bool:
    """Adds new users to db"""
    if chat_cache.get(chat_id):
        if user.id in chat_cache[chat_id]:
            logger.debug(f"Already seen user with id {user.id}")
            return False # already added to db
    else:
        chat_cache[chat_id]: list = []
    logger.debug(f"New user with id {user.id}")
    rank = check_rank(chat_id, user)
    db.user_to_db(user_id=user.id, chat_id=chat_id, username=user.username,
                  first_name=user.first_name, last_name=user.last_name, rank=rank)
    chat_cache[chat_id].append(user.id)
    return True


class BaseRegistrator(object):
    """
    Abstract base class
    """

    def register(self, **options):
        """
        Decorator
        kwargs: registration options
        """

        def decorator(func):
            """
            On decoration
            func: function being decorated
            """
            # register the wrapped function
            self.add_to_all(self.wrapper(func, **options), **options)

        return decorator

    def wrapper(self, func, **options):
        """Wraps around a function to perform actions when it's called"""
        @wraps(func)
        def on_call(update, context):
            user = update.effective_user
            chat_id = update.message.chat_id

            # Add to db
            add_user(chat_id, user)

            # check access level
            if options.get('access', ANYBODY) in [NOBODY, ADMIN, WHITELISTED]:
                if check_rank(user) <= options['access']:
                    return func(update, context)
                else:
                    self.access_denied(update, context)
            else:
                return func(update, context)

        return on_call

    def add_to_all(self, func, **kwargs):
        raise NotImplementedError  # should be inherited

    def access_denied(self, update, context):
        logger.warning(f"{update.effective_user} does not have the required rank to execute")


class Command(BaseRegistrator):
    all = {}  # {command: {"callback": func, **options}}

    def register(self, command: list, description: str, access: int = ANYBODY, **kwargs):
        """Decorator used to register a command"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(command=command, description=description, access=access, **kwargs)

    def add_to_all(self, wrapped_func, **kwargs):
        commands: list = kwargs["command"]

        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()

        # a single function can have multiple commands
        for c in commands:
            options["callback"]: object = wrapped_func
            self.all[c]: dict = options


class MessageText(BaseRegistrator):
    all = {}  # {pattern: {"callback": func, **options}}

    def register(self, regex: str, access=None, **kwargs):
        """Decorator used to register a text action"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(regex=regex, access=access, **kwargs)

    def add_to_all(self, wrapped_func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = wrapped_func

        self.all[wrapped_func.__name__]: dict = options


class InlineQuery(BaseRegistrator):
    all = {}  # {pattern: {"callback": func, **options}}

    def register(self, pattern: str, access=None, **kwargs):
        """Decorator used to register an inline query"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(pattern=pattern, access=access, **kwargs)

    def add_to_all(self, wrapped_func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = wrapped_func

        self.all[wrapped_func.__name__]: dict = options


class CallbackQuery(BaseRegistrator):
    all = {}  # {callback_data: {"callback": func, **options}}

    def register(self, callback_data: str, access=None, **kwargs):
        """Decorator used to register a callback"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(callback_data=callback_data, access=access, **kwargs)

    def add_to_all(self, wrapped_func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = wrapped_func

        self.all[wrapped_func.__name__]: dict = options



