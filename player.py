import math
import random
from board import Board


class Player:

    def __init__(self, max_depth):
        self.max_depth = max_depth

    P1_WIN_SCORE = 200
    P2_WIN_SCORE = -200
    TIE_SCORE = 0

class ManualPlayer(Player):
    label = "Manual"

    def findMove(self, move_history):
        board = Board(move_history)
        opts = " "
        for c in range(7):
            opts += (str(c+1) if board.isValidMove(c) else ' ')+"  "

        while True:
            if(board.turn == 1):
                print("\n")
                board.printBoard()
                print(opts)
                pit = input("Pick a column (P1): ")
            try: pit = int(pit) - 1
            except ValueError: continue
            if board.isValidMove(pit):
                return pit

class PlayerRandom(Player):
    label = "Random"

    def findMove(self, move_history):
        board = Board(move_history)
        moves = board.getPossibleMoves()
        return random.choice(moves)


class PlayerMM(Player):
    label = "Minimax"
    moves_considered = 0

    def heuristic(self, board):
        h = 0
        for row in range(0, 6):
            if board.board[(row*7) + 3] == board.turn:
                h += 2
        return h

    def heuristic1(self,board):
        h = 0
        if(7 - board.recent_move[1] + board.checkAdjacentSpacesHeuristic(board.recent_move) < 4):
            h -= 70

        if(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 2):
            h += 10
        elif(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 3):
            h += 25
        elif(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 4):
            h += 95

        if(board.checkAdjacentSpacesHeuristic(board.recent_move) == 2):
            h += 35
        elif(board.checkAdjacentSpacesHeuristic(board.recent_move) == 3):
            h += 50
        elif(board.checkAdjacentSpacesHeuristic(board.recent_move) == 4):
            h += 200

        if(board.turn == 2):
            h = h * -1
       
        return h

    def heuristic2(self, board):
        h = 0
        for space in board.board:
            if board.board[space] == 1: # player's turn
                if space == 0: # top left corner
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                elif space == 6: #top right corner
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                elif space == 41: # bottom right corner
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                elif space == 35: # bottom left corner
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                elif (space) % 7 == 0: # on the left border
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                elif (space) % 6 == 0: # on the right border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                elif (space + 7) > 42: # on the bottom border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                elif (space - 7) < 0: # on the top border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                else:
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 1 + 7] == 2 and board.board[space + 1 - 7] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 1 - 7] == 2 and board.board[space + 1 + 7] == 2: # in-between two opposing chips
                        h += 100
            elif board.board[space] == 2: #opponent checks ------------------------------------------------
                if space == 0: # top left corner
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                elif space == 6: #top right corner
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                elif space == 41: # bottom right corner
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                elif space == 35: # bottom left corner
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                elif (space) % 7 == 0: # on the left border
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                elif (space) % 6 == 0: # on the right border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                elif (space + 7) > 42: # on the bottom border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                elif (space - 7) < 0: # on the top border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                else:
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
        return h        

    def heuristic3(self, board):
        move = board.recent_move
        player = board.turn
        h = 0
        if player == 1:
            opp = 2
            h += board.checkAdjacentSpacesHeuristic(move)
        else:
            opp = 1
            h += board.checkAdjacentSpacesHeuristicEnemy(move)
        row = move[0]
        col = move[1]
        up_right = 0
        check = (row - 1, col + 1) # up-right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the top-right
                up_right += 1
            else:
                streak = False # there is not an opponent to the top-right
            check = (check[0] - 1, check[1] + 1) # moving further up-right
        right = 0
        check = (row, col + 1) # right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the right
                right += 1
            else:
                streak = False # there is not an opponent to the right
            check = (check[0], check[1] + 1) # moving further right
        bottom_right = 0
        check = (row + 1, col + 1) # bottom-right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom-right
                bottom_right += 1
            else:
                streak = False # there is not an opponent to the bottom-right
            check = (check[0] + 1, check[1] + 1) # moving further bottom-right
        bottom = 0
        check = (row + 1, col) # bottom
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom
                bottom += 1
            else:
                streak = False # there is not an opponent to the bottom
            check = (check[0], check[1] + 1) # moving further bottom
        bottom_left = 0
        check = (row + 1, col - 1) # bottom-left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom-left
                bottom_left += 1
            else:
                streak = False # there is not an opponent to the bottom-left
            check = (check[0] + 1, check[1] - 1) # moving further bottom-left
        left = 0
        check = (row, col - 1) # left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the left
                left += 1
            else:
                streak = False # there is not an opponent to the left
            check = (check[0], check[1] - 1) # moving further left
        up_left = 0
        check = (row - 1, col - 1) # up-left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the up-left
                up_left += 1
            else:
                streak = False # there is not an opponent to the up-left
            check = (check[0] - 1, check[1] - 1) # moving further up-left
        h += up_right + right + bottom_right + bottom + bottom_left + left + up_left
        if (up_right + bottom_left >= 3):
            h += 10
        if (right + left >= 3):
            h += 10
        if (bottom_right + up_left >= 3):
            h += 10
        if (up_right == 3 or right == 3 or bottom_right == 3 or bottom == 3 or bottom_left == 3 or left == 3 or up_left == 3):
            h += 10
        return h


    def minimax(self, board, depth):
        if board.game_over:
            if board.winner == 1:
                return (None, self.P1_WIN_SCORE)
            elif board.winner == 2:
                return (None, self.P2_WIN_SCORE)
            else:
                return None, self.TIE_SCORE

        h = self.heuristic3(board)
        # Value of max-depth states
        if (not board.game_over) and (depth == 0):
            return (None, h)

        if board.turn == 1:
            is_max = True
            best_value = -math.inf
        elif board.turn == 2:
            is_max = False
            best_value = math.inf

        valid_moves = board.getPossibleMoves()
        for move in valid_moves:
            self.moves_considered += 1

            board.makeMove(move)
            v = self.minimax(board, depth - 1)[1] # Value of minimax call from this board
            board.undoMove()

            if is_max:
                if v >= best_value:
                    best_value = v
                    best_move = move
            elif not is_max:
                if v <= best_value:
                    best_value = v
                    best_move = move

        result = (best_move, best_value)
        return result

    def findMove(self, move_history):
        board = Board(move_history)
        move, score = self.minimax(board, self.max_depth)
        return move


