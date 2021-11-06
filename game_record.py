"""
Define a team's progress throughout the year
"""

class GameRecord:

    def __init__(self, team):
        self.team_name = team
        self.point_diff = None
        self.opponent = None
        self.game_location = None
        self.win_loss_type = None

    def set_win_loss_outcome(self, we_won):
        if self.game_location == 'home':
            if we_won:
                self.win_loss_type = 'home_wins'
            else:
                self.win_loss_type = 'home_losses'
        elif self.game_location == 'away':
            if we_won:
                self.win_loss_type = 'road_wins'
            else:
                self.win_loss_type = 'road_losses'
        else:
            if we_won:
                self.win_loss_type = 'neutral_wins'
            else:
                self.win_loss_type = 'neutral_losses'
