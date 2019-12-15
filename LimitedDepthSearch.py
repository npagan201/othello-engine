import engine.OthelloInterface as interface
import engine.OthelloEngine as engine


class LimitedDepthSearch(interface.Othello_AI):
    def __init__(self, team_type, board_size, time_limit):
        interface.Othello_AI.__init__(self, team_type, board_size, time_limit)

    def get_move(self, board_state):
        moves = engine.get_all_moves(board_state, self.team_type)
        board_list = [board_state] * len(moves)

        return moves[0]

    def get_team_name(self):
        return 'Some-Team-Name'


   # Perform move
   def update_board(self, move):
      # move format: ('B', (i, j)) or ('B', None)
      # update the board state given the current move
      # if the move is None, do nothing
      # Assume that is a valid move, no need for extra error checking
      if move[1] is not None:
         r = move[1][0]
         c = move[1][1]
         color = move[0]

         #left
         i = r
         j = c - 1
         while j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c-1
                  for index in range(c - j - 1):
                     self.game_state[i][j + index + 1] = color
               #end the loop
               break

         #left-up direction
         i = r - 1
         j = c - 1
         while i >= 0 and j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c-1, r-1
                  for index in range(c - j - 1):
                     self.game_state[i + index + 1][j + index + 1] = color
               #end the loop
               break

         #up
         i = r -1
         j = c
         while i >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r-1
                  for index in range(r - i - 1):
                     self.game_state[i + index + 1][j] = color
               #end the loop
               break

         #right-up direction
         i = r - 1
         j = c + 1
         while i >= 0 and j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r-1, c+1
                  for index in range(r - i - 1):
                     self.game_state[i + index + 1][j - index - 1] = color
               #end loop
               break

         #right direction
         i = r
         j = c + 1
         while j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c+1
                  for index in range(j - c - 1):
                     self.game_state[i][j - index - 1] = color
               #end loop
               break

         #right-down
         i = r + 1
         j = c + 1
         while i < len(self.game_state) and j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1,c+1
                  for index in range(j - c - 1):
                     self.game_state[i - index - 1][j - index - 1] = color
               #end loop
               break

         #down
         i = r + 1
         j = c
         while i < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1
                  for index in range(i - r - 1):
                     self.game_state[i - index - 1][j] = color
               #end loop
               break

         #left-down
         i = r + 1
         j = c - 1
         while i < len(self.game_state) and j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1
                  for index in range(i - r - 1):
                     self.game_state[i - index - 1][j + index + 1] = color
               #end loop
               break

         #set the spot in the game_state
         self.game_state[r][c] = color


def opposite_type(team_type):
    if team_type == 'B':
        return 'W'
    else:
        return 'B'


def alpha_beta_search(board_state, team_type, depth, alpha=-100, beta=100, max_player=True):
    if depth == 0:
        return 0

    if max_player:
        best_value = -100
        for move in engine.get_all_moves(board_state, team_type):
            new_board = update_board(board_state, move)
            opposite = opposite_type(team_type)
            best_value = max(best_value, alpha_beta_search(new_board, opposite, depth-1, alpha, beta, False))
            alpha = max(alpha, best_value)
            # Prune values if there is a need
            if alpha >= beta:
                break
        return best_value

    else:
        best_value = 100
        for move in engine.get_all_moves(board_state, team_type):
            new_board = update_board(board_state, move)
            opposite = opposite_type(team_type)
            best_value = min(best_value, alpha_beta_search(new_board, opposite, depth-1, alpha, beta, True))
            beta = min(beta, best_value)
            # Prune values if there is a need
            if alpha >= beta:
                break
        return best_value
