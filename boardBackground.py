import pygame
pygame.init()
#board

class Board:
    def __init__(self, screen, width, height, rows, cols, square_size, board_pos):
        #properties of class, used to calculate board, images, surfaces
        self.screen = screen
        self.width = width #window width
        self.height = height #window height
        self.rows = rows # 8
        self.cols = cols #8
        self.square_size = square_size
        self.board_pos = board_pos
        self.pieces = {}


    def background(self, screen):
        screen.fill("light blue") #background
        for row in range(self.rows):
            for col in range(self.cols):
                color = "white" if (row + col) % 2 == 0 else "green" #even or odd 
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size)) 
                #position and size

    def load_image(self, img_file, name):
        self.image = pygame.image.load(img_file).convert_alpha() #loading image file
        self.name = name
        self.pieces.update({name:self.image}) #adds image to dictionary with piece name

    def check(self):
        if "bR" in self.pieces:
            return True
        else:
            return False

    def print_images(self, screen):
        for row in range(self.rows): #8
            for col in range(self.cols): #8
                self.piece = self.board_pos[row][col] #piece on board
                if self.piece != "__": #piece is not empty
                    screen.blit(self.pieces[self.piece], (col * self.square_size, row * self.square_size)) 
                    # printing piece image on board
 
    def printing_validMoves(self, piecemoves, screen):
        radius = 15
        colourOppacity = (50, 50, 50, 128)  # 50, 50, 50 grey, 128 opacity
        
        #surface
        circle_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        for move in piecemoves:
            row, col = move
            circle_surface.fill((0, 0, 0, 0)) #clears
            pygame.draw.circle(circle_surface, colourOppacity, (self.square_size // 2, self.square_size // 2), radius) #circle
            screen.blit(circle_surface, (col * self.square_size, row * self.square_size)) #prints on squares

    def print_capturedPieces(self, capturedpieces, screen): 
        whitex = 590 #base coordinates
        blackx = 590
        whitey = 100
        blacky = 200

        for piece in capturedpieces: #each piece in caputured piece
            if piece[0] == "w": #for white
                screen.blit(self.pieces[piece], (whitex, whitey)) #prints captured piece on screen
                whitex += 25 #adds 25x for next piece on the right
                if whitex > 780: #if fills up row
                    whitex = 590 #resets the x coordinate
                    whitey += 50  #moves y up for new row
            elif piece[0] == "b": #black
                screen.blit(self.pieces[piece], (blackx, blacky))
                blackx += 25
                if blackx > 780:
                    blackx = 590
                    blacky += 50  # moves from 200 → 250


