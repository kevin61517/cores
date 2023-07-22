"""
資料庫核心
"""
from src.database.base import *
from src.database.mysqldb import _SqlalchemyManager
from src.database.redisdb import _RedisManager
from src.database.orm import *
from src.database.mixins import *


db = _SqlalchemyManager()
redis = _RedisManager()