class PlayerAB(Player):
    label = "Alpha-Beta"
    moves_considered = 0

    def heuristic(self, board):
        h = 0
        for row in range(0, 6):
            if board.board[(row*7) + 3] == board.turn:
                h += 2
        return h

    def heuristic1(self,board):
        h = 0
        if(7 - board.recent_move[1] + board.checkAdjacentSpacesHeuristic(board.recent_move) < 4):
            h-= 70

        if(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 2):
            h += 10
        elif(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 3):
            h += 25
        elif(board.checkAdjacentSpacesHeuristicEnemy(board.recent_move) == 4):
            h += 95

        if(board.checkAdjacentSpacesHeuristic(board.recent_move) == 2):
            h += 35
        elif(board.checkAdjacentSpacesHeuristic(board.recent_move) == 3):
            h += 50
        elif(board.checkAdjacentSpacesHeuristic(board.recent_move) == 4):
            h += 200

        if(board.turn == 2):
            h = h * -1
       
        return h
    
    def heuristic2(self, board):
        h = 0
        for space in board.board:
            if board.board[space] == 1: # player's turn
                if space == 0: # top left corner
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                elif space == 6: #top right corner
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                elif space == 41: # bottom right corner
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                elif space == 35: # bottom left corner
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                elif (space) % 7 == 0: # on the left border
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                elif (space) % 6 == 0: # on the right border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                elif (space + 7) > 42: # on the bottom border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                elif (space - 7) < 0: # on the top border
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                else:
                    if board.board[space - 1] == 1: # check left
                        h += 1
                    if board.board[space + 1] == 1: # check right
                        h += 1
                    if board.board[space + 7] == 1: # check above
                        h += 1
                    if board.board[space - 1] == 1: # check below
                        h += 1
                    if board.board[space - 1 - 7] == 1: # check top left
                        h += 1
                    if board.board[space + 1 - 7] == 1: # check top right
                        h += 1
                    if board.board[space + 1 + 7] == 1: # check bottom right
                        h += 1
                    if board.board[space - 1 + 7] == 1: # check bottom left
                        h += 1
                    if board.board[space - 1] == 2 and board.board[space + 1] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 7] == 2 and board.board[space + 7] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 1 + 7] == 2 and board.board[space + 1 - 7] == 2: # in-between two opposing chips
                        h += 100
                    if board.board[space - 1 - 7] == 2 and board.board[space + 1 + 7] == 2: # in-between two opposing chips
                        h += 100
            elif board.board[space] == 2: #opponent checks ------------------------------------------------
                if space == 0: # top left corner
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                elif space == 6: #top right corner
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                elif space == 41: # bottom right corner
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                elif space == 35: # bottom left corner
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                elif (space) % 7 == 0: # on the left border
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                elif (space) % 6 == 0: # on the right border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                elif (space + 7) > 42: # on the bottom border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                elif (space - 7) < 0: # on the top border
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
                else:
                    if board.board[space - 1] == 2: # check left
                        h += -2
                    if board.board[space + 1] == 2: # check right
                        h += -2
                    if board.board[space + 7] == 2: # check above
                        h += -2
                    if board.board[space - 1] == 2: # check below
                        h += -2
                    if board.board[space - 1 - 7] == 2: # check top left
                        h += -2
                    if board.board[space + 1 - 7] == 2: # check top right
                        h += -2
                    if board.board[space + 1 + 7] == 2: # check bottom right
                        h += -2
                    if board.board[space - 1 + 7] == 2: # check bottom left
                        h += -2
        return h

    def heuristic3(self, board):
        move = board.recent_move
        player = board.turn
        h = 0
        if player == 1:
            opp = 2
            h += board.checkAdjacentSpacesHeuristic(move)
        else:
            opp = 1
            h += board.checkAdjacentSpacesHeuristicEnemy(move)
        row = move[0]
        col = move[1]
        up_right = 0
        check = (row - 1, col + 1) # up-right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the top-right
                up_right += 1
            else:
                streak = False # there is not an opponent to the top-right
            check = (check[0] - 1, check[1] + 1) # moving further up-right
        right = 0
        check = (row, col + 1) # right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the right
                right += 1
            else:
                streak = False # there is not an opponent to the right
            check = (check[0], check[1] + 1) # moving further right
        bottom_right = 0
        check = (row + 1, col + 1) # bottom-right
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom-right
                bottom_right += 1
            else:
                streak = False # there is not an opponent to the bottom-right
            check = (check[0] + 1, check[1] + 1) # moving further bottom-right
        bottom = 0
        check = (row + 1, col) # bottom
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom
                bottom += 1
            else:
                streak = False # there is not an opponent to the bottom
            check = (check[0], check[1] + 1) # moving further bottom
        bottom_left = 0
        check = (row + 1, col - 1) # bottom-left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the bottom-left
                bottom_left += 1
            else:
                streak = False # there is not an opponent to the bottom-left
            check = (check[0] + 1, check[1] - 1) # moving further bottom-left
        left = 0
        check = (row, col - 1) # left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the left
                left += 1
            else:
                streak = False # there is not an opponent to the left
            check = (check[0], check[1] - 1) # moving further left
        up_left = 0
        check = (row - 1, col - 1) # up-left
        streak = True
        while (check[0] >= 0 and check[0] <= 6 and check[1] >= 0 and check[1] <= 7 and streak):
            if board.getSpace(check[0], check[1]) == opp: # there is an opponent to the up-left
                up_left += 1
            else:
                streak = False # there is not an opponent to the up-left
            check = (check[0] - 1, check[1] - 1) # moving further up-left
        h += up_right + right + bottom_right + bottom + bottom_left + left + up_left
        if (up_right + bottom_left >= 3):
            h += 10
        if (right + left >= 3):
            h += 10
        if (bottom_right + up_left >= 3):
            h += 10
        if (up_right == 3 or right == 3 or bottom_right == 3 or bottom == 3 or bottom_left == 3 or left == 3 or up_left == 3):
            h += 10
        return h

    def alphaBeta(self, board, depth, alpha, beta):
        if board.game_over:
            if board.winner == 1:
                return (None, self.P1_WIN_SCORE)
            elif board.winner == 2:
                return (None, self.P2_WIN_SCORE)
            else:
                return (None, self.TIE_SCORE)

        h = self.heuristic3(board)
        if (not board.game_over) and (depth == 0): # reached depth limit
            return (None, h)

        if board.turn == 1:
            is_max = True
            best_value = -math.inf
        elif board.turn == 2:
            is_max = False
            best_value = math.inf

        valid_moves = board.getPossibleMoves()
        for move in valid_moves:
            self.moves_considered += 1

            board.makeMove(move)
            v = self.alphaBeta(board, depth - 1, alpha, beta)[1] # Score
            board.undoMove()
            if is_max:
                best_value = max(best_value, v)
                if best_value == v:
                    best_move = move
                alpha = max(alpha, best_value)
                if alpha >= beta:
                    return (None, best_value)
            elif not is_max:
                best_value = min(best_value, v)
                if best_value == v:
                    best_move = move
                beta = min(beta, best_value)
                if alpha >= beta:
                    return (None, best_value)

        result = (best_move, best_value)
        return result

    def findMove(self, move_history):
        board = Board(move_history)
        move, score = self.alphaBeta(board, self.max_depth, -math.inf, math.inf)
        return move


