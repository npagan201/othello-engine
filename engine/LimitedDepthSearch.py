import OthelloInterface as interface
import OthelloEngine as engine


class Othello_AI(interface.Othello_AI):
    def __init__(self, team_type, board_size, time_limit):
        interface.Othello_AI.__init__(self, team_type, board_size, time_limit)

    def get_move(self, board_state):
        return alpha_beta_search(board_state, self.team_type, 7)[0]

    def get_team_name(self):
        return 'Some-Team-Name'


# Perform move
def update_board(board_state, move):
    # move format: ('B', (i, j)) or ('B', None)
    # update the board state given the current move
    # if the move is None, do nothing
    # Assume that is a valid move, no need for extra error checking
    if move[1] is not None:
        r = move[1][0]
        c = move[1][1]
        color = move[0]

        # left
        i = r
        j = c - 1
        while j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                j -= 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at c-1
                    for index in range(c - j - 1):
                        board_state[i][j + index + 1] = color
                # end the loop
                break

        # left-up direction
        i = r - 1
        j = c - 1
        while i >= 0 and j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i -= 1
                j -= 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at c-1, r-1
                    for index in range(c - j - 1):
                        board_state[i + index + 1][j + index + 1] = color
                # end the loop
                break

        # up
        i = r - 1
        j = c
        while i >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i -= 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at r-1
                    for index in range(r - i - 1):
                        board_state[i + index + 1][j] = color
                # end the loop
                break

        # right-up direction
        i = r - 1
        j = c + 1
        while i >= 0 and j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i -= 1
                j += 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at r-1, c+1
                    for index in range(r - i - 1):
                        board_state[i + index + 1][j - index - 1] = color
                # end loop
                break

        # right direction
        i = r
        j = c + 1
        while j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                j += 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at c+1
                    for index in range(j - c - 1):
                        board_state[i][j - index - 1] = color
                # end loop
                break

        # right-down
        i = r + 1
        j = c + 1
        while i < len(board_state) and j < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i += 1
                j += 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at r+1,c+1
                    for index in range(j - c - 1):
                        board_state[i - index - 1][j - index - 1] = color
                # end loop
                break

        # down
        i = r + 1
        j = c
        while i < len(board_state):
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i += 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at r+1
                    for index in range(i - r - 1):
                        board_state[i - index - 1][j] = color
                # end loop
                break

        # left-down
        i = r + 1
        j = c - 1
        while i < len(board_state) and j >= 0:
            if board_state[i][j] != color and board_state[i][j] != '-':
                # it's opposite color, keep checking
                i += 1
                j -= 1
            else:
                if board_state[i][j] == color:
                    # it's the same color, go back and change till we are at r+1
                    for index in range(i - r - 1):
                        board_state[i - index - 1][j + index + 1] = color
                # end loop
                break

        # set the spot in the game_state
        board_state[r][c] = color
        return board_state


def opposite_type(team_type):
    if team_type == 'B':
        return 'W'
    else:
        return 'B'


def alpha_beta_search(board_state, team_type, depth, alpha=float("-inf"), beta=float("inf"), max_player=True):
    move_list = engine.get_all_moves(board_state, team_type)
    best_move = None

    if depth == 0:
        return best_move, sum(row.count(team_type) for row in board_state)

    if len(move_list) == 0:
        return None, 0

    if max_player:
        best_value = float("-inf")
        for move in move_list:
            new_board = update_board(board_state, move)
            opposite = opposite_type(team_type)
            score = alpha_beta_search(new_board, opposite, depth - 1, alpha, beta, False)[1]
            if score > best_value:
                best_value = score
                best_move = move
            alpha = max(alpha, best_value)
            # Prune values if there is a need
            if alpha >= beta:
                break
        return best_move, best_value

    else:
        best_value = float("inf")
        for move in move_list:
            new_board = update_board(board_state, move)
            opposite = opposite_type(team_type)
            score = alpha_beta_search(new_board, opposite, depth - 1, alpha, beta, True)[1]
            if score < best_value:
                best_value = score
                best_move = move
            beta = min(beta, best_value)
            # Prune values if there is a need
            if alpha >= beta:
                break
        return best_move, best_value


