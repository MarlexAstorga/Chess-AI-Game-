import pygame
pygame.init()
from valid import ValidMoves
class CheckingMoves(ValidMoves):
    def __init__(self, x1, y1, x2, y2, pieceone, piecetwo, board_pos, yxlist, validcastlesides, turn):
        super().__init__(board_pos)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.yxlist = yxlist
        self.pieceone = pieceone
        self.piecetwo = piecetwo
        self.turn = turn
        self.validcastlesides = validcastlesides
        #validlist, list of valid moves, false, false, false... if one is true then theres a valid move
        self.validlist = [self.checking_horse(), 
                          self.checking_bishop(), 
                          self.checking_rook(),
                          self.checking_pawn(),
                          self.checking_king(),
                          self.checking_queen(),
                        ]
        
        

    def checking_horse(self):
        #initally set false
        self.hmove = False
        #if x1, y1 are not empty
        if self.x1 != None and self.y1 != None:
            #if pieceone is a piece
            if self.pieceone != None:
                #if piece clicked is a horse
                if self.pieceone[1] == "H":
                    #if piece moved to is a valid move calculated from the valid horse moves
                    if (self.y2, self.x2) in self.horse_valid(self.y1, self.x1, self.pieceone):
                        self.hmove = True #move is valid
        else: self.hmove = False #else move is false
        return self.hmove
    
    #similarily the same for every other piece, bishop, rook, pawn, king

    def checking_bishop(self):
        self.bmove = False
        if self.x1 != None and self.y1 != None:
            if self.pieceone != None:
                if self.pieceone[1] == "B":
                    if (self.y2, self.x2) in self.bishop_valid(self.y1, self.x1, self.pieceone):
                        self.bmove = True
        else: self.bmove = False
        return self.bmove

    def checking_rook(self):
        self.rmove = False
        if self.x1 != None and self.y1 != None:
            if self.pieceone != None:
                if self.pieceone[1] == "R":
                    if (self.y2, self.x2) in self.rook_valid(self.y1, self.x1, self.pieceone):
                        self.rmove = True
        else: self.rmove = False
        return self.rmove

    def checking_pawn(self):
        self.pmove = False
        if self.x1 != None and self.y1 != None:
            if self.pieceone != None:
                if self.pieceone[1] == "P":
                    if (self.y2, self.x2) in self.pawn_valid(self.y1, self.x1, self.pieceone):
                        
                        self.pmove = True
        else: self.pmove = False
        return self.pmove

    def checking_king(self):
        self.kmove = False
        if self.x1 != None and self.y1 != None:
            if self.pieceone != None:
                if self.pieceone[1] == "K":
                    #passes in validcastle sides aswell, to append castling moves
                    if (self.y2, self.x2) in self.king_valid(self.y1, self.x1, self.pieceone, self.validcastlesides, self.turn):
                        self.kmove = True
        else: self.kmove = False
        return self.kmove

    def checking_queen(self):
        self.qmove = False
        if self.x1 != None and self.y1 != None:
            if self.pieceone != None:
                if self.pieceone[1] == "Q":
                    if (self.y2, self.x2) in self.queen_valid(self.y1, self.x1, self.pieceone):
                        self.qmove = True
        else: self.qmove = False
        return self.qmove


