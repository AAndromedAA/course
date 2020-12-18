from country import Country
from season import Season
from competition import Competition
from team import Team
from match import Match
from base import Base, slave_session, slave_engine
from sqlalchemy import or_, and_, asc


class Model:
    def __init__(self):
        Base.metadata.create_all(slave_engine)
        self.slave_session = slave_session()

    def read_competitions(self, season):
        if season == 0:
            return self.slave_session.query(Competition).distinct(Competition.name).order_by(asc(Competition.name)).all()
        else:
            return self.slave_session.query(Competition).filter(Competition.season == season).order_by(asc(Competition.name)).all()

    def read_matches_by_team_id(self, team_id, competition_id=0):
        if competition_id != 0:
            return self.slave_session.query(Match).filter(and_(or_(Match.home_team == team_id, Match.away_team == team_id),
                                                           Match.competition_id == competition_id)).all()
        else:
            return self.slave_session.query(Match).filter(or_(Match.home_team == team_id, Match.away_team == team_id)).all()

    def get_competitions_ids_by_name(self, competition_name):
        return self.slave_session.query(Competition).filter(Competition.name == competition_name).all()

    def read_teams_by_competition(self, competition_name='', competition_id=0):
        competitions_ids = list()
        if competition_id == 0:
            for competition in self.get_competitions_ids_by_name(competition_name):
                competitions_ids.append(int(vars(competition)['id']))
        if competition_id == 0:
            team_ids = list()
            for match in self.slave_session.query(Match).filter(Match.competition_id.in_(competitions_ids)).all():
                team_ids.append(vars(match)['home_team'])
                team_ids.append(vars(match)['away_team'])
        else:
            team_ids = list(self.slave_session.query(Match.home_team).filter(Match.competition_id == competition_id))
            for team in list(self.slave_session.query(Match.away_team).filter(Match.competition_id == competition_id)):
                team_ids.append(team)
        return self.slave_session.query(Team).filter(Team.id.in_(team_ids)).order_by(asc(Team.name)).all()

    def set_competitions_years(self, matches):
        matches_ = list()
        for match in matches:
            test = vars(self.slave_session.query(Competition).filter(Competition.id == int(vars(match)['competition_id'])).one())
            matches_.append({'id': int(vars(match)["id"]), 'home_team': int(vars(match)["home_team"]), 'away_team': int(vars(match)["away_team"]),
                             'home_team_goals': int(vars(match)["home_team_goals"]),
                             'away_team_goals': int(vars(match)["away_team_goals"]),
                             'year': int(test['season'])})
        return matches_
