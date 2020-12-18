from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Competition(Base):
    __tablename__ = "Competition"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(Integer, ForeignKey('Country.id'))
    country_obj = relationship('Country', backref="Competition")
    season = Column(Integer, ForeignKey('Season.year'))
    season_obj = relationship('Season', backref="Competition")

    def __init__(self, id, name, country, country_obj, season, season_obj):
        self.id = id
        self.name = name
        self.country = country
        self.country_obj = country_obj
        self.season = season
        self.season_obj = season_obj
