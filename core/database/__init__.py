"""
資料庫核心
"""
from core.database.base import *
from core.database.mysqldb import _SqlalchemyManager
from core.database.redisdb import _RedisManager
from core.database.orm import *
from core.database.mixins import *


db = _SqlalchemyManager()
redis = _RedisManager()
