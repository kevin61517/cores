"""
伺服器Redis資料庫封裝
"""
from typing import Optional
from redis import Redis, ConnectionPool
import aioredis
from ..database.base import DBInterface
from constants import REDIS_HOST, REDIS_PORT


class _RedisManager(DBInterface):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db_=0):
        self._redis_url = f'redis://{host}:{port}'
        self.db = db_

        self._sync_pool: Optional[ConnectionPool] = None
        self._sync_redis: Optional[Redis] = None

        self._async_pool: Optional[aioredis.ConnectionPool] = None
        self._async_redis: Optional[aioredis.Redis] = None

    def create_engine(self):
        """啟動引擎"""
        self._sync_connect()
        self._async_connect()

    async def close_engine(self):
        """關閉引擎"""
        self._sync_close()
        await self._async_close()

    def choose(self, db: int):
        pool = ConnectionPool.from_url(self._redis_url, decode_responses=True, encoding='utf-8')
        return Redis(connection_pool=pool, db=db)

    def _sync_connect(self):
        """創建同步連線"""
        self._sync_pool = ConnectionPool.from_url(self._redis_url, decode_responses=True, encoding='utf-8')
        self._sync_redis = Redis(connection_pool=self._sync_pool, db=self.db)

    def _async_connect(self):
        """創建異步連線"""
        self._async_pool = aioredis.ConnectionPool.from_url(self._redis_url, decode_responses=True, encoding='utf-8')
        self._async_redis = aioredis.Redis(connection_pool=self._async_pool, db=self.db)

    def _sync_close(self):
        """關閉同步連線"""
        if self._sync_pool is not None:
            self._sync_redis.close()
            self._sync_pool.disconnect()

    async def _async_close(self):
        """關閉異步連線"""
        if self._async_pool is not None:
            await self._async_redis.close()
            await self._async_pool.disconnect()

    @property
    def sync_(self):
        """同步調用"""
        return self._sync_redis

    @property
    def async_(self) -> aioredis.Redis:
        """異步調用"""
        return self._async_redis


redis = _RedisManager()
