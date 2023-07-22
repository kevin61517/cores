"""
資料庫核心
"""
from .mysqldb import _SqlalchemyManager
from .redisdb import _RedisManager
from .orm import *
from .mixins import *


db = _SqlalchemyManager()
redis = _RedisManager()
