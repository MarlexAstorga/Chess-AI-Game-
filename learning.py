import pygame
from boardBackground import Board
class learningChess(Board):
    def __init__(self, screen, width, height, rows, cols, square_size, board_pos):
        super().__init__(screen, width, height, rows, cols, square_size, board_pos)
        self.screen = screen
        self.pieces = {}
    
    def movepiece(self, move):
        start_pos, end_pos = move
        #moves piece
        self.board_pos[end_pos[0]][end_pos[1]] = self.board_pos[start_pos[0]][start_pos[1]]
        self.board_pos[start_pos[0]][start_pos[1]] = "__"
        if start_pos == (3 ,5):
            self.board_pos[3][4] = "__"
        return self.board_pos

    
    

    