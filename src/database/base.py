"""
資料庫Interface
"""
import abc
from sqlalchemy import Column, Integer, Boolean, String, Numeric, DateTime, func


class TableTypes:
    """資料表欄位、欄位類型"""
    Column = Column
    Integer = Integer
    Boolean = Boolean
    String = String
    Numeric = Numeric
    DateTime = DateTime
    func = func


class DBInterface(abc.ABC):
    """資料庫Interface"""
    @abc.abstractmethod
    def create_engine(self):
        """啟動連線"""

    @abc.abstractmethod
    def close_engine(self):
        """關閉連線"""
