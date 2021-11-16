import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROWS = 6
COLUMNS = 7


def create_board():
    square = np.zeros((ROWS, COLUMNS))
    return square


def drop_ball(boards, rows, cols, ball):
    boards[rows][cols] = ball


def valid_drop(boards, cols):
    return boards[ROWS - 1][cols] == 0


def open_row(boards, cols):
    for r in range(ROWS):
        if boards[r][cols] == 0:
            return r


def flip_board(boards):
    print(np.flip(boards, 0))


def win_move(boards, ball):
    # checking horizontal for wins
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if boards[r][c] == ball and boards[r][c + 1] == ball and boards[r][c + 2] == ball and boards[r][c + 3] == ball:
                return True

    # checking for vertical wins
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if boards[r][c] == ball and boards[r + 1][c] == ball and boards[r + 2][c] == ball and boards[r + 3][c] == ball:
                return True

    # checking for positive slope diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if boards[r][c] == ball and boards[r + 1][c + 1] == ball and boards[r + 2][c + 2] == ball and boards[r + 3][c + 3] == ball:
                return True

    # checking for negative
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if boards[r][c] == ball and boards[r - 1][c + 1] == ball and boards[r - 2][c + 2] == ball and boards[r - 3][c + 3] == ball:
                return True


def draw_board(boards):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * BOARD, r * BOARD + BOARD, BOARD, BOARD))
            pygame.draw.circle(screen, BLACK, (int(c * BOARD + BOARD / 2), int(r * BOARD + BOARD + BOARD / 2)), RADIUS)

        for a in range(COLUMNS):
            for b in range(ROWS):
                if boards[b][a] == 1:
                    pygame.draw.circle(screen, RED, (int(a * BOARD + BOARD / 2), height - int(b * BOARD + BOARD / 2)), RADIUS)

                elif boards[b][a] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(a * BOARD + BOARD / 2), height - int(b * BOARD + BOARD / 2)), RADIUS)

    pygame.display.update()


board = create_board()

game_over = False
turn = 0

pygame.init()

BOARD = 100

width = COLUMNS * BOARD
height = (ROWS + 1) * BOARD

size = (width, height)

RADIUS = int(BOARD / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
flip_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, BOARD))
            pos = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos, int(BOARD / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos, int(BOARD / 2)), RADIUS)

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ask for player 1 input
            if turn == 0:
                pos = event.pos[0]
                col = int(math.floor(pos / BOARD))
                if valid_drop(board, col):
                    row = open_row(board, col)
                    drop_ball(board, row, col, 1)

                    if win_move(board, 1):
                        print("Player 1 Wins. Congrats!!")
                        game_over = True

                        # Ask for player 2 input
            else:
                pos = event.pos[0]
                col = int(math.floor(pos / BOARD))
                if valid_drop(board, col):
                    row = open_row(board, col)
                    drop_ball(board, row, col, 2)

                    if win_move(board, 2):
                        print("Player 2 Wins. Congrats!!")
                        game_over = True

            flip_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
