import numpy as np
import pygame
import sys
import math

COLUMNS = 7
ROWS = 7
WINNING_NUMBER = 3 #WINNNG_NUMBER +1 is the number of pieces you need to connect
BOX = 100
RADIUS = int(BOX / 2) -5


def check_place(board,player_sel, counter,ROWS):
    if board[ROWS-counter][player_sel] == 0:
        return True
    else:
        False

def check_winner(matrix_A,ver_hor= True):
    
    winner = False
    count_horizontal = 0
    count_vertical = 0
    count_right_diagonal_DOWN = 0
    count_right_diagonal_RIGHT = 0
    count_left_diagonal_DOWN = 0
    count_left_diagonal_RIGHT = 0

    copy_matrix_A = np.empty_like(matrix_A)
    copy_matrix_A[:] = matrix_A

    for i in range(matrix_A.shape[0]// 2):
        copy_matrix_A[[i,-i-1],:] = copy_matrix_A[[-i-1,i],:]
    
    for r in range(ROWS):
        
        if ver_hor:
            n = 0
        else:
            n = r
        
        for c in range(COLUMNS-1-n):
        
            if ver_hor:

                horizontal_matched = False
                vertical_matched = False

                if count_vertical == WINNING_NUMBER or count_horizontal == WINNING_NUMBER:
                        winner = True
                        break
                if matrix_A[r][c] == matrix_A[r][c+1] != 0:
                    #print("good horizontal")
                    count_horizontal += 1
                    horizontal_matched = True

                if matrix_A[c][r] == matrix_A[c+1][r] != 0:
                    #print("good vertical")
                    count_vertical += 1
                    vertical_matched = True

                #------------------------------------------
                if not horizontal_matched:
                    #print("bad horizontal")
                    count_horizontal = 0
                if not vertical_matched:
                    #print("bad vertical")
                    count_vertical = 0
            else:

                left_diagonal_matched_DOWN = False
                left_diagonal_matched_RIGHT = False
                right_diagonal_matched_DOWN = False
                right_diagonal_matched_RIGHT = False

                if count_right_diagonal_DOWN == WINNING_NUMBER or count_right_diagonal_RIGHT == WINNING_NUMBER or count_left_diagonal_DOWN == WINNING_NUMBER or count_left_diagonal_RIGHT == WINNING_NUMBER:
                        winner = True
                        break

                if matrix_A[c+r][c] == matrix_A[r+c+1][c+1] !=0:
                    #print("good right diagonal DOWN")
                    count_right_diagonal_DOWN += 1
                    right_diagonal_matched_DOWN = True

                if matrix_A[c][c+r] == matrix_A[c+1][r+c+1] !=0:
                    #print("good right diagonal RIGHT")
                    count_right_diagonal_RIGHT += 1
                    right_diagonal_matched_RIGHT = True
                
                if copy_matrix_A[c+r][c] == copy_matrix_A[r+c+1][c+1] != 0:
                    #print("Good Left Diagonal DOWN")
                    count_left_diagonal_DOWN += 1
                    left_diagonal_matched_DOWN = True

                if copy_matrix_A[c][c+r] == copy_matrix_A[c+1][r+c+1] != 0:
                    #print("Good Left Diagonal RIGHT")
                    count_left_diagonal_RIGHT +=1
                    left_diagonal_matched_RIGHT = True
                

                # ---------------------------------------------
                if not right_diagonal_matched_DOWN:
                    #print("bad right diagonal DOWN")
                    count_right_diagonal_DOWN = 0
                
                if not right_diagonal_matched_RIGHT:
                    #print("bad right diagonal RIGHT")
                    count_right_diagonal_RIGHT = 0

                if not left_diagonal_matched_DOWN:
                    #print("bad left diagonal DOWN")
                    count_left_diagonal_DOWN = 0

                if not left_diagonal_matched_RIGHT:
                    #print("bad left diagonal RIGHT")
                    count_left_diagonal_RIGHT = 0

        if count_right_diagonal_DOWN == WINNING_NUMBER or count_right_diagonal_RIGHT == WINNING_NUMBER or count_left_diagonal_DOWN == WINNING_NUMBER or count_left_diagonal_RIGHT == WINNING_NUMBER or count_vertical == WINNING_NUMBER or count_horizontal == WINNING_NUMBER:
            winner = True
            break                       
    """
    if ver_hor:
        print("The horizontal count is: ",count_horizontal)
        print("The vertical count is: ",count_vertical)
    else:
        print("The right Diagonal DOWN count is: ",count_right_diagonal_DOWN)
        print("The right Diagonal RIGHT count is: ",count_right_diagonal_RIGHT)
        print("The left Diagonal DOWN count is: ",count_left_diagonal_DOWN)
        print("The left Diagonal RIGHT count is: ",count_left_diagonal_RIGHT)
    """
    return winner

def execute_game(turns,board,player_selection):
    game_over = False
    flag_succesful_drop = False
    while(True):
        #player_selection = int(input("Player {} please choice a column(0-{}): ".format(turns+1,COLUMNS-1))) #for console input
        if (player_selection>=0 and player_selection<=COLUMNS-1):
            break
        
    for i in range(ROWS):
        if check_place(board,player_selection,i+1,ROWS):
            board[ROWS-i-1][player_selection] = turns +1
            flag_succesful_drop = True
            if check_winner(board,ver_hor=True) or check_winner(board,ver_hor=False):
                print("Player {} WON!!!".format(turns+1))
                game_over = True
            break
    if not flag_succesful_drop:
        print("Column is full")
    else:
        turns += 1
    
    return game_over,turns

def draw_board(screen,board,turns,xpos):
    
    pygame.draw.rect(screen,(0,0,0),(0,0,COLUMNS*BOX,BOX))
    if turns == 0:
        pygame.draw.circle(screen,(255,0,0),(xpos,BOX/2),RADIUS)
    else:
        pygame.draw.circle(screen,(0,255,0),(xpos,BOX/2),RADIUS)
    
    pygame.draw.rect(screen,(0,0,255),(0,BOX,COLUMNS*BOX,ROWS*BOX))

    for r in range(1,ROWS+1):
        for c in range(COLUMNS):
            if board[r-1][c] == 0: 
                pygame.draw.circle(screen,(0,0,0),(c*BOX + BOX/2, r*BOX + BOX/2),RADIUS)
            elif board[r-1][c] == 1:
                pygame.draw.circle(screen,(255,0,0),(c*BOX + BOX/2, r*BOX + BOX/2),RADIUS)
            else:
                pygame.draw.circle(screen,(0,255,0),(c*BOX + BOX/2, r*BOX + BOX/2),RADIUS)

    pygame.display.update()

if __name__ == "__main__":
    
    pygame.init()
    
    width = BOX * COLUMNS
    height = BOX * ROWS + BOX
    turns = 0

    board = np.zeros((ROWS,COLUMNS))
    print(board)

    screen = pygame.display.set_mode((width,height))
    draw_board(screen,board,turns,2*width)
    pygame.display.update()

    font_obj = pygame.font.SysFont("monospace",int(math.floor(width/17.5)))

    game_over = False
    
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                xpos = event.pos[0]
                pygame.draw.rect(screen,(0,0,0),(0,0,COLUMNS*BOX,BOX))
                if turns == 0:
                    pygame.draw.circle(screen,(255,0,0),(xpos,BOX/2),RADIUS)
                else:
                    pygame.draw.circle(screen,(0,255,0),(xpos,BOX/2),RADIUS)

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player_selection = event.pos[0] // 100
                #Turn of Player 1
                if turns == 0:
                    game_over, turns = execute_game(turns,board,player_selection)
                    
                #Turn of Player 2
                elif turns == 1:
                    game_over, turns= execute_game(turns,board,player_selection)
                    
                #print(board)
                if not game_over: turns = turns %2
                xpos = event.pos[0]
                draw_board(screen,board,turns,xpos)

        if game_over:
            pygame.draw.rect(screen,(0,0,0),(0,0,COLUMNS*BOX,BOX))
            if turns == 1:
                label = font_obj.render("Player {} kicked your ass!!".format(turns),1,(255,0,0))
            else:
                label = font_obj.render("Player {} kicked your ass!!".format(turns),1,(0,255,0))
            screen.blit(label,(35,30))
            pygame.display.update()
            pygame.time.delay(4000)
