from base import Base
from sqlalchemy import Column, String


class URL(Base):
    __tablename__ = "urls"

    short_url = Column(String(256), primary_key=True, unique=True, nullable=False)
    long_url = Column(String(256), nullable=False, unique=True)
    time = Column(String(256), nullable=False)

    def __init__(self, short_url, long_url, time):
        self.short_url = short_url
        self.long_url = long_url
        self.time = time
