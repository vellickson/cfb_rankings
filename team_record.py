"""
A team's progress throughout the year
"""
import psycopg2
from env import CONNECTION_STRING


class TeamRecord:

    def __init__(self, team_id, season):
        self.team_id = team_id
        self.season = season
        self.conn = psycopg2.connect(CONNECTION_STRING)
        self.home_wins = 0
        self.home_losses = 0
        self.away_wins = 0
        self.away_losses = 0
        self.neutral_wins = 0
        self.neutral_losses = 0
        self.point_diff = 0
        self.record_id = 0
        self.opponents = []
        self.fcs_opponents = 0
        self.get_record()

    def get_total_wins(self):
        """aggregate home/away/neutral wins"""
        return self.home_wins + self.away_wins + self.neutral_wins

    def get_total_losses(self):
        """aggregate home/away/neutral losses"""
        return self.home_losses + self.away_losses + self.neutral_losses

    def get_record(self):
        sql_get_record = f"SELECT * FROM team_records where season = {self.season} and team_id = {self.team_id}"
        # print('sql: ', sql_get_record)
        get_record_cursor = self.conn.cursor()
        get_record_cursor.execute(sql_get_record)
        record = get_record_cursor.fetchone()
        # print('record: ', record)

        self.home_wins = record[1]
        self.away_wins = record[3]
        self.neutral_wins = record[5]

        self.home_losses = record[2]
        self.away_losses = record[4]
        self.neutral_losses = record[6]

        self.record_id = record[7]
        self.point_diff = record[8]





