# Tic-Tac-Toe Game (Human v/s AI)
# Submitted by :
# Rohan Grover - 102003029
# Divyanshu - 102003028
# 2COE2

# Run this Code in oflline Compiler only as PyGame Library is not supported in Online Compilers 

# Importing all the required libraries
# pip install pygame
import random
import time
import math
import pygame
import numpy as np

# Minimax function is the main AI algorithm used by Computer for finding best Position of 'X' and 'O'
# This function uses Minimax Algorithm along with Alpha-Beta Pruning 
def minimax(board, depth, is_max, n, alpha=-math.inf, beta=math.inf):
    winner = check_win(board)
    if winner:
        return scores[winner]
    if is_max:   # This block find the position of 'X' where maximum score is obtained for Computer
        best_score = -math.inf
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "x"
                    score = minimax(board, depth+1, False, n,         
                                    alpha, beta)+random.randint(-5, 5)
                    board[i][j] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta >= alpha:
                        pass
        return best_score
    else:         # This block find the position of 'O' where minimum score is obtained for User 
        best_score = math.inf
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = "o"
                    score = minimax(board, depth+1, True, n,
                                    alpha, beta)+random.randint(-5, 5)
                    board[i][j] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if alpha >= beta:
                        pass
        return best_score

# best_move function determines the best move for the Computer by calling Minimax function for each possible positon of 'X'
def best_move(board):
    n = len(board)
    best_score = -math.inf
    move = (0, 0)
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                board[i][j] = "x"
                score = minimax(board, 0, False, len(board))
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    board[move[0]][move[1]] = "x"
    return board


# check_win function checks which Player has won or the game has Tied
# It checks for three consecutive 'X' or 'O' in same row, column or diagonal 
def check_win(board):
    n = len(board)
    first = board[0][0]

    diagonal = first != ""
    for i in range(n):
        if board[i][i] != first:
            diagonal = False
            break
    if diagonal:
        return first
    first = board[0][n-1]
    back_diag = first != ""
    for i in range(1, n+1):
        if board[i-1][n-i] != first:
            back_diag = False
            break
    if back_diag:
        return first

    for i in range(n):
        first = board[i][0]
        sideways = first != ""
        for j in range(n):
            if board[i][j] != first:
                sideways = False
        if sideways:
            return first

    for i in range(n):
        first = board[0][i]
        sideways = first != ""
        for j in range(n):
            if board[j][i] != first:
                sideways = False
        if sideways:
            return first

    open_spots = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                open_spots += 1
    if open_spots == 0:
        return "tie"
    return None     # It returns none if the game has not ended yet

def reset(n):   # For reinitializing all variables
    board = [["" for i in range(n)] for j in range(n)]
    loop = True
    return board, loop, None, True

def rect(screen, color, x, y, w, h, fill=0): # for drawing rectangle on Pygame Window
    pygame.draw.rect(screen, color, (x, y, w, h), fill)


def square(screen, color, x, y, s, fill=0): # for drawing square on Pygame Window
    rect(screen, color, x, y, s, s, fill)


def background(screen, color):  # for setting background color of Pygame Window
    rect(screen, color, 0, 0, WIDTH, HEIGHT)

def print_message(T, screen, f):  # For printing message on Tic Tac Toe Window
    padding=10
    rect(screen, (153, 255, 204), padding, 470 - padding, WIDTH-padding*2, 80)
    rect(screen, (0, 0, 0), padding, 470 - padding, WIDTH-padding*2, 80, 3)
    black = (0, 0, 0)
    font = pygame.font.Font('Target.otf', f)
    text = font.render(T, True, black)
    textRect = text.get_rect()
    textRect.center = (235, 500)
    screen.blit(text, textRect)


scores = {
    "x": 10,            # Positive Score is best score for Computer
    "o": -10,           # Negative Score is best score for User
    "tie": 0
}

pygame.init() # Initializing the Pygame Environment

