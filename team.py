"""
Team info and methods to update that data
"""
from team_record import TeamRecord
from game_record import GameRecord
import psycopg2
import sys


class Team:

    def __init__(self, name, GameRecord=None):
        self.name = str(name)
        self.name = name.replace('\'', '\'\'')

        self.conn = psycopg2.connect("dbname=cfb_rankings user=postgres password=postgres")

        self.team_id = self.get_team_id()
        self.record = GameRecord

    def get_team_id(self):
        sql_get_team_id = f"SELECT team_id from teams where team_name = '{self.name}'"
        team_id_cursor = self.conn.cursor()
        team_id_cursor.execute(sql_get_team_id)
        team_id = team_id_cursor.fetchone()[0]
        return team_id

    def get_win_loss(self):
        """sql call that returns wins and losses"""


    # def get_record_id(self, season):

    def update_record(self, season):
        """update the record associated with a team for a given season"""
        sql_get_team_record = f"SELECT record_id FROM records WHERE team_id = {self.team_id} AND season = {season}"
        cur_get_team_record = self.conn.cursor()
        cur_get_team_record.execute(sql_get_team_record)

        if cur_get_team_record.rowcount != 0:
            record_id = cur_get_team_record.fetchone()[0]
            cur_get_team_record.close()
        else:
            print(f'create a new record for {self.name}')
            sql_create_team_record = f'INSERT INTO records(team_id, season) VALUES({self.team_id}, {season}) ' \
                                     f'RETURNING record_id;'
            cur_create_team_record = self.conn.cursor()
            try:
                cur_create_team_record.execute(sql_create_team_record)
                record_id = cur_create_team_record.fetchone()[0]
                self.conn.commit()
                cur_create_team_record.close()
            except Exception as error:
                print(f'Unable to create record for {self.name} in the {season} season: {error}')
                sys.exit()

        print(f'record_id for {self.name}: {record_id}')

        sql_update_record = f"UPDATE records set {self.record.win_loss_type} = " \
            f"{self.record.win_loss_type} + 1, point_diff = point_diff + {self.record.point_diff} " \
            f"WHERE record_id = {record_id}"

        sql_update_opponents = f"INSERT INTO season_opponents(record_id, team_id) VALUES({record_id}, " \
                               f"{self.record.get_opponents()})"

        # print(sql_update_record)
        try:
            cur_update_record = self.conn.cursor()
            cur_update_record.execute(sql_update_record)
            self.conn.commit()
            cur_update_record.close()
        except Exception as error:
            print(f'Unable to update game record for {self.name} using this statement: {sql_update_record} because'
                  f'of {error}')

        # def get_record_id():

    def get_opponents_win_loss(self):
        """sql call to get the win loss records of all opponents"""