def coin_parity(board_state, team_type):
    '''
    Coin Parity Heuristic Value =
    	100 * (Max Player Coins - Min Player Coins ) / (Max Player Coins + Min Player Coins)
    '''
    value = 0
    maxP = 0
    minP = 0
    for i in range(len(board_state)):
        for j in range(len(board_state[i])):
            if j == 'B':
                if team_type == 'B':
                    maxP += 1
                else:
                    minP += 1
            elif j == 'W':
                if team_type == 'W':
                    maxP += 1
                else:
                    minP += 1
    value = 100 * ((maxP - minP) / (maxP + minP))
    return value


def mobility(board_state, team_type):
    '''
    	if ( Max Player Moves + Min Player Moves != 0)
    		Mobility Heuristic Value =
    			100 * (Max Player Moves - Min Player Moves) / (Max Player Moves + Min Player Moves)
    	else
    		Mobility Heuristic Value = 0
    	'''
    if team_type == 'B':
        team = 'B'
        maxM = engine.get_all_moves(board_state, team)
        minM = engine.get_all_moves(board_state, 'W')

    else:
        team = 'W'
        maxM = engine.get_all_moves(board_state, team)
        minM = engine.get_all_moves(board_state, 'B')
    if (maxM + minM != 0):
        mobile = 100 * ((maxM - minM) / (maxM + minM))
    else:
        mobile = 0
    return mobile


def corners(board_state, team_type):
    '''
    	if ( Max Player Corners + Min Player Corners != 0)
    		Corner Heuristic Value =
    			100 * (Max Player Corners - Min Player Corners) / (Max Player Corners + Min Player Corners)
    	else
    		Corner Heuristic Value = 0
    	'''
    value = 0
    maxC = 0
    minC = 0
    if team_type == 'B':
        if board_state[0][0] == 'B':
            maxC += 1
        elif board_state[0][0] == 'W':
            minC += 1

        if board_state[0][len(board_state) - 1] == 'B':
            maxC += 1
        elif board_state[0][len(board_state) - 1] == 'W':
            minC += 1

        if board_state[len(board_state) - 1][0] == 'B':
            maxC += 1
        elif board_state[len(board_state) - 1][0] == 'W':
            minC += 1

        if board_state[len(board_state) - 1][len(board_state) - 1] == 'B':
            maxC += 1
        elif board_state[len(board_state) - 1][len(board_state) - 1] == 'W':
            minC += 1
    else:
        if board_state[0][0] == 'W':
            maxC += 1
        elif board_state[0][0] == 'B':
            minC += 1

        if board_state[0][len(board_state) - 1] == 'W':
            maxC += 1
        elif board_state[0][len(board_state) - 1] == 'B':
            minC += 1

        if board_state[len(board_state) - 1][0] == 'W':
            maxC += 1
        elif board_state[len(board_state) - 1][0] == 'B':
            minC += 1

        if board_state[len(board_state) - 1][len(board_state) - 1] == 'W':
            maxC += 1
        elif board_state[len(board_state) - 1][len(board_state) - 1] == 'B':
            minC += 1

    if maxC + minC != 0:
		value = 100 * (maxC - minC) / (maxC + minC)
    else:
		value = 0
    return value


