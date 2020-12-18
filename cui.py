from model import Model


class Cui:
    @staticmethod
    def get_created_main_menu_option():
        print('\tMain menu\n1.Get team statistic\n2.Get all competition teams statistic')
        print('3.Get team`s detailed statistic\n4.Get team`s detailed statistic by season')
        print('5.Refresh data\n6.Create backup\n7.Download backup\n8.Exit')
        return input()

    @staticmethod
    def show_competitions(season=0):
        print('\tCompetitions list')
        for competition in Model().read_competitions(season=season):
            if season == 0:
                print(vars(competition)['name'])
            else:
                print(vars(competition)['id'], vars(competition)['name'])

    @staticmethod
    def show_teams(teams):
        print('\tTeams list')
        for team in teams:
            print(vars(team)['id'], vars(team)['name'])

    @staticmethod
    def show_dumps_list(dumps):
        print('\tBackups list:')
        for dump in dumps:
            print(dump['time'], ' --- ', dump['name'])
