"""
This file contains decorators which can be used to register functions.
"""
import logging
import config

logging.basicConfig(format=config.LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseRegistrator(object):
    """Abstract base class"""
    def register(self, **kwargs):
        def decorator(func):
            logger.debug(f"Registering {func.__name__} {kwargs}")
            self._add_to_all(func, **kwargs)
            return func
        return decorator

    def _add_to_all(self, func, **kwargs):
        raise NotImplementedError  # should be inherited


class Command(BaseRegistrator):
    all = {}  # {command: {"calback": func, **options}}

    def register(self, command: list, description, **kwargs):
        """Decorator used to register a command"""
        return super().register(command=command, description=description, **kwargs)

    def _add_to_all(self, func, **kwargs):
        commands: list = kwargs["command"]

        # options is the kwargs given in the decorator, except for command
        options = kwargs.copy()
        options.pop("command")

        # a single function can have multiple commands
        for c in commands:
            options["callback"]: object = func
            self.all[c]: dict = options


class MessageText(BaseRegistrator):
    all = {}  # {pattern: {"calback": func, **options}}

    def register(self, pattern: str, **kwargs):
        """Decorator used to register a text action"""
        return super().register(pattern=pattern, **kwargs)

    def _add_to_all(self, func, **kwargs):
        pattern: str = kwargs["pattern"]

        # options is the kwargs given in the decorator, except for pattern
        options = kwargs.copy()
        options.pop("pattern")
        options["callback"]: object = func

        self.all[pattern]: dict = options


class InlineQuery(BaseRegistrator):
    all = {}  # {pattern: {"calback": func, **options}}

    def register(self, pattern: str, **kwargs):
        """Decorator used to register an inline query"""

        return super().register(pattern=pattern, **kwargs)

    def _add_to_all(self, func, **kwargs):
        query: str = kwargs["pattern"]

        # options is the kwargs given in the decorator, except for query
        options = kwargs.copy()
        options.pop("pattern")
        options["callback"]: object = func

        self.all[query]: dict = options


class CallbackQuery(BaseRegistrator):
    all = {}  # {callback_data: {"calback": func, **options}}

    def register(self, callback_data: str, **kwargs):
        """Decorator used to register a callback"""
        return super().register(callback_data=callback_data, **kwargs)

    def _add_to_all(self, func, **kwargs):
        callback_data: str = kwargs["callback_data"]

        # options is the kwargs given in the decorator, except for callback_data
        options = kwargs.copy()
        options.pop("callback_data")
        options["callback"]: object = func

        self.all[callback_data]: dict = options
