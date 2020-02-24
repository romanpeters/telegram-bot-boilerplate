"""
This file contains some decorators used to register features to the bot and set access levels
"""
import logging
from functools import wraps
import bot.database as db
import config

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

ADMIN, WHITELISTED, ANYONE = range(0, 3)


def check_rank(user) -> int:
    """Returns the user's rank"""
    if f"@{user.username}" in config.ADMINS:
        return ADMIN
    else:
        session = db.Session()
        entry = session.query(db.User).filter_by(user_id=user.id).first()
        session.close()
        if entry:
            return entry.rank
    return ANYONE


class BaseRegistrator(object):
    """
    Abstract base class
    """
    def register(self, **options):
        """
        Decorator
        kwargs: registration options
        """

        def on_init(func):
            """
            On decoration
            func: function being decorated
            """
            # register
            self.add_to_all(func, **options)

            @wraps(func)
            def on_call(update, context, *args, **kwargs):
                """
                On function call
                """
                if options.get('access') in [ADMIN, WHITELISTED]:
                    # check access level
                    if check_rank(update.effective_user) <= options['access']:
                        return func(update, context, *args, **kwargs)
                    else:
                        self.access_denied(update, context, func)
            return on_call
        return on_init

    def add_to_all(self, func, **kwargs):
        raise NotImplementedError  # should be inherited

    def access_denied(self, update, context, func):
        logger.warning(f"{update.effective_user} does not have the required rank to execute {func.__name__}")


class Command(BaseRegistrator):
    all = {}  # {command: {"callback": func, **options}}

    def register(self, command: list, description: str, access: int = ANYONE, **kwargs):
        """Decorator used to register a command"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(command=command, description=description, access=access, **kwargs)

    def add_to_all(self, func, **kwargs):
        commands: list = kwargs["command"]

        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()

        # a single function can have multiple commands
        for c in commands:
            options["callback"]: object = func
            self.all[c]: dict = options


class MessageText(BaseRegistrator):
    all = {}  # {pattern: {"callback": func, **options}}

    def register(self, regex: str, access=None, **kwargs):
        """Decorator used to register a text action"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(regex=regex, access=access, **kwargs)

    def add_to_all(self, func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = func

        self.all[func.__name__]: dict = options


class InlineQuery(BaseRegistrator):
    all = {}  # {pattern: {"callback": func, **options}}

    def register(self, pattern: str, access=None, **kwargs):
        """Decorator used to register an inline query"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(pattern=pattern, access=access, **kwargs)

    def add_to_all(self, func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = func

        self.all[func.__name__]: dict = options


class CallbackQuery(BaseRegistrator):
    all = {}  # {callback_data: {"callback": func, **options}}

    def register(self, callback_data: str, access=None, **kwargs):
        """Decorator used to register a callback"""
        # This method is only used to specify parameters and then call the parent method
        return super().register(callback_data=callback_data, access=access, **kwargs)

    def add_to_all(self, func, **kwargs):
        # options is the kwargs given in the decorator + callback
        options = kwargs.copy()
        options["callback"]: object = func

        self.all[func.__name__]: dict = options

