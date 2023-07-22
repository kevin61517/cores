from ..database import db, Mixin, ORM


class TestORM(ORM):
    __json_hidden__ = ['created_at']
    __json_public__ = []
    __json_modifiers__ = {
        'test_column': lambda self, value: value,
    }


class Test(Mixin, TestORM, db.Model):
    """測試資料庫"""
    __tablename__ = 'test_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    is_active = db.Column(db.Boolean, default=False)
    is_online = db.Column(db.Boolean, default=False)

    @property
    def test_column(self):
        return self.name + '測試後綴'
