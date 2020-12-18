from base import Base
from sqlalchemy import Column, Integer, String


class Country(Base):
    __tablename__ = 'Country'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
