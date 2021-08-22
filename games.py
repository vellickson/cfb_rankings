"""
    1. Pass in season and week #
    2. Make call to API to get relevant data
    3. Write game info to database in games table
    4. Update win/loss record for each team

"""
import requests
from team import Team


class GameResults:

    def __init__(self, season, week):
        self.season = season
        self.week = week

    def get_weekly_game_results(self):
        """for given week, make an API call to get the info"""
        url = f'https://api.collegefootballdata.com/games?year={self.season}&week={self.week}'
        headers = {'Accept': 'application/json',
                   'Authorization': 'Bearer XNvoXV6PuAgCRpcNSuo9+nYU6xmWa/16GxJ+D8NLwKVS3zyjETQPatR7b6Hq92t4'}

        # TODO: Add exception handling to api request
        r = requests.get(url, headers=headers)
        # print(r.status_code)

        results_as_list = r.json()
        for result in results_as_list:
            winning_team = Team()
            losing_team = Team()

            home_team = result.get('home_team')
            away_team = result.get('away_team')
            home_points = result.get('home_points')
            away_points = result.get('away_points')
            neutral_location = result.get('neutral_site')

            # TODO: Make a decision about how to handle record information
            if home_points > away_points:
                winning_team.name = home_team
                losing_team.name = away_team
                winning_team.record.update_point_differential(home_points - away_points)
                winning_team.game_point_differential = home_points - away_points
                losing_team.game_point_differential = away_points - home_points
                if not neutral_location:
                    winning_team.game_location = "home"
                    losing_team.game_location = "away"

            else:
                winning_team.name = away_team
                losing_team.name = home_team
                winning_team.game_point_differential = away_points - home_points
                losing_team.game_point_differential = home_points - away_points
                if not neutral_location:
                    winning_team.game_location = "away"
                    losing_team.game_location = "home"

            if neutral_location:
                winning_team.game_location = "neutral"
                losing_team.game_location = "neutral"

            winning_team.opponents.append(losing_team)
            losing_team.opponents.append(winning_team)

            winning_team.update_record(we_won=True, season=self.season, week=self.week)
            losing_team.update_record(we_won=False, season=self.season, week=self.week)
            print('blah')

    def extract_team_data(self, game_results):
        """extract information specific to each team"""
        winning_team = Team('')
        losing_team = Team('')
        winning_team.update_win_loss()
        losing_team.update_win_loss()

    def store_game_results(self, game_results):
        """store info in games database table"""





