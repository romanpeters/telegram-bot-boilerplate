"""
Decorators for restricting access
"""
import bot.database as db
import config
from functools import wraps

ADMIN, WHITELISTED, PEASANT = range(0, 3)


def check_rank(user) -> int:
    if f"@{user.username}" in config.ADMINS:
        return ADMIN
    else:
        session = db.Session()
        entry = session.query(db.User).filter_by(user_id=user.id).first()
        session.close()
        if entry:
            return entry.rank
    return PEASANT


def everyone(func):
    """Decorator: Rank 2"""
    @wraps(func)
    def decorator(update, context):
        func(update, context)
    return decorator


def whitelist(func):
    """Decorator: Rank 1"""
    @wraps(func)
    def decorator(update, context):
        if check_rank(update.effective_user) <= WHITELISTED:
            func(update, context)
    return decorator


def admin(func):
    """Decorator: Rank 0"""
    @wraps(func)
    def decorator(update, context):
        if check_rank(update.effective_user) == ADMIN:
            func(update, context)
    return decorator


def private(func):
    """Decorator: Private chat only"""
    @wraps(func)
    def decorator(update, context):
        if update.message.chat.type == 'private':
            func(update, context)
        else:
            update.message.reply_text("This command can only be used in private chats")
    return decorator


def group(func):
    """Decorator: Group chat only"""
    @wraps(func)
    def decorator(update, context):
        if update.message.chat.type == 'group':
            func(update, context)
        else:
            update.message.reply_text("This command can only be used in group chats")
    return decorator
