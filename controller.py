from model import Model
from cui import Cui
import pandas as pd
from view import View
import os, time, datetime
from data_getter import DataGetter


def detailed_analyze_by_season(matches, teams):
    matches_df = pd.DataFrame({'home_team': [int(vars(match)['home_team']) for match in matches],
                               'away_team': [int(vars(match)['away_team']) for match in matches],
                               'home_team_goals': [int(vars(match)['home_team_goals']) for match in matches],
                               'away_team_goals': [int(vars(match)['away_team_goals']) for match in matches]})
    matches = list()
    print(matches_df)
    for i in range(0, len(matches_df)):
        print(matches_df.iloc[i])
        matches.append(pd.Series({'home_team_goals': matches_df.iloc[i]['home_team_goals'],
                                  'away_team_goals': matches_df.iloc[i]['away_team_goals']}))
        matches[len(matches)-1].name = \
            [vars(x) for x in teams if int(vars(x)['id']) == int(matches_df.iloc[i]['home_team'])][0]['name'] + ' - ' + \
            [vars(x) for x in teams if int(vars(x)['id']) == int(matches_df.iloc[i]['away_team'])][0]['name']
    return matches


def analyze_detailed_statistic(matches, team_id):
    matches_df = pd.DataFrame({'home_team': [int(match['home_team']) for match in matches],
                               'away_team': [int(match['away_team']) for match in matches],
                               'home_team_goals': [int(match['home_team_goals']) for match in matches],
                               'away_team_goals': [int(match['away_team_goals']) for match in matches],
                               'year': [int(match['year']) for match in matches]})
    home_matches = pd.DataFrame(matches_df[matches_df.home_team == team_id]
                                [['home_team_goals', 'away_team_goals', 'year']])
    first_team_goals_home = home_matches[['home_team_goals', 'year']].groupby(['year'])['home_team_goals'].sum()
    second_team_goals_away = home_matches[['away_team_goals', 'year']].groupby(['year'])['away_team_goals'].sum()

    away_matches = pd.DataFrame(matches_df[matches_df.home_team != team_id]
                                [['home_team_goals', 'away_team_goals', 'year']])
    second_team_goals_home = away_matches[['home_team_goals', 'year']].groupby(['year'])['home_team_goals'].sum()
    first_team_goals_away = away_matches[['away_team_goals', 'year']].groupby(['year'])['away_team_goals'].sum()
    team_goals = first_team_goals_home + first_team_goals_away
    others_goals = second_team_goals_home + second_team_goals_away
    return team_goals, others_goals


def analyze_absolute_statistic(matches, team_id):
    matches_df = pd.DataFrame({'home_team': [int(match['home_team']) for match in matches],
                               'away_team': [int(match['away_team']) for match in matches],
                               'home_team_goals': [int(match['home_team_goals']) for match in matches],
                               'away_team_goals': [int(match['away_team_goals']) for match in matches],
                               'year': [int(match['year']) for match in matches]})
    print(matches_df)
    home_matches = pd.DataFrame(matches_df[matches_df.home_team == team_id]
                                [['home_team_goals', 'away_team_goals', 'year']])
    home_matches = pd.DataFrame({'year': home_matches['year'], 'total':
                                 home_matches['home_team_goals'] - home_matches['away_team_goals']}) \
                                 .groupby(['year'])['total'].sum()
    away_matches = pd.DataFrame(matches_df[matches_df.away_team == team_id]
                                [['home_team_goals', 'away_team_goals', 'year']])
    away_matches = pd.DataFrame({'year': away_matches['year'], 'total':
                                away_matches['away_team_goals'] - away_matches['home_team_goals']}) \
                                .groupby(['year'])['total'].sum()
    total_statistic = home_matches + away_matches
    for year in range(2008, 2021):
        if year not in list(total_statistic.index):
            total_statistic = total_statistic.append(pd.Series(0, index=[year]))
    return total_statistic.sort_index()


