from ast import Num
import sys
import os

if __package__:
    parentdir = os.path.dirname(__file__)
    rootdir = os.path.dirname(parentdir)
    if rootdir not in sys.path:
        sys.path.append(rootdir)
    if parentdir not in sys.path:
        sys.path.append(parentdir)
    from .base import Base

from sqlalchemy import Column, String, Boolean, Integer


class DelStack(Base):
    __tablename__ = "delStack"
    short_url = Column(String(256), unique=True, nullable=False)
    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )

    def __init__(self, shortUrl):
        self.short_url = shortUrl
