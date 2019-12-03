import engine.OthelloInterface as interface
from engine.OthelloEngine import get_all_moves


class LimitedDepthSearch(interface.Othello_AI):
    def __init__(self, team_type, board_size, time_limit):
        interface.Othello_AI.__init__(self, team_type, board_size, time_limit)

    def get_move(self, board_state):
        moves = get_all_moves(board_state, self.team_type)
        return moves[0]

    def get_team_name(self):
        return 'Some-Team-Name'
