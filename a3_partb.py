# Main Author: Techatat Obun 
# Main Reviewer: Di Liu, Le Chanh Tin Luong

# This function duplicates and returns the board. You may find this useful

from a3_parta import evaluate_board
from a1_partd import overflow
from a1_partc import Queue

def copy_board(board):
        current_board = []
        height = len(board)
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board


"""
   This GameTree class represents a game tree for all possible moves from the current state of the board.
   When it is initialized, it creates a root node from the current state of the board.
   It then builds the tree of the possible moves from the root.
   It scores the nodes in a depth first manner.
   It returns the move that leads to the child node with the highest score.    
"""
class GameTree:
    """
        This class represents a node in the game tree.
        It contains the state of the board, the depth of the node, the player who is making the move,
        It also contains the move that leads to this node, the score of the node.
        It has a list of children nodes.
    """
    class Node:
        def __init__(self, board, depth, player, tree_height = 4):
            # deep copy of board so it won't affect the original board
            self.board = copy_board(board)
            self.depth = depth
            self.player = player
            # tree height determines the intelligence of the AI
            self.tree_height = tree_height
            # There could be many children nodes so it is stored in a list
            self.children = []
            self.move = None
            self.score = None

    

    def __init__(self, board, player, tree_height = 4):
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        # create a root node from the current state of board
        self.root = self.Node(self.board, 0, self.player, self.tree_height)
        # once have the root node, build the tree of the possible moves from the root
        self.build_tree(self.root, self.player)
        # after building the tree, score the nodes in a depth first manner
        if self.root is not None:
            self.score_nodes(self.root)



    """
        This function builds the tree of the possible moves from the root.
        It is passed the root node of the tree.
        it will build the tree to a height of tree_height
        use recursion to build the tree
        it return nothing
    """
    def build_tree(self, node, player):
        # or it reaches the terminal state
        the_queue = Queue()
        # base case: if the node reaches the maximum height of the tree, return
        if self.is_terminal(node.board, player) or node.depth == self.tree_height - 1:
            return
        # if the node is not a leaf node, build its children
        # loop through the board to find the empty cell or the cell that corresponds to the player
        for i in range(len(node.board)):
            for j in range(len(node.board[0])):
                #get the current value of the cell
                current_value = node.board[i][j]
                # player one look for empty cell or cell with positive number
                if player == 1:
                    if current_value >= 0:  
                        # deep copy of board so it won't affect the original board
                        new_board = copy_board(node.board)
                        # Make the move on the copied board by placing the player's piece
                        new_board[i][j] = current_value + 1  
                        #perform overflow routine as needed
                        overflow(new_board, the_queue)
                        # create a child node to store all information of the new board
                        child_node = self.Node(new_board, node.depth + 1, player, self.tree_height)
                        # Store the move that leads to this node
                        child_node.move = (i, j)
                        # add the child node to the children list of the parent node  
                        node.children.append(child_node)
                        # Recursively build the tree for the child node but next move will be the opponent's move
                        self.build_tree(child_node, -player)  
                # player two look for empty cell or cell with negative number
                else:
                    # this block of code is the same as the block of code above only different in the sign of the current value
                    if current_value <= 0:
                        new_board = copy_board(node.board)
                        # Make the move on the copied board by placing the player's piece 
                        new_board[i][j] = current_value - 1
                        # perform overflow routine as needed
                        overflow(new_board, the_queue)
                        child_node = self.Node(new_board, node.depth + 1, player, self.tree_height)
                        child_node.move = (i, j)  # Store the move that leads to this node
                        node.children.append(child_node)
                        self.build_tree(child_node, -player) 

                
    
    """
        This function check if the board is in a terminal state
        terminal state: 
            - someone has won
            - all the cells are filled
        It is passed a board
        it return True if the board is in a terminal state
        otherwise, return False
    """
    def is_terminal(self, board, player):
        # check if the board is in a terminal state
        
        # return result from evaluate_board function = 2 meaning someone has won
        # tie game: all the cells are filled
        if (all(board[i][j] != 0 for i in range(len(board)) for j in range(len(board[0]))) \
            # there is a winner
            or all(board[i][j] >= 0 for i in range(len(board)) for j in range(len(board[0])))) \
            or all(board[i][j] <= 0 for i in range(len(board)) for j in range(len(board[0]))):
            return True
        else:
            return False
        

        """
        This function scores the nodes in a depth first manner. 
        It is passed the root node of the tree.
        it return nothing
        """
    def score_nodes(self, node):
        # base case: if the node is a leaf node, use the evaluation function to score it
        if node.children == []:
            # add higher score to the node that is closer to the root
            node.score = evaluate_board(node.board, node.player) * (self.tree_height - node.depth)
            # if the node is on opponent's turn, change the sign of the score
            node.score = -node.score if node.depth % 2 == 0 else node.score
            return 
        # if the node is not a leaf node, score its children
        else:
            for child in node.children:
                self.score_nodes(child)
            # if the node is at an even level, score it as the max of the children's scores
            if node.depth % 2 == 0:
                node.score = max(child.score for child in node.children)
            # if the node is at an odd level, score it as the min of the children's scores
            else:
                node.score = min(child.score for child in node.children)


    """
        This function returns the move that leads to the child node with the highest score.
        It is passed nothing
    """
    def get_move(self):
        # loop through the children of the root node to find the child with the highest score and return the move that leads to that child
        for child in self.root.children:
            if child.score == self.root.score:
                print(f'return the move: ', child.move)
                return child.move
   
    """
        This is a wrapper for the clear_children function.
        It is passed nothing
        it will clear the tree for the garbage collector
        Then it set the root to None
    """
    def clear_tree(self):
        self.clear_children(self.root)
        self.root = None
    
    """
        This function clears the children of a node.
        It is passed a node
        it will clear the children of the node for the garbage collector
    """
    def clear_children(self, node):
        # base case: if the node is a leaf node, return
        if node is None:
            return
        # if the node is not a leaf node, remove all its children
        for child in node.children:
            self.clear_children(child)

        node.children = []
