from data.config import ITEMS_MAXSIZE, ITEMS_TTL

from cachetools import TTLCache


__all__ = ['items_cache']

items_cache = TTLCache(maxsize=ITEMS_MAXSIZE, ttl=ITEMS_TTL)
