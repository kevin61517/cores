"""
伺服器Mysql資料庫封裝
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import delete, select, update
from constants import MYSQL_URL
from src.database.base import DBInterface, TableTypes


class _SqlalchemyManager(DBInterface, TableTypes):
    """Mysql資料庫"""
    def __init__(self):
        self.sync_url = f'mysql:{MYSQL_URL}'
        self.async_url = f'mysql+aiomysql:{MYSQL_URL}'
        self.engine = None
        self.session_factory = None
        self.async_engine = None
        self.async_session_factory = None
        self.Model = declarative_base()

    @property
    def query(self):
        """查詢"""
        return select

    @property
    def delete(self):
        """刪除"""
        return delete

    @property
    def update(self):
        """更新"""
        return update

    @property
    def session(self) -> scoped_session:
        """會話"""
        return scoped_session(self.session_factory)

    async def async_session(self) -> AsyncSession:
        """異步會話"""
        return self.async_session_factory()

    def create_engine(self):
        """建立連建"""
        self.engine = create_engine(self.sync_url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.async_engine = create_async_engine(self.async_url, future=True, echo=True)
        self.async_session_factory = sessionmaker(bind=self.async_engine, class_=AsyncSession)

    async def close_engine(self):
        """關閉連線"""
        self.engine.dispose()
        await self.async_engine.dispose()

    @staticmethod
    def close_session(session):
        """關閉會話"""
        session.close()



