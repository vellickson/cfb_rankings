"""
Defines a team's progress throughout the year
"""


class Record:

    def __init__(self):
        self.win_loss = { 'wins': 0, 'loss': 0 }
        self.home_wins = 0
        self.home_losses = 0
        self.away_wins = 0
        self.away_losses = 0
        self.neutral_wins = 0
        self.neutral_losses = 0
        self.point_diff = 0
        self.opponents = []
        self.season = 0

    def add_opponent(self, opponent):
        self.opponents.append(opponent)

    def get_opponents(self):
        return self.opponents

    def update_point_differential(self, points):
        self.point_diff += points

    def get_win_loss(self):
        """aggregate home/away/neutral wins and losses"""
        return self.win_loss

    def get_point_differential(self):
        return self.point_diff


