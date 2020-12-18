from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Match(Base):
    __tablename__ = "Match"

    id = Column(Integer, primary_key=True)
    home_team = Column(Integer, ForeignKey('Team.id'))
    away_team = Column(Integer, ForeignKey('Team.id'))
    home_team_obj = relationship('Team', foreign_keys=[home_team])
    away_team_obj = relationship('Team', foreign_keys=[away_team])
    home_team_goals = Column(Integer)
    away_team_goals = Column(Integer)
    competition_id = Column(Integer, ForeignKey('Competition.id'))
    competition = relationship('Competition', backref="Match")

    def __init__(self, id, home_team, away_team, home_team_goals, away_team_goals, competition_id,
                 home_team_obj, away_team_obj, competition):
        self.id = id
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_goals = home_team_goals
        self.away_team_goals = away_team_goals
        self.competition_id = competition_id
        self.home_team_obj = home_team_obj
        self.away_team_obj = away_team_obj
        self.competition = competition
