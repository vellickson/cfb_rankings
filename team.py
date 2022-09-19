"""
Team info and methods to update that data
"""
from team_record import TeamRecord
from game_record import GameRecord
import psycopg2
import sys
from env import CONNECTION_STRING


class Team:

    def __init__(self, season, name=None, team_id=None):
        self.conn = psycopg2.connect(CONNECTION_STRING)
        self.season = season
        if name:
            self.name = str(name).replace('\'', '\'\'')
        else:
            self.name = None
        self.team_id = team_id
        self.get_team_info()
        self.team_record = self.get_season_record()

    def get_team_info(self):
        sql_get_team = None
        if self.name:
            sql_get_team = f"SELECT * from teams where team_name = '{self.name}'"
        elif self.team_id:
            sql_get_team = f"SELECT * from teams where team_id = {self.team_id}"
        team_id_cursor = self.conn.cursor()
        team_id_cursor.execute(sql_get_team)
        result = team_id_cursor.fetchone()
        # print(f'sql: {sql_get_team}')
        # print(f'result: {result}')
        self.team_id = result[0]
        self.name = result[1]
        team_id_cursor.close()

    def get_season_record(self):
        record = TeamRecord(self.team_id, self.season)
        # print(f'record from team.get_season_record {record}')
        if record.record_id != 0:
            # print('record is not None')
            return record
        else:
            return None

    def get_win_loss(self):
        """sql call that returns wins and losses"""

    # def get_record_id(self, season):

    def update_record(self, season, game_record):
        """update the record associated with a team for a given season"""
        record_id = self.get_season_record().record_id
        # print(f'record_id for {self.name}: {record_id}')

        sql_update_record = f"UPDATE team_records set {game_record.win_loss_type} = " \
            f"{game_record.win_loss_type} + 1, " \
            f"point_diff = point_diff + {game_record.point_diff} " \
            f"WHERE record_id = {record_id}"

        # print(f'update_record: {sql_update_record}')

        sql_update_opponents = f"INSERT INTO season_opponents(record_id, opponent_id) VALUES({record_id}, " \
                               f"{game_record.opponent})"

        # print(f'game_record.opponent {game_record.opponent}')
        # print(f'update_opponents {sql_update_opponents}')

        try:
            cur_update_record = self.conn.cursor()
            cur_update_record.execute(sql_update_record)
            cur_update_record.execute(sql_update_opponents)
            self.conn.commit()
            cur_update_record.close()
        except Exception as error:
            print(f'Unable to update game record for {self.name} using this statement: {sql_update_record} because'
                  f'of {error}')

    # def get_season_record(self, season):
    #     """retrieve season record"""
    #     sql_get_team_record = f"SELECT record_id FROM records WHERE team_id = {self.team_id} AND season = {season}"
    #     cur_get_team_record = self.conn.cursor()
    #
    #     try:
    #         cur_get_team_record.execute(sql_get_team_record)
    #     except Exception as error:
    #         print(f'unable to retrieve season record_id: {error}')
    #
    #     if cur_get_team_record.rowcount != 0:
    #         record_id = cur_get_team_record.fetchone()[0]
    #         cur_get_team_record.close()
    #     else:
    #         record_id = self.create_season_record(season)
    #
    #     return record_id

    def create_season_record(self, season):
        """create a record for the season"""
        # print(f'create a new record for {self.name}')
        sql_create_team_record = f'INSERT INTO team_records (team_id, season) VALUES({self.team_id}, {season}) ' \
                                 f'RETURNING record_id;'
        cur_create_team_record = self.conn.cursor()

        try:
            cur_create_team_record.execute(sql_create_team_record)
            record_id = cur_create_team_record.fetchone()[0]
            self.conn.commit()
            cur_create_team_record.close()
            return record_id
        except Exception as error:
            print(f'Unable to create record for {self.name} in the {season} season: {error}')
            sys.exit()

    def get_opponents_win_loss(self):
        """sql call to get the win loss records of all opponents"""
