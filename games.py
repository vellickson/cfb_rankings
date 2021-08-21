"""
    1. Pass in season and week #
    2. Make call to API to get relevant data
    3. Write game info to database in games table
    4. Update win/loss record for each team

"""
import requests
from team import Team


def get_weekly_game_results(season, week):
    """for given week, make an API call to get the info"""
    url = f'https://api.collegefootballdata.com/games?year={season}&week={week}'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)


def extract_team_data(game_results):
    """extract information specific to each team"""
    winning_team = Team('')
    losing_team = Team('')
    winning_team.update_win_loss()
    losing_team.update_win_loss()


def store_game_results(game_results):
    """store info in games database table"""





