# Main Author: Le Chanh Tin Luong
# Main Reviewer: Di Liu, Techatat Obun

from a1_partd import overflow 
from a1_partc import Queue

"""
    This function receives two parameters: board and player.
    The board is a 2D grid where 0 represents an empty cell, and non-zero values represent the number of pieces in a cell, 
    with the sign indicating the corresponding player. 
    The player is +1 for player 1, or -1 for player 2.

    This function evaluates the game board for a specific player.
    This function returns a score, with higher scores being better for the corresponding player. 

    The score must meet these criteria:
    - A win for one player is a loss for the other.
    - Winning boards must score higher than any non-winning boards.
    - Losing boards must score lower than any non-losing boards.
    - All winning (or losing) boards must have the same score. 
"""


def evaluate_board(board, player):
    score = 0
    the_queue = Queue()
    # adjust the board after overflow
    overflow(board, the_queue)

    # if the board only contain 0, both player get 0 score
    if all(board[i][j] == 0 for i in range(len(board)) for j in range(len(board[0]))):
        score = 0
    # determine the score for each player
    else:
        # check if the board is only contain positive number if yes, player 1 win and get max score
        if all(board[i][j] >= 0 for i in range(len(board)) for j in range(len(board[0]))):
            score = float('inf') if player == 1 else float('-inf')
            
        # if the board is only contain negative number if yes, player 2 win and get max score
        elif all(board[i][j] <= 0 for i in range(len(board)) for j in range(len(board[0]))):
            score = float('inf') if player == -1 else float('-inf')
            
        # if the board is not contain only positive or negative number both player get 1 score for each of their cell
        # and reduce 1 score for each of opponent's cell
        else:
            for row in board:
                for cell in row:
                    # evaluate the score for player 1 by adding the positive values and subtracting the negative values
                    if player == 1:
                        if cell > 0:
                            score += abs(cell)
                        elif cell < 0:
                            score -= abs(cell)
                    # evaluate the score for player 2 by adding the negative values and subtracting the positive values
                    else:
                        if cell < 0:
                            score += abs(cell)
                        elif cell > 0:
                            score -= abs(cell)
                        
    return score
