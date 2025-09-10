import pygame
pygame.init()
pygame.mixer.init()
from boardBackground import Board
move_sound = pygame.mixer.Sound("move-self.mp3")
capture_sound = pygame.mixer.Sound("capture.mp3")
class Moving1(Board):
    def __init__(self, screen, width, height, rows, cols, square_size, board_pos):
        super().__init__(screen, width, height, rows, cols, square_size, board_pos)
        self.selectlist = []
        self.yxlist = []
        self.select = False
        self.capturedpieces = []
        self.move = False
        self.turn = "white"

    def piece_xy(self, mouse):
        self.mouse = mouse
        self.mousex = mouse[0]
        self.mousey = mouse[1]
        self.col = self.mousex // self.square_size
        self.row = self.mousey // self.square_size
        self.xy = self.row, self.col
    
    def piece_selection(self):
        if self.row < 8 and self.col < 8:
            self.piece = self.board_pos[self.row][self.col] #piece on board where mouse clicked
        else:
            return self.yxlist, self.selectlist
        self.move = False
        if len(self.selectlist) >= 2: #selectlist is always two
            self.selectlist.clear() #clears if greater than two
            self.yxlist.clear()
        self.selectlist.append(self.piece) #appending piece to list
        self.yxlist.append(self.xy)
        return self.yxlist, self.selectlist
    
    def sideturn(self, validmove):
        self.move = False
        self.validmove = validmove
        self.turn = getattr(self, "turn", "white")
        if validmove == True:
            if len(self.selectlist) == 2:
                self.firstitem = self.selectlist[0]
                if self.turn == "white" and self.firstitem[0] == "w":
                    self.move = True
                    self.turn = "black"
                elif self.turn == "black" and self.firstitem[0] == "b":
                    self.move = True
                    self.turn = "white"
                else:
                    self.move = False
        return self.turn, self.move
    
    def movepos(self, validmove):
        self.validmove = validmove
        if len(self.selectlist) == 2 and self.validmove == True:
            self.y1, self.x1 = self.yxlist[0]
            self.y2, self.x2 = self.yxlist[1]
            #if enpassant move
            #if spot is empty and piecemoved was a pawn
            if self.board_pos[self.y2][self.x2] == "__" and self.board_pos[self.y1][self.x1][1] == "P":
                #if piece beside was a enemy pawn
                if self.y2 != 7 and self.board_pos[self.y2+1][self.x2] == "bP":
                    self.capturedpieces.append(self.board_pos[self.y2+1][self.x2])
                    capture_sound.play()
                    self.board_pos[self.y2+1][self.x2] = "__" #piece eliminataed
                elif self.y2 != 0 and self.board_pos[self.y2-1][self.x2] == "wP":
                    self.capturedpieces.append(self.board_pos[self.y2-1][self.x2])
                    capture_sound.play()
                    self.board_pos[self.y2-1][self.x2] = "__"
            #castling moves for king
            #if piece is king
            if self.board_pos[self.y1][self.x1] == "wK":
                # if its moved two squares right
                if (self.y2, self.x2) == (7, 6):
                    self.board_pos[7][5] = self.board_pos[7][7] #now king
                    self.board_pos[7][7] = "__" #7,7 is now empty
                if (self.y2, self.x2) == (7, 2):
                    self.board_pos[7][3] = self.board_pos[7][0]
                    self.board_pos[7][0] = "__"
            if self.board_pos[self.y1][self.x1] == "bK":
                if (self.y2, self.x2) == (0, 6):
                    self.board_pos[0][5] = self.board_pos[0][7]
                    self.board_pos[0][7] = "__"
                if (self.y2, self.x2) == (0, 2):
                    self.board_pos[0][3] = self.board_pos[0][0]
                    self.board_pos[0][0] = "__"
            
            if self.board_pos[self.y2][self.x2] != "__":
                self.capturedpieces.append(self.board_pos[self.y2][self.x2])
                capture_sound.play()
            if self.board_pos[self.y2][self.x2] == "__":
                move_sound.play()
            #move piece to x2, y2
            self.board_pos[self.y2][self.x2] = self.board_pos[self.y1][self.x1]
            #x1, y1 is now empty
            self.board_pos[self.y1][self.x1] = "__"
            
            
            return self.board_pos
        
    def co_ords(self):
        if len(self.selectlist) == 2:
            self.y1, self.x1 = self.yxlist[0]
            self.y2, self.x2 = self.yxlist[1]
            return self.y1, self.x1, self.y2, self.x2
        else:
            return -1, -1, -1, -1

    def piece_name(self):
        if len(self.selectlist) == 2:
            self.pieceone = self.selectlist[0]
            self.piecetwo = self.selectlist[1]
            return self.pieceone, self.piecetwo
        else: return None, None
        
        

