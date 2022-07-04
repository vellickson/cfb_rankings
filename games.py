"""
    1. Pass in season and week #
    2. Make call to API to get relevant data
    3. Write game info to database in games table
    4. Update win/loss record for each team

"""
import requests
import psycopg2
import json
from team import Team
from game_record import GameRecord


def get_weekly_game_results(season, week):
    """for given week, make an API call to get the info"""

    # PRODUCTION
    url = f'https://api.collegefootballdata.com/games?year={season}&week={week}'
    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer XNvoXV6PuAgCRpcNSuo9+nYU6xmWa/16GxJ+D8NLwKVS3zyjETQPatR7b6Hq92t4'}
    # TODO: Add exception handling to api request and use status_code
    # r = requests.get(url, headers=headers)
    # print(r.status_code)

    # TESTING
    #with open('2019week1.json', 'w') as f:
    #    json.dump(r.json(), f)

    # TESTING
    with open('2019week2game1.json', 'r') as f:
        results_as_list = json.load(f)

    f.close()

    # PRODUCTION
    # results_as_list = r.json()

    for result in results_as_list:

        home_team = result.get('home_team')
        away_team = result.get('away_team')
        home_points = result.get('home_points')
        away_points = result.get('away_points')
        neutral_location = result.get('neutral_site')
        winning_team = None
        losing_team = None

        # TODO: What to do with FCS teams?
        if home_points > away_points:
            winning_team_game_record = GameRecord(home_team)
            losing_team_game_record = GameRecord(away_team)
            winning_team_game_record.point_diff = home_points - away_points
            losing_team_game_record.point_diff = away_points - home_points

            if not neutral_location:
                winning_team_game_record.game_location = "home"
                losing_team_game_record.game_location = "away"

        else:
            winning_team_game_record = GameRecord(away_team)
            losing_team_game_record = GameRecord(home_team)
            winning_team_game_record.point_diff = away_points - home_points
            losing_team_game_record.point_diff = home_points - away_points

            if not neutral_location:
                winning_team_game_record.game_location = "away"
                losing_team_game_record.game_location = "home"

        if neutral_location:
            winning_team_game_record.game_location = "neutral"
            losing_team_game_record.game_location = "neutral"

        winning_team_game_record.set_win_loss_outcome(we_won=True)
        losing_team_game_record.set_win_loss_outcome(we_won=False)

        winning_team = get_team(winning_team_game_record)
        losing_team = get_team(losing_team_game_record)

        winning_team.update_record(season, winning_team_game_record)
        losing_team.update_record(season, losing_team_game_record)


def get_team(game_record):
    team = None

    try:
        team = Team(game_record.team_name)
    except Exception as get_team_error:
        print(f'could not create Team object ... FCS? or {get_team_error}')

    return team


def call_update(team, game_record, season):
    # FCS teams should be None
    if team is not None:
        try:
            team.update_record(season, game_record)
        except Exception as update_error:
            print(f'could not write records... FCS? or {update_error}')


def extract_team_data(game_results):
    """extract information specific to each team"""
    winning_team = Team('')
    losing_team = Team('')


def store_game_results(game_results):
    """store info in games database table"""





