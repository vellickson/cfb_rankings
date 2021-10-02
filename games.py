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
from record import Record


def get_weekly_game_results(season, week):
    """for given week, make an API call to get the info"""
    url = f'https://api.collegefootballdata.com/games?year={season}&week={week}'
    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer XNvoXV6PuAgCRpcNSuo9+nYU6xmWa/16GxJ+D8NLwKVS3zyjETQPatR7b6Hq92t4'}

    # TODO: Add exception handling to api request and use status_code
    # PRODUCTION
    # r = requests.get(url, headers=headers)
    # print(r.status_code)

    # TESTING ONLY
    #with open('2019week1.json', 'w') as f:
    #    json.dump(r.json(), f)

    #f.close()

    with open('2019week1.json', 'r') as f:
        results_as_list = json.load(f)

    # PRODUCTION
    # results_as_list = r.json()

    for result in results_as_list:

        home_team = result.get('home_team')
        away_team = result.get('away_team')
        home_points = result.get('home_points')
        away_points = result.get('away_points')
        neutral_location = result.get('neutral_site')

        # TODO: What to do with FCS teams?
        if home_points > away_points:
            winning_team_record = Record(home_team)
            losing_team_record = Record(away_team)
            winning_team_record.point_diff = home_points - away_points
            losing_team_record.point_diff = away_points - home_points

            if not neutral_location:
                winning_team_record.game_location = "home"
                losing_team_record.game_location = "away"

        else:
            winning_team_record = Record(away_team)
            losing_team_record = Record(home_team)
            winning_team_record.point_diff = away_points - home_points
            losing_team_record.point_diff = home_points - away_points

            if not neutral_location:
                winning_team_record.game_location = "away"
                losing_team_record.game_location = "home"

        if neutral_location:
            winning_team_record.game_location = "neutral"
            losing_team_record.game_location = "neutral"

        winning_team_record.opponents.append(losing_team_record.team_name)
        losing_team_record.opponents.append(winning_team_record.team_name)

        winning_team_record.update_win_loss(we_won=True)
        losing_team_record.update_win_loss(we_won=False)

        try:
            winning_team = Team(winning_team_record.team_name, record=winning_team_record)
            winning_team.update_record(season)
        except:
            print(f'could not write records for {winning_team_record.team_name} ... FCS?')

        try:
            losing_team = Team(losing_team_record.team_name, record=losing_team_record)
            losing_team.update_record(season)
        except:
            print(f'could not write records for {losing_team_record.team_name} ... FCS?')


def extract_team_data(game_results):
    """extract information specific to each team"""
    winning_team = Team('')
    losing_team = Team('')

def store_game_results(game_results):
    """store info in games database table"""





