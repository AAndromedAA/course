from controller import Controller


class Router:
    main_menu_option_handler = int()
    controller_methods = {1: Controller.get_team_absolute_statistic, 2: Controller.get_several_teams_absolute_statistics,
                          3: Controller.get_team_detailed_statistic, 4: Controller.get_team_statistic_by_season,
                          5: Controller.make_refresh, 6: Controller.create_backup, 7: Controller.download_backup}

    def __init__(self, main_menu_option):
        self.main_menu_option_handler = main_menu_option

    def route(self):
        if self.main_menu_option_handler in range(1, 8):
            self.controller_methods[self.main_menu_option_handler]()
        else:
            raise Exception('Unknown option')
