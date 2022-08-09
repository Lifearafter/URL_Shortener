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

from sqlalchemy import Column, String


class URL_Mapping(Base):
    __tablename__ = "urls"

    short_url = Column(String(1024), primary_key=True,
                       unique=True, nullable=False)
    long_url = Column(String(768), nullable=False, unique=True)
    time = Column(String(256), nullable=False)

    def __init__(self, short_url, long_url, time):
        self.short_url = short_url
        self.long_url = long_url
        self.time = time