SIZE = 470, 550     # Dimensions of Pygame Window 
WIDTH, HEIGHT = 470, 470        # Dimensions of Square Board where Tiles have been placed

def main():
    # Space between pygame window and Tic Tac Toe Play Area
    padding = 10
    # Size of Tic Tac Toe Board
    n = 3  
    # Size of one Square Block
    s = (WIDTH-padding*2)//n   

    # Initializing an Empty Board
    board = [["" for i in range(n)] for j in range(n)]

    # Computer(X) will always start the game
    turn = "x"

    # Loading and Transforming X and O Images
    x_image = pygame.image.load(r"x.png")
    x_image = pygame.transform.scale(x_image, (s, s))
    o_image = pygame.image.load(r"o.png")
    o_image = pygame.transform.scale(o_image, (s, s))

    # Initializing loop as True which will change to False when one Game ends
    loop = True

    human_played = False
    winner = False
    restarted = False

    # Initializing running as True which will change to False when User exits from the Game
    running = True

    # best_move function called to Determine The Best Move for the Computer
    board = best_move(board)    
    
    # To pass the turn to next player
    turn = "x" if turn == "o" else "o"

    # Start the screen
    screen = pygame.display.set_mode(SIZE)  

    # Setting the Title of Game Window
    pygame.display.set_caption('TIC TAC TOE')

    while running:
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # The user closed the window
                running = False  # Stop running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board, loop, winner, restarted = reset(n) # reinitialize all the variables

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Mapping between board variable and actual Game window when user clicks on certain tile with mouse
                j = int(Mouse_x//s)
                i = int(Mouse_y//s)    
                if i < n and j < n:
                    # If it is User's turn and the tile clicked by User is empty then fill it with 'O'
                    if board[i][j] == "":
                        board[i][j] = turn
                        turn = "x" if turn == "o" else "o"

                        # If User has clicked on the empty tile when it was his turn change this variable to True
                        human_played = True

                    # check_win is called to check if one of the Player has won or the Game has tied
                    winner = check_win(board)

        if loop:
            rect(screen, (153, 255, 204), padding,padding, WIDTH-padding*2, 550-padding*2)
            # Logic goes here
            if not winner:
                # check_win is called to check if one of the Player has won or the Game has tied
                winner = check_win(board)
            if winner:
                # For printing the message on screen when the game ends
                if winner == "tie":
                    winner = 'Tie'
                    T = winner+"!"
                    print(T)
                    print_message(str(T), screen, 40)
                else:
                    if(winner.upper() == 'X'):
                        winner = 'X '
                    else:
                        winner = 'O '
                    T = winner+" Wins!"
                    print(T)
                    print_message(str(T), screen, 40)
                # User can press 'r' to restart the game
                print("Press 'r' to restart")
                loop = False

            # To Update the Pygame Window w.r.t board matrix with the 'X' and 'O' images
            for i in range(n):
                for j in range(n):
                    item = board[i][j]
                    if item == "x":
                        screen.blit(x_image, (j*s+padding, i*s+padding))
                    elif item == "o":
                        screen.blit(o_image, (j*s+padding, i*s+padding))
                    square(screen, (0, 0, 0), j*s+padding, i*s+padding, s, 3)
            rect(screen, (0, 0, 0), padding, 470 - padding, WIDTH-padding*2, 80, 3)
            if not winner:
                print_message('TIC TAC TOE', screen, 40)
            pygame.display.update()

            # If 'r' is pressed by User start the Game again
            if restarted:
                turn = "x"
                board = best_move(board)
                turn = "x" if turn == "o" else "o"
                restarted = False

            # If User has played his turn , Computer will decide its best move and play
            if human_played:
                time.sleep(.5)
                board = best_move(board)
                turn = "x" if turn == "o" else "o"
                human_played = False
    pygame.quit()  # Close the window


if __name__ == "__main__":
    main()