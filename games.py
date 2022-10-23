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
    url = f'https://api.collegefootballdata.com/games?year={season}&week={week}&division=fbs'
    headers = {'Accept': 'application/json',
               'Authorization': 'Bearer XNvoXV6PuAgCRpcNSuo9+nYU6xmWa/16GxJ+D8NLwKVS3zyjETQPatR7b6Hq92t4'}
    # TODO: Add exception handling to api request and use status_code
    # r = requests.get(url, headers=headers)
    # print(f'request status code: {r.status_code}')

    # TESTING - writing to weekly file
    #with open('2019week1.json', 'w') as f:
    #    json.dump(r.json(), f)

    # TESTING - reading from weekly file
    with open('game_data/2022week8.json', 'r') as f:
        results_as_list = json.load(f)

    f.close()

    # PRODUCTION
    # results_as_list = r.json()

    for result in results_as_list:
        # print(f'result {result}')
        # home_division = result.get('home_division')
        # if home_division == "fcs":
        #     continue

        home_team = result.get('home_team')
        away_team = result.get('away_team')
        home_points = result.get('home_points')
        away_points = result.get('away_points')
        neutral_location = result.get('neutral_site')

        if home_points is None or away_points is None:
            print(f'ERROR: Missing point info for {result}')
            continue

        # TODO: Handle FCS teams in a graceful manner
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

        # Get a team object to act upon if we can
        winning_team = get_team(winning_team_game_record, season)
        losing_team = get_team(losing_team_game_record, season)

        # If we don't have a team object, assume FCS
        if not winning_team:
            losing_team_game_record.opponent = -1
        else:
            losing_team_game_record.opponent = winning_team.team_id

        if not losing_team:
            winning_team_game_record.opponent = -1
        else:
            winning_team_game_record.opponent = losing_team.team_id

        if winning_team:
            # print(f'winning_team.team_record {winning_team.team_record}')
            if winning_team.team_record is None:
                # print(f'creating record for {winning_team.name}')
                winning_team.create_season_record(season)

            winning_team.update_record(season, winning_team_game_record)

        if losing_team:
            if losing_team.team_record is None:
                losing_team.create_season_record(season)

            losing_team.update_record(season, losing_team_game_record)
        # break


def get_team(game_record, season):
    try:
        team = Team(season, name=game_record.team_name)
        return team
    except Exception as get_team_error:
        print(f'could not get Team object ... is {game_record.team_name} in FCS?')
        return None


# def call_update(team, game_record, season):
#     # FCS teams should be None
#     if team is not None:
#         try:
#             team.update_record(season, game_record)
#         except Exception as update_error:
#             print(f'could not write records... FCS? or {update_error}')


def store_game_results(game_results):
    """store info in games database table"""





