import functools
import logging

logger = logging.getLogger(__name__)


def log_function_call(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling function: {func.__name__}")
        return await func(*args, **kwargs)
    return wrapper