class PlayerMC(Player):
    label = "Monte Carlo"
    moves_considered = 0
    turn = -1
    # Number of random games to play per possible move
    test_total = 100

    # Algorithm: for each valid move, make the move, then make random moves until game is over. Repeat some number of
    # times for each move, recording each win and loss for that move. Then, pick the move with the best win/loss
    # ratio.

    'Uses the Monte Carlo algorithm to select a move based on random testing and win ratios.'
    def monteCarlo(self, board):

        # Keeping track of wins and losses for each move; resets after each move is made
        wins_per_move = {}
        losses_per_move = {}

        # Plays 'test_number' of test games for each possible move, recording the results in wins_per_move and
        # losses_per_move. The move that is selected is the move with the greatest win/loss ratio
        possible_moves = board.getPossibleMoves()
        for move in possible_moves:
            # Add move to win and loss dictionaries
            wins_per_move[move] = 0
            losses_per_move[move] = 0
            # print("Checking move: " + str(move))
            # Reset board turn to MC player's turn
            board.makeMove(move)
            self.moves_considered += 1
            # Prevents unnecessary looping when a winner is found
            if board.game_over:
                # print("Found winner: " + str(move))
                return move
            test_number = 0
            while test_number < self.test_total:
                moves_in_test = 0
                # Plays games randomly until 'test_total' test games has been played
                while not board.game_over:
                    valid_moves = board.getPossibleMoves()
                    random_move = random.choice(valid_moves)
                    board.makeMove(random_move)
                    self.moves_considered += 1
                    moves_in_test += 1
                # Test game ends, record result
                if board.winner == self.turn:
                    wins_per_move[move] += 1
                elif board.winner != 0:
                    losses_per_move[move] += 1

                # Undo the random moves made, resetting to initial state after first move is made
                for m in range(0, moves_in_test):
                    board.undoMove()
                test_number += 1
                # Upon finishing of tests, undo initial move in order to check next move
                if test_number == self.test_total:
                    board.undoMove()

        # Dictionaries as lists to better access keys and value
        move_list = list(wins_per_move.keys())
        win_list = list(wins_per_move.values())
        loss_list = list(losses_per_move.values())
        win_ratios = []
        # Calculating win ratios
        for wins in win_list:
            losses = loss_list[win_list.index(wins)]
            if losses == 0:
                win_ratios.append(wins)
                continue
            ratio = wins / losses
            win_ratios.append(ratio)
        # Get best ratio and return its corresponding move
        best_ratio = max(win_ratios)
        best_move = move_list[win_ratios.index(best_ratio)]

        # print(self.wins_per_move)
        # print(self.losses_per_move)
        # print(win_ratios)
        # print(best_move)
        return best_move

    'Finds a move using the above Monte Carlo algorithm'
    def findMove(self, move_history):
        board = Board(move_history)
        self.turn = board.turn
        move = self.monteCarlo(board)
        self.current_move = -1
        return move
