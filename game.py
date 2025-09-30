#   Author: Catherine Leung
#   This is the game that you will code the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

#   Main Author(s): Di Liu
#   Main Reviewer(s): Techatat Obun, Le Chanh Tin Luong

import pygame
import sys
import math

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Board:
    def __init__(self,width,height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0
        # To track the history of the board for undo functionality
        self.history = []
        # To track the state of undo function ( only enable after a move then if make a move, disable)
        self.undo_enabled = False

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row,col,player):
        if row >= 0  and row < self.height and col >= 0 and col < self.width and (self.board[row][col]==0 or self.board[row][col]/abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            # Saves the current state of the board to the history
            self.history.append([row[:] for row in self.board])
            # Then makes the move
            self.board[row][col] += player
            self.turn += 1
            # Updates the attribute to True
            self.undo_enabled = True
            return True
        return False

    """
    The following function is to perform an undo functionality.
    When the button is clicked, the event reverts the game board to a state before that human player's last move 
    """
    def undo(self):

        # If the board has some moves:
        if self.history:
            
            # Reverts the board to the last saved state
            self.board = self.history.pop()
            # Decrements the turn counter
            if self.turn > 0:
                self.turn -= 1
                
            # Disables after one undo
            self.undo_enabled = False
            
    def check_win(self):
        if(self.turn > 0):
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if(self.board[i][j] > 0):
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif(self.board[i][j] < 0):
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if(num_p1 == 0):
                return -1
            if(num_p2== 0):
                return 1
        return 0

    def do_overflow(self,q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if(numsteps != 0):
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE+Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = p1_sprites
                    else:
                        sprite = p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

"""
The following Button class is to draw the button on the winder, and perform a button functionality.
"""
class Button:
    """
    The constructor is to define the basic information of a button.
    The constructor initializes the Button with position (x, y), dimensions (width, height), and a label.
    """
    def __init__(self, x, y, width, height, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

    """
    This function is to draw a button on the screen.
    """
    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, 1, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    """
    This function handles mouse button down events on the button, triggering a board undo functionality if the button is clicked.
    """
    def handle_event(self, event, board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # If the button is clicked, calls the undo() function and reverts the board to the last step before human's last move
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                board.undo()

    """
    This function checks if the given position (mouse coordinates) is over the button.
    """
    def is_over(self, pos):
        
        # pos is the mouse position of a tuple of (x, y) coordinates
        # If the mouse's coordinates are in the boundaries of the button, returns True; otherwise, returns False
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    """
    This functions checks if a mouse button down event occurs within the button boundaries.
    """
    def is_clicked(self, event):
        
        # Checks if a mouse button down event has occurred
        if event.type == pygame.MOUSEBUTTONDOWN:  

            # Gets the position of the mouse at the time of the click
            # If the mouse's position is within the button's boundaries, returns True; otherwise, returns False
            x, y = event.pos  
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                return True
        return False

# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5
# Define a custom event for the turn change
CHANGE_TURN_EVENT = pygame.USEREVENT + 1

# hate the colours?  there are other options.  Just change the lines below to another colour's file name.  
# the following are available blue, pink, yellow, orange, grey, green
p1spritesheet = pygame.image.load('blue.png')
p2spritesheet = pygame.image.load('pink.png')
p1_sprites = []
p2_sprites = []


player_id = [1 , -1]


for i in range(8):
    curr_sprite = pygame.Rect(32*i,0,32,32)
    p1_sprites.append(p1spritesheet.subsurface(curr_sprite))
    p2_sprites.append(p2spritesheet.subsurface(curr_sprite))    


frame = 0

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200,800))

pygame.font.init()
font = pygame.font.Font(None, 36)  # Change the size as needed
bigfont = pygame.font.Font(None, 108)
# Create the game board
# board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])
# TO DO: crete a level of intelligence of the bot
status=["",""]
current_player = 0
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
# Game loop
running = True
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

# Creates an instance of Button for the undo button
undo_button = Button(900, 180, 200, 50, 'Undo')
is_make_move = False


while running:
    
    # Resets is_make_move flag
    is_make_move = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)
            player2_dropdown.handle_event(event)
            choice[0] = player1_dropdown.get_choice()
            choice[1] = player2_dropdown.get_choice()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET    
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE
                
                # Handles undo button event only if the current player is a human
                if undo_button.is_over((x, y)) and choice[current_player] == 0 and board.turn > 0 and board.undo_enabled:

                    # Checks if the mouse is over the undo button, the current player's choice is 0,
                    # the game has progressed beyond the initial turn, and undo is enabled on the board.
                    undo_button.handle_event(event, board)

                    # If the conditions are met, the handle the event (undo operation is triggered) for the undo button.
                    # Converts the current player to the other player
                    if choice[current_player] == 0:

                        # If current player's choice is 0 and the other player's choice is not 0, keep the current player unchanged
                        if choice[(current_player + 1) % 2] != 0:
                            current_player = current_player
                        else:
                            # If the other player's choice is also 0, switch to the other player
                            current_player = (current_player + 1) % 2
                    else:
                        # If the current player's choice is not 0, switch to the other player
                        current_player = (current_player + 1) % 2

            # Checks if the turn change event has occurred
            if event.type == CHANGE_TURN_EVENT:  
                # Changes the turn to the AI
                current_player = (current_player + 1) % 2
                # Stops the timer
                pygame.time.set_timer(CHANGE_TURN_EVENT, 0)
                   
    win = board.check_win()
    if win != 0:
        winner = 1
        if win == -1:
            winner = 2
        has_winner = True

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if repeat_step == FULL_DELAY:
                    next = overflow_boards.dequeue()
                    board.set(next)
                    repeat_step = 0
                else:
                    repeat_step += 1
            else:
                overflowing = False

                # goes between 0 and 1
                current_player = (current_player + 1) % 2

        else:
            status[0] = "Player " + str(current_player + 1) + "'s turn"
            make_move = False
            if choice[current_player] == 1:
                (grid_row,grid_col) = bots[current_player].get_play(board.get_board())
                status[1] = "Bot chose row {}, col {}".format(grid_row, grid_col)
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                       has_winner = True
                       # if p1 makes an invalid move, p2 wins.  if p2 makes an invalid move p1 wins
                       winner = ((current_player + 1) % 2) + 1 
                else:
                    make_move = True
            else:
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True
                    
            # Checks if the current player is Human
            if choice[current_player] == 0:
                # Checks if AI playing against Human
                if choice[current_player] != choice[(current_player + 1) % 2]:
                    if make_move:
                        board.add_piece(grid_row, grid_col, player_id[current_player])
                        numsteps = board.do_overflow(overflow_boards)
                        if numsteps != 0:
                            overflowing = True
                            repeat_step = 0
                        else:
                            # Sets a timer event to occur after 5 seconds
                            pygame.time.set_timer(CHANGE_TURN_EVENT, 5000)
                        grid_row = -1
                        grid_col = -1  
                        # Sets a flag that human player has made a move
                        is_make_move = True  


                else: 
                    if make_move:
                        board.add_piece(grid_row, grid_col, player_id[current_player])
                        numsteps = board.do_overflow(overflow_boards)
                        if numsteps != 0:
                            overflowing = True
                            repeat_step = 0
                        else:
                            current_player = (current_player + 1) % 2
                        grid_row = -1
                        grid_col = -1  

            else: 
                if make_move:
                    board.add_piece(grid_row, grid_col, player_id[current_player])
                    numsteps = board.do_overflow(overflow_boards)
                    if numsteps != 0:
                        overflowing = True
                        repeat_step = 0
                    else:
                        current_player = (current_player + 1) % 2
                    grid_row = -1
                    grid_col = -1  

    # Draw the game board
    window.fill(WHITE)
    board.draw(window,frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    
    # Draws the undo button on the screen if the current player is human:
    if choice[current_player] == 0:
        undo_button.draw(window)  
        
    # Draws the next button only if the player is not the same type
    if choice[current_player] != choice[(current_player + 1) % 2]:
        if choice[current_player] == 0:
            # Render the countdown as text and blit it to the screen
            countdown_text = font.render("You have 5 seconds to Undo after making a move", True, (0, 0, 0))
            window.blit(countdown_text, (20, 50))  # Adjust the position as needed
    if not has_winner:  
        text = font.render(status[0], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET, 750 ))
        text = font.render(status[1], True, (0, 0, 0))  # Black color
        window.blit(text, (X_OFFSET,  700 ))
    else:
        text = bigfont.render("Player " + str(winner)  + " wins!", True, (0, 0, 0))  # Black color
        window.blit(text, (300, 250))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
