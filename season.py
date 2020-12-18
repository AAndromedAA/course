from base import Base
from sqlalchemy import Column, Integer


class Season(Base):
    __tablename__ = "Season"

    year = Column(Integer, primary_key=True)

    def __init__(self, year):
        self.year = year
