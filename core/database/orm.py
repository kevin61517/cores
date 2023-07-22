"""
ORM
"""
from typing import Optional
from exceptions import DBOrmError, DBOptionError


class ORMObject:
    """伺服器內部ORM物件"""

    def __init__(self, cls, db_columns, public=None, hidden=None, modifiers=None):
        self._public: list = public if public else []  # 公開欄位
        self._hidden: list = hidden if hidden else []  # 隱藏欄位
        self._modifiers: dict = modifiers if modifiers else {}  # 擴充欄位
        self._cls: type = cls  # 資料表類
        self._db_columns: list = db_columns  # 資料表欄位
        self.id: Optional[int] = None
        self.created_at: Optional[str] = None
        self.updated_at: Optional[str] = None

    def __repr__(self):
        return f'<{self._cls}{self.id}>'

    def to_json(self):
        """object -> dict"""
        rv = {}
        for key, value in vars(self).items():
            if self._public and key in self._public:
                rv[key] = value
            elif not key.startswith('_') and key not in self._hidden:
                rv[key] = value
        return rv

    @property
    def columns(self):
        for column in self._db_columns:
            yield column


class ORM:
    """ORMObject Manager -> 給Sqlalchemy Table繼承"""
    __default_orm__: ORMObject = ORMObject
    __json_public__: list = []  # 公開欄位
    __json_hidden__: list = []  # 隱藏欄位
    __json_modifiers__: dict = {}  # 擴充欄位

    def get_field_names(self):
        """self.__mapper__ -> sqlalchemy物件屬性"""
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def get_instance(self) -> ORMObject:
        """
        Sqlalchemy物件轉伺服器物件
        由於sqlalchemy model物件被查詢出來後需要有session上下文綁定才能呼叫屬性，一旦脫離session時便無法再以物件屬性形式呼叫
        因此在Server內的傳遞都以ORMObject型態操作，結束後再重新入庫。
        self = Sqlalchemy object
        instance = Server object
        """
        db_columns = list(self.get_field_names())
        instance = self.__default_orm__(
            cls=self.__class__.__name__,
            db_columns=db_columns,
            hidden=self.__json_hidden__,
            public=self.__json_public__,
            modifiers=self.__json_modifiers__
        )
        for field in db_columns:
            setattr(instance, field, getattr(self, field))
        for attr_name, method in self.__json_modifiers__.items():
            value = getattr(self, attr_name)
            setattr(instance, attr_name, method(self, value))
        return self._valid_instance(instance)

    def _valid_instance(self, instance):
        """校驗ORM物件"""
        for column in self.__mixin_columns__:
            if getattr(instance, column) is None:
                raise DBOrmError('伺服器ORM物件實例化錯誤', payload={'instance': instance})
        return instance
