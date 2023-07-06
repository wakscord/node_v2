from redis.asyncio import ConnectionPool, Redis

from app.common.settings import settings

pool = ConnectionPool(host=settings.REDIS_URL, port=6379, password=settings.REDIS_PASSWORD)
session: Redis = Redis(connection_pool=pool, decode_responses=True)
