"""
Team Attributes
 1. Static team info
 2. Wins, Losses as integers
 3. Opponents as a list of Team objects containing their name and record

"""
from record import Record

class Team:

    def __init__(self):
        self.name = ''
        self.total_wins = 0
        self.total_losses = 0
        self.opponents = []
        self.game_point_differential = 0
        self.game_location = ''
        self.record = Record()

    def get_win_loss(self):
        """sql call that returns wins and losses"""

    def get_opponents(self):
        """sql call that returns list of opponents as Team objects"""
        return self.opponents

    def get_record(self):
        """return win-loss record of this team"""

    def update_record(self, we_won=False, season=2019, week=0):
        """sql call to update win loss"""
        sql = 'UPDATE records set '
        if we_won:
            sql += self.game_location + "_wins blah blah"
        else:
            sql += self.game_location + "_losses blah blah"

    def get_opponents_win_loss(self):
        """sql call to get the win loss records of all opponents"""
        for opponent in self.opponents:
            opponent.get_record()
