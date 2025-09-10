import pygame
pygame.init()
from check import ChessRules
#check = false
#squares between empty x+1 == "__"
#squares are not attacked
#get opposite turn, generate attack moves
#if y1, x+1 in between squares, not valid
#squares have not moved at all
class Castling(ChessRules):
    def __init__(self, board_pos, turn):
        self.board_pos = board_pos
        self.turn = turn
        self.incheck = self.in_check(board_pos)

        #wR, wK, wR, bR, bK, bR
        self.piecesmoved = [False, False, False, False, False, False]
        self.attackingmoves = {}
        #valid sides, wK, wQ, bK, bQ
        self.validcastlesides = [self.wKside(),
                                 self.wQside(),
                                 self.bKside(),
                                 self.bQside(),]
    
    #checking if king side is valid
    def wKside(self):
        self.haspiecesmoved()
        if self.incheck == False: #if not in check
            if self.piecesmoved[1] == False and self.piecesmoved[2] == False: #if the king and rook have not moved at all
               
                if self.board_pos[7][5] == "__" and self.board_pos[7][6] == "__": #if squares between is empty
                    for start, end in self.attackingmoves.items(): #atacking moves
                        for value in end:
                            #checks to see if the squares between the king and rook are not being attacked by the enemy side
                            if value == (7, 5) or value == (7, 6): 
                                
                                return False #if it is then return False
                    return True # if everything is valid then return True                
        return False # return False
    
    #similarily the same for every other side wQ side, bKside, bQside in different coordinates
    

    def wQside(self):
        self.haspiecesmoved() #if pieces moved
        if self.incheck == False:
            if self.piecesmoved[1] == False and self.piecesmoved[0] == False:
                if self.board_pos[7][3] == "__" and self.board_pos[7][2] == "__" and self.board_pos[7][1] == "__":
                    for start, end in self.attackingmoves.items():
                        for value in end:
                            if value == (7, 3) or value == (7, 2): #7 ,1 can be attacked but has to be empty
                                return False
                    return True                
        return False

    def bKside(self):
        self.haspiecesmoved()
        if self.incheck == False:
            if self.piecesmoved[3] == False and self.piecesmoved[4] == False:
                if self.board_pos[0][2] == "__" and self.board_pos[0][3] == "__" and self.board_pos[0][1] == "__":
                    for start, end in self.attackingmoves.items():
                        for value in end:
                            if value == (0, 3) or value == (0, 2):
                                return False
                    return True                
        return False

    def bQside(self):
        self.haspiecesmoved()
        if self.incheck == False:
            if self.piecesmoved[4] == False and self.piecesmoved[5] == False:
                if self.board_pos[0][5] == "__" and self.board_pos[0][6] == "__":
                    for start, end in self.attackingmoves.items():
                        for value in end:
                            if value == (0, 5) or value == (0, 6):
                                return False
                    return True                
        return False

    def getattackingmoves(self): #attacking movees of opposite sides, attacked squares
        super().opposite()
        ignore, self.attackingmoves = super().valid_moves(self.board_pos, True)
        super().opposite()
        return self.attackingmoves
    
    def haspiecesmoved(self):
        
        #checks if any of the rooks or the kings have ever moved
        if self.board_pos[7][0] != "wR":
            self.piecesmoved[0] = True
        if self.board_pos[7][4] != "wK":
            self.piecesmoved[1] = True
        if self.board_pos[7][7] != "wR":
            self.piecesmoved[2] = True
        if self.board_pos[0][0] != "bR":
            self.piecesmoved[3] = True
        if self.board_pos[0][4] != "bK":
            self.piecesmoved[4] = True
        if self.board_pos[0][7] != "bR":
            self.piecesmoved[5] = True
        return self.piecesmoved
        
       