def stability(board_state, team_type):
    '''
    if ( Max Player Stability Value + Min Player Stability Value != 0)
        Stability  Heuristic Value =
            100 * (Max Player Stability Value - Min Player Stability Value) / (Max Player Stability Value + Min Player Stability Value)
    else
        Stability Heuristic Value = 0

    '''
    value = 0
    maxS = 0
    minS = 0
    if team_type == 'B':
        if board_state[0][0] == 'B':
            maxS += 1
        elif board_state[0][0] == 'W':
            minS += 1

        if board_state[0][len(board_state) - 1] == 'B':
            maxS += 1
        elif board_state[0][len(board_state) - 1] == 'W':
            minS += 1

        if board_state[len(board_state) - 1][0] == 'B':
            maxS += 1
        elif board_state[len(board_state) - 1][0] == 'W':
            minS += 1

        if board_state[len(board_state) - 1][len(board_state) - 1] == 'B':
            maxS += 1
        elif board_state[len(board_state) - 1][len(board_state) - 1] == 'W':
            minS += 1

        for i in range(1, len(board_state[0] - 1)):  # top row
            if (board_state[0][i - 1]) and (board_state[0][i + 1]) != 'W':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # bottom row
            if (board_state[len(board_state) - 1][i - 1]) and (board_state[len(board_state) - 1][i + 1]) != 'W':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # left col
            if (board_state[i - 1][0]) and (board_state[i + 1][0]) != 'W':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # right col
            if (board_state[i - 1][len(board_state) - 1]) and (board_state[i + 1][len(board_state) - 1]) != 'W':
                maxS += 1
            else:
                minS += 1

        for i in range(len(board_state) - 2):
            for j in range(len(board_state[i]) - 2):
                if (board_state[i - 1][j - 1] != 'W') \
                        and (board_state[i][j - 1] != 'W') \
                        and (board_state[i - 1][j] != 'W') \
                        and (board_state[i + 1][j + 1] != 'W') \
                        and (board_state[i + 1][j] != 'W') \
                        and (board_state[i][j + 1] != 'W') \
                        and (board_state[i + 1][j - 1] != 'W') \
                        and (board_state[i - 1][j + 1] != 'W'):
                    maxS += 1
                else:
                    maxS -= 1

    else:
        if board_state[0][0] == 'W':
            maxS += 1
        elif board_state[0][0] == 'B':
            minS += 1

        if board_state[0][len(board_state) - 1] == 'W':
            maxS += 1
        elif board_state[0][len(board_state) - 1] == 'B':
            minS += 1

        if board_state[len(board_state) - 1][0] == 'W':
            maxS += 1
        elif board_state[len(board_state) - 1][0] == 'B':
            minS += 1

        if board_state[len(board_state) - 1][len(board_state) - 1] == 'W':
            maxS += 1
        elif board_state[len(board_state) - 1][len(board_state) - 1] == 'B':
            minS += 1

        for i in range(1, len(board_state[0] - 1)):  # top row
            if (board_state[0][i - 1]) and (board_state[0][i + 1]) != 'B':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # bottom row
            if (board_state[len(board_state) - 1][i - 1]) and (board_state[len(board_state) - 1][i + 1]) != 'B':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # left col
            if (board_state[i - 1][0]) and (board_state[i + 1][0]) != 'B':
                maxS += 1
            else:
                minS += 1

        for i in range(1, len(board_state[0]) - 1):  # right col
            if (board_state[i - 1][len(board_state) - 1]) and (board_state[i + 1][len(board_state) - 1]) != 'B':
                maxS += 1
            else:
                minS += 1

    for i in range(len(board_state) - 2):
        for j in range(len(board_state[i]) - 2):
            if (board_state[i - 1][j - 1] != 'B') \
                    and (board_state[i][j - 1] != 'B') \
                    and (board_state[i - 1][j] != 'B') \
                    and (board_state[i + 1][j + 1] != 'B') \
                    and (board_state[i + 1][j] != 'B') \
                    and (board_state[i][j + 1] != 'B') \
                    and (board_state[i + 1][j - 1] != 'B') \
                    and (board_state[i - 1][j + 1] != 'B'):
                maxS += 1
            else:
                maxS -= 1

    if maxS + minS != 0:
        value = 100 * (maxS - minS) / (maxS + minS)
    else:
        value = 0
    return value


def heuristics(board_state, team_type):
    value = 0
    value += coin_parity(board_state, team_type)
    value += mobility(board_state, team_type)
    value += corners(board_state, team_type)
    value += stability(board_state, team_type)
    return value
