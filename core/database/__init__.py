"""
資料庫核心
"""
from ..database.base import *
from ..database.mysqldb import _SqlalchemyManager
from ..database.redisdb import _RedisManager
from ..database.orm import *
from ..database.mixins import *


db = _SqlalchemyManager()
redis = _RedisManager()
