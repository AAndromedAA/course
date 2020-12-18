import http.client
import json
import time

import psycopg2


class DataGetter:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': "22b211d986mshe5b91185f35ba73p1483fbjsnc86db3fd0ab8",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

        self.master_session = psycopg2.connect("dbname='football' host='192.168.0.104' user='postgres' password='3497279088'")
        self.slave_session = psycopg2.connect("dbname='football' host='192.168.0.110' user='postgres' password='3497279088'")
        self.master_curs = self.master_session.cursor()
        self.slave_curs = self.slave_session.cursor()

    def get_seasons(self):
        self.conn.request("GET", "/seasons", headers=self.headers)
        res = self.conn.getresponse()
        seasons = json.loads(res.read().decode('utf-8'))['api']['seasons']
        for i in range(1, len(seasons)+1):
            try:
                self.master_curs.execute('INSERT INTO "Season" (year) VALUES({})'.format(int(seasons[str(i)])))
                self.master_session.commit()
            except:
                self.master_session.rollback()

    def get_leagues(self):
        self.slave_curs.execute("SELECT * FROM \"Season\"")
        seasons = self.slave_curs.fetchall()
        for season in seasons:
            print(season[0])
            self.conn.request("GET", "/v2/leagues/country/world/{}".format(season[0]), headers=self.headers)
            res = self.conn.getresponse()
            leagues = json.loads(res.read().decode('utf-8'))['api']['leagues']
            for league in leagues:
                try:
                    #if str(league['name']).__contains__('UEFA') or str(league['name']).__contains__('Euro') or \
                    #   str(league['name']).__contains__('World'):
                    self.master_curs.execute('INSERT INTO "Competition" (id, name, country, season) '
                                             'VALUES({}, \'{}\', (SELECT id FROM "Country" WHERE name LIKE \'%{}%\'), {})'
                                             .format(int(league['league_id']), league['name'], league['country'].replace(' ',  "-"),
                                                         int(league['season'])))
                    self.master_session.commit()
                except Exception as ex:
                    print(ex)
                    self.master_session.rollback()
            time.sleep(2)

    def get_teams(self):
        self.slave_curs.execute('SELECT * FROM "Competition"')
        competitions = self.slave_curs.fetchall()
        for competition in competitions:
            self.conn.request("GET", "/v2/teams/league/{}".format(competition[0]), headers=self.headers)
            res = self.conn.getresponse()
            teams = json.loads(res.read().decode('utf-8'))['api']['teams']
            for team in teams:
                try:
                    self.master_curs.execute('INSERT INTO "Team" (id, name, country_id) '
                                             'VALUES({}, \'{}\', (SELECT id FROM "Country" WHERE name LIKE \'%{}%\'))'
                                             .format(int(team['team_id']), team['name'], team['country'].replace(' ', "-")))
                    self.master_session.commit()
                except Exception as ex:
                    print(ex)
                    self.master_session.rollback()
            time.sleep(3)

    def get_matches(self):
        self.slave_curs.execute('SELECT * FROM "Competition"')
        competitions = self.slave_curs.fetchall()
        for competition in competitions:
            self.conn.request("GET", "/v2/fixtures/league/{}?timezone=Europe%2FLondon".format(competition[0]),
                              headers=self.headers)
            res = self.conn.getresponse()
            matches = json.loads(res.read().decode('utf-8'))['api']['fixtures']
            self.slave_curs.execute('SELECT id FROM "Team"')
            teams = [x[0] for x in self.slave_curs.fetchall()]
            for match in matches:
                try:
                    if int(match['homeTeam']['team_id']) in teams and int(match['awayTeam']['team_id']) in teams:
                        self.master_curs.execute('INSERT INTO "Match" (id, home_team, away_team, home_team_goals,'
                                                 'away_team_goals, competition_id) VALUES({}, {}, {}, {}, {}, {})'
                                                 .format(int(match['fixture_id']), int(match['homeTeam']['team_id']),
                                                         int(match['awayTeam']['team_id']), int(match['goalsHomeTeam']),
                                                         int(match['goalsAwayTeam']), competition[0]))
                        self.master_session.commit()
                except Exception as ex:
                    print(ex)
                    self.master_session.rollback()
            time.sleep(2)

    def get_countries(self):
        self.conn.request("GET", "/countries",
                          headers=self.headers)
        res = self.conn.getresponse()
        countries = json.loads(res.read().decode('utf-8'))['api']['countries']
        for country in countries.values():
            try:
                self.master_curs.execute('INSERT INTO "Country" (name) VALUES(\'{}\')'.format(country))
                self.master_session.commit()
            except:
                self.master_session.rollback()
