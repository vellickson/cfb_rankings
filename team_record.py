"""
Define a team's progress throughout the year
"""


class TeamRecord:

    def __init__(self, team):
        self.team_name = team
        self.home_wins = 0
        self.home_losses = 0
        self.away_wins = 0
        self.away_losses = 0
        self.neutral_wins = 0
        self.neutral_losses = 0
        self.point_diff = 0
        self.opponents = []
        self.season = 0

    # TODO: get_opponents
    def get_opponents(self):
        return self.opponents

    def get_total_wins(self):
        """aggregate home/away/neutral wins and losses"""
        return self.home_wins + self.away_wins + self.neutral_wins

    def get_total_losses(self):
        return self.home_losses + self.away_losses + self.neutral_losses



