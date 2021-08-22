"""
Team Attributes
 1. Static team info
 2. Wins, Losses as integers
 3. Opponents as a list of Team objects containing their name and record

"""


class Team:

    def __init__(self):
        self.name = ''
        self.total_wins = 0
        self.total_losses = 0
        self.opponents = []
        self.point_differential = 0
        self.game_location = ''

    def get_win_loss(self):
        """sql call that returns wins and losses"""

    def get_opponents(self):
        """sql call that returns list of opponents as Team objects"""
        opponents = [Team()]
        return opponents

    def update_win_loss(self, wins=None, losses=None):
        """sql call to update win loss"""

    def update_opponents(self, opponent):
        """sql call to update a list of opponents"""

    def get_opponents_win_loss(self):
        """sql call to get the win loss records of all opponents"""
        opponents = self.get_opponents()
        for opponent in opponents:
            opponent.get_record()
