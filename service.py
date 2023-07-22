"""
資料庫查詢封裝
"""
from typing import Optional
from .database import db, ORMObject
from .exceptions import DBOptionError


class Service:

    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """檢查model是否伺服器配置的相同"""
        rv = isinstance(model, (ORMObject, self.__model__))
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    @staticmethod
    def _preprocess_params(kws):
        return kws

    def save(self, model) -> Optional[ORMObject]:
        """儲存資料"""
        self._isinstance(model)
        session = db.session
        try:
            session.add(model)
            session.flush()
            session.commit()
            instance: ORMObject = model.get_instance()
        except Exception as e:
            session.rollback()
            instance = None
            raise DBOptionError('資料庫新增時發生錯誤。', payload={'error': e, 'instance': instance})
        finally:
            session.close()
        return instance

    def create(self, **kws) -> ORMObject:
        """新增"""
        model = self.__model__(**self._preprocess_params(kws))
        instance: ORMObject = self.save(model)
        return instance

    def update(self, model: ORMObject, **kws) -> ORMObject:
        """更新"""
        self._isinstance(model)
        session = db.session
        if not (updated := self._preprocess_params(kws)):
            updated = {k: v for k, v in vars(model).items() if k in model.columns}
        try:
            target = session.query(self.__model__).get(model.id)
            for k, v in updated.items():
                if k in model.columns:
                    setattr(target, k, v)
            session.flush()
            session.commit()
            instance: ORMObject = target.get_instance()
            return instance
        except Exception as e:
            session.rollback()
            raise DBOptionError('資料庫更新時發生錯誤。')
        finally:
            session.close()

    def delete(self, model_or_id: ORMObject, mark_deleted=False):
        """刪除"""
        if model_or_id is None:
            return
        model = model_or_id if self._isinstance(model_or_id, self.__model__) else self.get(model_or_id)
        session = db.session
        try:
            target = session.query(self.__model__).get(model.id)
            session.delete(target)
            session.flush()
            session.commit()
        except Exception as e:
            session.rollback()
            raise DBOptionError('資料庫刪除時發生錯誤。')
        finally:
            session.close()

    def first(self, **kws) -> Optional[ORMObject]:
        session = db.session
        model = session.query(self.__model__).filter_by(**kws).first()
        if not model:
            return None
        instance: ORMObject = model.get_instance()
        session.close()
        return instance

    def all(self) -> list[ORMObject]:
        """所有model"""
        session = db.session
        session.commit()
        result: list[ORMObject] = [model.get_instance() for model in session.query(self.__model__)]
        session.close()
        return result

    def get(self, id_) -> Optional[ORMObject]:
        """id精準查詢"""
        session = db.session
        model = session.query(self.__model__).get(id_)
        if not model:
            return None
        instance = model.get_instance()
        session.close()
        return instance

    def exists(self, **kws) -> bool:
        return db.session.query(self.__model__).filter_by(**kws).count() > 0

    def count(self, **kws) -> int:
        return db.session.query(self.__model__).filter_by(**kws).count()

    def get_or_create(self, defaults=None, **kws) -> tuple[ORMObject, bool]:
        """取得或創建"""
        instance = self.first(**kws)
        if not instance:
            return self.create(**dict(defaults or (), **kws)), True
        return instance, False


class AsyncService:
    """for爬蟲"""

    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """檢查model是否伺服器配置的相同"""
        rv = isinstance(model, (ORMObject, self.__model__))
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    @staticmethod
    def _preprocess_params(kws):
        return kws

    async def save(self, model) -> None:
        """儲存資料"""
        self._isinstance(model)
        session = await db.async_session()
        async with session.begin():
            try:
                session.add(model)
                await session.flush()
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise DBOptionError('異步插入資料時發生錯誤。', payload={'error': e})

    async def create(self, **kws) -> Optional[ORMObject]:
        """異步新增"""
        payload = self._preprocess_params(kws)
        model = self.__model__(**payload)
        await self.save(model)
        instance: ORMObject = await self.first(**payload)
        return instance

    async def get_or_create(self, default=None, **kws) -> tuple[ORMObject, bool]:
        """異步取得或創建"""
        instance = await self.first(**kws)
        if not instance:
            return await self.create(**dict(default or kws)), True
        return instance, False

    async def delete(self, model: ORMObject) -> None:
        """異步刪除"""
        self._isinstance(model)
        session = await db.async_session()
        async with session.begin():
            await session.execute(db.delete(self.__model__).filter(self.__model__.id == model.id))

    async def update(self, model: ORMObject, **kws) -> ORMObject:
        session = await db.async_session()
        async with session.begin():
            if not (updated := self._preprocess_params(kws)):
                updated = {k: v for k, v in vars(model).items() if k in model.columns}
            try:
                query = await session.execute(db.query(self.__model__).filter(self.__model__.id == model.id))
                target = query.scalar()
                for k, v in updated.items():
                    if k in model.columns:
                        setattr(target, k, v)
                instance: ORMObject = target.get_instance()
                return instance
            except Exception as e:
                session.rollback()
                raise DBOptionError('資料庫更新時發生錯誤。', payload={'error': e})

    async def get(self, id_: int) -> Optional[ORMObject]:
        """get"""
        session = await db.async_session()
        async with session.begin():
            model = await session.get(self.__model__, id_)
            if not model:
                return None
            return model.get_instance()

    async def first(self, **kws) -> Optional[ORMObject]:
        """first"""
        session = await db.async_session()
        async with session.begin():
            query = await session.execute(db.query(self.__model__).filter_by(**kws))
            model = query.scalar()
            if not model:
                return None
            instance = model.get_instance()
        return instance

    async def all(self) -> list[ORMObject]:
        """all"""
        session = await db.async_session()
        async with session.begin():
            query = await session.execute(db.query(self.__model__))
            models = query.scalars()
            return [model.get_instance() for model in models]

    async def exists(self, **kws) -> bool:
        return await self.count(**kws) > 0

    async def count(self, **kws) -> int:
        session = await db.async_session()
        async with session.begin():
            query = await session.execute(db.func.count(db.query(self.__model__.id).filter_by(**kws)))
            return query.scalar()
