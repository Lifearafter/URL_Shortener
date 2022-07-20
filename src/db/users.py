from enum import unique
from xmlrpc.client import Boolean
from base import Base
from sqlalchemy import Column, String, Boolean, Integer


class Users(Base):
    __tablename__ = "users"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True
    )
    user_type = Column(Boolean, nullable=False)
    auth_key = Column(String(256), unique=True)

    def __init__(self, user_type, auth_key):
        self.user_type = user_type
        self.auth_key = auth_key