class Controller:
    @staticmethod
    def get_team_absolute_statistic():
        Cui.show_competitions()
        competition_name = input('Enter competition name: ')
        teams = Model().read_teams_by_competition(competition_name=competition_name)
        Cui.show_teams(teams)
        team_id = int(input('Enter team id: '))
        start_time = time.time()
        matches = Model().read_matches_by_team_id(team_id)
        print(time.time() - start_time, 'seconds')
        matches = Model().set_competitions_years(matches)
        total_score = analyze_absolute_statistic(matches, team_id)
        total_score.name = [vars(x) for x in teams if int(vars(x)['id']) == team_id][0]['name']
        total_score_df = pd.DataFrame(total_score)

        new_sample_df = total_score_df.loc[2008:2020, ['{}'.format(total_score.name)]]
        View.view_lines_plot(new_sample_df)

    @staticmethod
    def get_several_teams_absolute_statistics():
        Cui.show_competitions()
        competition_name = input('Enter competition name: ')
        teams = list(Model().read_teams_by_competition(competition_name=competition_name))
        Cui.show_teams(teams)
        teams_ids = list()
        while True:
            team_id = input('Enter team id: ')
            if not team_id.isdigit():
                break
            teams_ids.append(int(team_id))

        teams_matches = list()
        for team_id in teams_ids:
            teams_matches.append(Model().set_competitions_years(Model().read_matches_by_team_id(team_id)))
        teams_total_statistics = list()
        i = 0
        for team_match in teams_matches:
            teams_total_statistics.append(analyze_absolute_statistic(team_match, teams_ids[i]))
            teams_total_statistics[len(teams_total_statistics)-1].name = \
                [vars(x) for x in teams if int(vars(x)['id']) == teams_ids[i]][0]['name']
            i += 1

        new_sample_df = pd.DataFrame(index=teams_total_statistics[0].index)
        for team_total_score in teams_total_statistics:
            new_sample_df['{}'.format(team_total_score.name)] = team_total_score.values
        View.view_lines_plot(new_sample_df)

    @staticmethod
    def get_team_detailed_statistic():
        Cui.show_competitions()
        competition_name = input('Enter competition name: ')
        teams = list(Model().read_teams_by_competition(competition_name=competition_name))
        Cui.show_teams(teams)
        team_id = int(input('Enter team id: '))

        matches = Model().read_matches_by_team_id(team_id)
        matches = Model().set_competitions_years(matches)
        detailed_statistic = analyze_detailed_statistic(matches, team_id)
        detailed_statistic[0].name = [vars(x) for x in teams if int(vars(x)['id']) == team_id][0]['name']
        detailed_statistic[1].name = 'Others'

        new_sample_df = pd.DataFrame(index=detailed_statistic[0].index)
        for team_total_score in detailed_statistic:
            new_sample_df['{}'.format(team_total_score.name)] = team_total_score.values
        View.view_column_plot(new_sample_df)

    @staticmethod
    def get_team_statistic_by_season():
        season = int(input('Enter season year: '))
        Cui.show_competitions(season)
        competition_id = int(input('Enter competition id: '))
        teams = list(Model().read_teams_by_competition(competition_id=competition_id))
        Cui.show_teams(teams)
        team_id = int(input('Enter team id: '))

        matches = Model().read_matches_by_team_id(team_id, competition_id=competition_id)
        statistic_by_season = detailed_analyze_by_season(matches, teams)

        new_sample_df = pd.DataFrame(index=statistic_by_season[0].index)
        for score in statistic_by_season:
            new_sample_df['{}'.format(score.name)] = score.values
        View.view_column_plot(new_sample_df.transpose())

    @staticmethod
    def make_refresh():
        DataGetter().get_seasons()
        print("Seasons had loaded")
        DataGetter().get_countries()
        print("Countries had loaded")
        DataGetter().get_leagues()
        print("Competitions had loaded")
        DataGetter().get_teams()
        print("Teams had loaded")
        DataGetter().get_matches()
        print("Matches had loaded\nAll data had successfully loaded!")

    @staticmethod
    def create_backup():
        dump_name = input('Enter dump file name: ')
        start_time = time.time()
        os.system('C:\\\"Program Files\"\PostgreSQL\\11\\bin\pg_dump.exe -h 192.168.0.110 -U postgres football > %HOMEPATH%\Desktop\course\\backups\{}.dump'.format(dump_name))
        print(time.time() - start_time, 'seconds')

    @staticmethod
    def download_backup():
        files = os.listdir('backups')
        if len(files) == 0:
            raise Exception("No backups")
        dumps = [{'name': x, 'time': time.ctime(os.path.getctime('backups\\{}'.format(x)))} for x in files if x.endswith('.dump')]
        Cui.show_dumps_list(dumps)
        dump_name = input('Enter dump file name (without type): ')
        start_time = time.time()
        os.system('C:\\\"Program Files\"\PostgreSQL\\11\\bin\psql.exe -h 192.168.0.104 -U postgres -c "DROP DATABASE IF EXISTS \"Football\""')
        os.system('C:\\\"Program Files\"\PostgreSQL\\11\\bin\psql.exe -h 192.168.0.104 -U postgres -c "CREATE DATABASE \"Football\""')
        os.system('C:\\\"Program Files\"\PostgreSQL\\11\\bin\psql.exe -h 192.168.0.104 -U postgres football < %HOMEPATH%\Desktop\course\\backups\\{}.dump'
                  .format(dump_name))
        print(time.time() - start_time, 'seconds')
