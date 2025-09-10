import pygame
pygame.init()
#board

class Board:
    def __init__(self, screen, width, height, rows, cols, square_size, board_pos):
        self.screen = screen
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.board_pos = board_pos
        self.pieces = {}


    def background(self, screen):
        screen.fill("light blue")
        for row in range(self.rows):
            for col in range(self.cols):
                color = "white" if (row + col) % 2 == 0 else "green"
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def load_image(self, img_file, name):
        self.image = pygame.image.load(img_file).convert_alpha()
        self.name = name
        self.pieces.update({name:self.image})

    def check(self):
        if "bR" in self.pieces:
            return True
        else:
            return False

    def print_images(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                self.piece = self.board_pos[row][col]
                if self.piece != "__":
                    screen.blit(self.pieces[self.piece], (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
 