"""
Determine rankings for each time
1. Foreach known team, get its aggregate win loss record and record of its opponents
2. Calculate rankings
3. Output list
"""

import psycopg2
from team_record import TeamRecord


class Rankings:
    def __init__(self, season):
        self.season = season
        self.conn = psycopg2.connect(
            "dbname='cfb_rankings' user='postgres' password='postgres' host='localhost' port=5433"
        )

    def rank_teams(self):
        # Iterate through each record and aggregate wins/losses
        sql_get_record = f"SELECT * FROM records where season = season"
        get_record_cursor = self.conn.cursor()
        get_record_cursor.execute(sql_get_record)
        print(f'cursor_description {get_record_cursor.description}')
        columns = get_record_cursor.description
        team_records = []

        print(f'col 0 {columns[0].name}')
        for record in get_record_cursor:
            team_id = record[0]
            team_name = self.get_team_name(team_id)
            team_record = TeamRecord(team_name)

            team_record.home_wins = record[1]
            team_record.away_wins = record[3]
            team_record.neutral_wins = record[5]

            team_record.home_losses = record[2]
            team_record.away_losses = record[4]
            team_record.neutral_losses = record[6]

            team_record.point_diff = record[8]

            opponents = self.get_opponent_names(team_id)
            team_record.fcs_opponents = opponents['fcs_count']
            team_record.opponents = opponents['opponents']

            # print(f'team: {team_name} '
            #       f'wins: {team_record.get_total_wins()} '
            #       f'losses: {team_record.get_total_losses()} '
            #       f'point_diff: {team_record.point_diff}')
            team_records.append(team_record)
            break

        print('count of team_records', len(team_records))
        team_records.sort(key=lambda x: (-x.get_total_wins(), x.get_total_losses(), x.fcs_opponents, -x.point_diff))
        for team_record in team_records:
            print(f'team: {team_record.team_name} '
                  f'wins: {team_record.get_total_wins()} '
                  f'losses: {team_record.get_total_losses()} '
                  f'point_diff: {team_record.point_diff} '
                  f'fcs_opponent_count: {team_record.fcs_opponents} '
                  f'opponents: {team_record.opponents}')

    def get_team_name(self, team_id):
        sql_get_team = f"SELECT team_name FROM teams where team_id = {team_id}"
        get_team_cursor = self.conn.cursor()
        get_team_cursor.execute(sql_get_team)
        team_name = get_team_cursor.fetchone()[0]
        return team_name

    # def get_fcs_opponent_count(self, team_id):
    #     sql_get_fcs_opponent_count = f"SELECT count(*) FROM season_opponents WHERE team_id = {team_id} and opponent_id = -1"
    #     get_fcs_count_cursor = self.conn.cursor()
    #     get_fcs_count_cursor.execute(sql_get_fcs_opponent_count)
    #     count = get_fcs_count_cursor.fetchone()[0]
    #     return count

    def get_opponent_names(self, team_id):
        fcs_count = 0
        opponent_names = []

        sql_get_opponent_names = f"SELECT * FROM season_opponents WHERE team_id = {team_id}"
        get_opponents_cursor = self.conn.cursor()
        get_opponents_cursor.execute(sql_get_opponent_names)

        opponent_results = get_opponents_cursor.fetchall()

        for result in opponent_results:
            print(f'opponent {result}')
            opponent_id = result[1]
            if opponent_id == -1:
                fcs_count += 1
            else:
                opponent_name = self.get_team_name(opponent_id)
                opponent_names.append(opponent_name)

        print(f'opponent_names {opponent_names}')
        result = {"fcs_count": fcs_count, "opponents": opponent_names}
        print(f'result {result}')
        return result
