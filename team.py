"""
Team info and methods to update that data
"""
from record import Record
import psycopg2


class Team:

    def __init__(self, name):
        self.name = name
        self.record = Record()
        self.team_id = None
        self.conn = psycopg2.connect("dbname=cfb_rankings user=postgres password=dbuser")
        self.cur = self.conn.cursor()
        sql = f"SELECT team_id from teams where team_name = '{self.name}'"
        self.cur.execute(sql)
        self.conn.commit()
        row = self.cur.fetchone()

        while row is not None:
            print(row)

    def get_win_loss(self):
        """sql call that returns wins and losses"""

    # def get_opponents(self):
    #     """sql call that returns list of opponents as Team objects"""
    #     return self.opponents

    def get_record(self):
        """return win-loss record of this team"""

    def update_record(self):
        """sql call to update win loss"""

        sql = f"UPDATE records set {self.record.win_loss_type} = " \
              f"{self.record.win_loss_type} + 1 WHERE team_id = {self.team_id}"

    def get_opponents_win_loss(self):
        """sql call to get the win loss records of all opponents"""
