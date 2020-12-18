from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = "Team"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey('Country.id'))
    country = relationship('Country', backref="Team")

    def __init__(self, id, name, country_id, country):
        self.id = id
        self.name = name
        self.country_id = country_id
        self.country = country
