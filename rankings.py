"""
Determine rankings for each team
1. Foreach known team, get its aggregate win loss record and the win loss record of its opponents
2. Calculate rankings
3. Output list
"""

import psycopg2
from env import CONNECTION_STRING
from team import Team


class Rankings:
    def __init__(self, season):
        self.season = season
        self.conn = psycopg2.connect(CONNECTION_STRING)

    def rank_teams(self):
        # Iterate through each team and aggregate their wins/losses
        sql_get_teams = f"SELECT team_id FROM teams"
        get_teams_cursor = self.conn.cursor()
        get_teams_cursor.execute(sql_get_teams)
        results = get_teams_cursor.fetchall()
        compiled_results = []
        i = 0
        for result in results:
            i += 1
            compiled_result = None
            # print(result[0])
            team_id = result[0]
            # print(result[0])
            team = Team(self.season, team_id=team_id)

            # this should be a list of Team objects
            opponents = self.get_opponents(team.team_record.record_id)
            # opponents = self.get_opponents(record_id)
            compiled_result = {"name": team.name,
                               "wins": team.team_record.get_total_wins(),
                               "losses": team.team_record.get_total_losses(),
                               "point_diff": team.team_record.point_diff,
                               "fcs_count": opponents['fcs_count'],
                               "opponent_total_wins": opponents['opponent_total_wins'],
                               "opponent_total_losses": opponents['opponent_total_losses'],
                               "opponents": opponents['opponents']
                               }
            compiled_results.append(compiled_result)
            if i > 131:
                break
            # break

        compiled_results.sort(key=lambda x: (
            -x["wins"], x["losses"], x["fcs_count"], -x["opponent_total_wins"], x["opponent_total_losses"], -x["point_diff"]))
        print('name, wins, losses, fcs_count, opponent_total_wins, opponent_total_losses, point_diff, opponents')
        for record in compiled_results:
            # print(f"record: {record}")
            print(
                f"{record['name']}, "
                f"{record['wins']}, "
                f"{record['losses']}, "
                f"{record['fcs_count']}, "
                f"{record['opponent_total_wins']}, "
                f"{record['opponent_total_losses']}, "
                f"{record['point_diff']}, "
                f"{record['opponents']}")

            # team_record.power_five_opponents = opponents['power_five']

            # print(f'team: {team_name} '
            #       f'wins: {team_record.get_total_wins()} '
            #       f'losses: {team_record.get_total_losses()} '
            #       f'point_diff: {team_record.point_diff}')
            # team_records.append(team_record)

        # # Iterate through each record and aggregate wins/losses
        # sql_get_record = f"SELECT * FROM records where season = {self.season}"
        # get_record_cursor = self.conn.cursor()
        # get_record_cursor.execute(sql_get_record)
        # # print(f'cursor_description {get_record_cursor.description}')
        # columns = get_record_cursor.description
        # team_records = []
        #
        # # print(f'col 0 {columns[0].name}')
        # for record in get_record_cursor:
        #     team_id = record[0]
        #     # print(f'team_id {team_id}')
        #     team_name = self.get_team_name(team_id)
        #     team_record = TeamRecord(team_name, self.season)
        #
        #     team_record.home_wins = record[1]
        #     team_record.away_wins = record[3]
        #     team_record.neutral_wins = record[5]
        #
        #     team_record.home_losses = record[2]
        #     team_record.away_losses = record[4]
        #     team_record.neutral_losses = record[6]
        #
        #     team_record.point_diff = record[8]
        #     record_id = record[7]
        #
        #     # this should be a list of Team objects
        #     opponents = self.get_opponent_names(record_id)
        #     # opponents = self.get_opponents(record_id)
        #     team_record.fcs_opponents = opponents['fcs_count']
        #     team_record.opponents = opponents['opponents']
        #     # team_record.power_five_opponents = opponents['power_five']
        #
        #     # print(f'team: {team_name} '
        #     #       f'wins: {team_record.get_total_wins()} '
        #     #       f'losses: {team_record.get_total_losses()} '
        #     #       f'point_diff: {team_record.point_diff}')
        #     team_records.append(team_record)
        #     # break
        #
        # # print('count of team_records', len(team_records))
        # team_records.sort(key=lambda x: (-x.get_total_wins(), x.get_total_losses(), x.fcs_opponents, -x.point_diff))
        # print('team, wins, losses, point_diff, fcs_opponent_count, opponents')
        # for team_record in team_records:
        #     print(f'{team_record.team_name},'
        #           f'{team_record.get_total_wins()},'
        #           f'{team_record.get_total_losses()},'
        #           f'{team_record.point_diff},'
        #           f'{team_record.fcs_opponents},',
        #           *team_record.opponents, sep=' ')

    # def get_team_name(self, team_id):
    #     sql_get_team = f"SELECT team_name, conference FROM teams where team_id = {team_id}"
    #     # print(f'sql_get_team {sql_get_team}')
    #     get_team_cursor = self.conn.cursor()
    #     get_team_cursor.execute(sql_get_team)
    #     team_name = get_team_cursor.fetchone()[0]
    #     # result = get_team_cursor.fetchall()
    #     # team_name = result[0][0]
    #     # conference = result[0][1]
    #     # print(f'team_name: {team_name} conference: {conference}')
    #     return team_name

    def get_opponents(self, record_id):
        fcs_count = 0
        opponents = []

        sql_get_opponents = f"SELECT * FROM season_opponents WHERE record_id = {record_id}"
        get_opponents_cursor = self.conn.cursor()
        get_opponents_cursor.execute(sql_get_opponents)

        results = get_opponents_cursor.fetchall()
        total_opponent_wins = 0
        total_opponent_losses = 0

        for result in results:
            # print(f'opponent {result}')
            opponent_id = result[2]
            if opponent_id == -1:
                fcs_count += 1
            else:
                opponent = Team(self.season, team_id=opponent_id)
                opponent_wins = opponent.team_record.get_total_wins()
                opponent_losses = opponent.team_record.get_total_losses()
                opponent_win_loss = f'{opponent_wins} - {opponent_losses}'
                opponent_str = f'{opponent.name} ({opponent_win_loss})'
                opponents.append(opponent_str)
                total_opponent_wins += opponent_wins
                total_opponent_losses += opponent_losses

        # print(f'opponent_names {opponent_names}')
        result = {
            "fcs_count": fcs_count,
            "opponents": opponents,
            "opponent_total_wins": total_opponent_wins,
            "opponent_total_losses": total_opponent_losses
        }
        # print(f'result {result}')
        return result
