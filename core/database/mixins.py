"""
model mixin
"""
from ..database.base import TableTypes as Types
from utils import taipei_now


class Mixin:
    """混合類"""
    __mixin_columns__ = ['id', 'created_at', 'updated_at']

    id = Types.Column(Types.Integer, primary_key=True, autoincrement=True)
    created_at = Types.Column(Types.DateTime(timezone=True), server_default=taipei_now())
    updated_at = Types.Column(Types.DateTime(timezone=True), server_default=taipei_now(), onupdate=taipei_now())
