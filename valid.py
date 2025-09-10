import pygame
import copy
pygame.init()

class ValidMoves():
    enpassantmoves = {}

    def __init__(self, board_pos):
        self.board_pos = board_pos
        
        

    def tempcheck(self, temp_board_pos):
        self.board_pos = copy.deepcopy(temp_board_pos)

    
    def revert_board(self, original_board_pos):
        self.board_pos = copy.deepcopy(original_board_pos)

    def horse_valid(self, y1, x1, pieceone):
        self.horse_moves_form = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (-1, +2), (-1, -2), (+1, -2)]
        self.horse_valid_moves = []
        for y, x in self.horse_moves_form: #goes through array of valid moves, adding x, y to current horse position
            self.temp_y1 = y1 + y
            self.temp_x1 = x1 + x
            # if coordinates is within range on the board
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8:
                # if piece location moving to is not already a spot of own pieces
                if self.board_pos[self.temp_y1][self.temp_x1][0] != pieceone[0]:
                    # append location
                    self.horse_valid_moves.append((self.temp_y1, self.temp_x1))
        return self.horse_valid_moves

    def bishop_valid(self, y1, x1, pieceone):
        self.bishop_valid_moves = []
        rows = 8
        #opposite piece
        if pieceone[0] == "w":
            opposite = "b"
        elif pieceone[0] == "b":
            opposite = "w"
        #formula for all diagonal directions top right, top left, bottom left, bottom right
        for i in range(rows):
            #increase by coordinates by 1 every loop
            self.temp_x1 = x1 + i
            self.temp_y1 = y1 + i
            #if within range and not the coordinate itself
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8 and self.temp_x1 != x1 and self.temp_y1 != y1:
                if self.board_pos[self.temp_y1][self.temp_x1][0] == pieceone[0]:
                    break
                    #if hits a piece of its own stop adding moves
                elif self.board_pos[self.temp_y1][self.temp_x1][0] == opposite:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
                    break
                    #if hits a piece of its enemy stop adding moves, but add that last move
                else:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
        
        for i in range(rows):
            self.temp_x1 = x1 + i
            self.temp_y1 = y1 - i
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8 and self.temp_x1 != x1 and self.temp_y1 != y1:
                if self.board_pos[self.temp_y1][self.temp_x1][0] == pieceone[0]:
                    break
                elif self.board_pos[self.temp_y1][self.temp_x1][0] == opposite:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
                    break
                else:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
        
        for i in range(rows):
            self.temp_x1 = x1 - i
            self.temp_y1 = y1 - i 
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8 and self.temp_x1 != x1 and self.temp_y1 != y1:
                if self.board_pos[self.temp_y1][self.temp_x1][0] == pieceone[0]:
                    break
                elif self.board_pos[self.temp_y1][self.temp_x1][0] == opposite:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
                    break
                else:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
        
        for i in range(rows):
            self.temp_x1 = x1 - i
            self.temp_y1 = y1 + i
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8 and self.temp_x1 != x1 and self.temp_y1 != y1:
                if self.board_pos[self.temp_y1][self.temp_x1][0] == pieceone[0]:
                    break
                elif self.board_pos[self.temp_y1][self.temp_x1][0] == opposite:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
                    break
                else:
                    self.bishop_valid_moves.append((self.temp_y1, self.temp_x1))
    
        return self.bishop_valid_moves

    def rook_valid(self, y1, x1, pieceone):
        rook_valid_moves = []
        formula = [(0, +1),(0, -1), (+1, 0), (-1,0)] #formula
        #opposite piece
        if pieceone[0] == "w":
            opposite = "b"
        elif pieceone[0] == "b":
            opposite = "w"
        for y,x in formula:
            for i in range(1,8): #1, 8 board start to end
                temp_y1 = y1 + y * i # goes through formula of every direciton for rook
                temp_x1 = x1 + x * i
                if 0 <= temp_x1 < 8 and 0 <= temp_y1 < 8:
                    # if coordinate is same side piece end
                    if self.board_pos[temp_y1][temp_x1][0] == pieceone[0]:
                        break
                    # if coordinate is opposite side piece end but append last valid move
                    elif self.board_pos[temp_y1][temp_x1][0] == opposite:
                        rook_valid_moves.append((temp_y1, temp_x1))
                        break
                    else:
                        #append move if empty
                        rook_valid_moves.append((temp_y1, temp_x1))
                else: break               

        return rook_valid_moves

    def queen_valid(self, y1, x1, pieceone):
        self.queen_moves = []
        # contains bishop and rook valid moves
        self.queen_moves.extend(ValidMoves.bishop_valid(self, y1, x1, pieceone))
        self.queen_moves.extend(ValidMoves.rook_valid(self, y1, x1, pieceone))
        return self.queen_moves

    def king_valid(self, y1, x1, pieceone, validcastlesides, turn):
        self.king_formula = [(-1, 0), (-1, +1), (-1, -1), (0, +1), (0, -1), (+1, 0), (+1, +1), (+1, -1)] #formula
        self.king_moves = []
        self.validcastlesides = validcastlesides #if castle is free strucuted as false, false, false, false
        self.turn = turn
        for y,x  in self.king_formula:
            #goes through formula appending valid moves
            self.temp_x1 = x1 + x
            self.temp_y1 = y1 + y
            #within range
            if 0 <= self.temp_x1 < 8 and 0 <= self.temp_y1 < 8:
                #if square is not taken by same side piece
                if pieceone[0] != self.board_pos[self.temp_y1][self.temp_x1][0]:
                    self.king_moves.append((self.temp_y1, self.temp_x1))
        
        if self.turn == "white":
            if validcastlesides[0] == True: #if king side castle is free
                self.king_moves.append((7, 6))
            if validcastlesides[1] == True: #if queen side castle is free
                self.king_moves.append((7, 2))
        if self.turn == "black":
            if validcastlesides[3] == True: # if king side castle is free
                self.king_moves.append((0, 6))
            if validcastlesides[2] == True: #if queen side castle is free
                self.king_moves.append((0, 2))
        return self.king_moves

    def pawn_valid(self, y1, x1, pieceone): #screenshot aswell
        self.pawn_moves = []
        self.y1 = y1
        self.pieceone = pieceone
        if self.y1 > 0:
            #white
            if self.pieceone[0] == "w":
                #if piece is at its starting position and the first two up squares are empty
                if self.y1 == 6 and self.board_pos[y1-1][x1] == "__" and self.board_pos[y1-2][x1] == "__": 
                    self.pawn_moves.extend([(y1-1, x1), (y1-2, x1)]) #appending both moves up one or two
                elif self.board_pos[y1-1][x1][0] != "w" and self.board_pos[y1-1][x1][0] != "b":
                    #if piece up one is empty append move
                    self.pawn_moves.append((y1-1, x1))
                #if piece is not edge of board to avoid error
                #if piece top right or top left is an enemy piece append valid move
                if x1 != 7 and self.board_pos[y1-1][x1+1][0] == "b":
                    self.pawn_moves.append((y1-1, x1+1))
                if x1 != 0 and self.board_pos[y1-1][x1-1][0] == "b":
                    self.pawn_moves.append((y1-1, x1-1))
                if y1 == 3:
                    #if piece is at y3, and the piece beside it is a valid enpassant move then append
                    if x1 != 7 and self.board_pos[y1][x1+1] == "bP":
                        if (y1, x1+1) in ValidMoves.enpassantmoves.values():
                            self.pawn_moves.append((y1-1, x1+1))
                    elif x1 != 0 and self.board_pos[y1][x1-1] == "bP":
                        if (y1, x1-1) in ValidMoves.enpassantmoves.values():
                            self.pawn_moves.append((y1-1, x1-1))

            #same as before but for black side
            elif self.pieceone[0] == "b":
                if self.y1 == 1 and self.board_pos[y1+1][x1] == "__" and self.board_pos[y1+2][x1] == "__":
                    self.pawn_moves.extend([(y1+1, x1), (y1+2, x1)])
                elif y1+1 < 8 and self.board_pos[y1+1][x1][0] != "w" and self.board_pos[y1+1][x1][0] != "b":
                    self.pawn_moves.append((y1+1, x1))
                if y1+1 < 8 and x1 != 7 and self.board_pos[y1+1][x1+1][0] == "w":
                    self.pawn_moves.append((y1+1, x1+1))
                if y1+1 < 8 and x1 != 0 and self.board_pos[y1+1][x1-1][0] == "w":
                    self.pawn_moves.append((y1+1, x1-1))
                if y1 == 4:
                    if x1 != 7 and self.board_pos[y1][x1+1] == "wP":
                        if (y1, x1+1) in ValidMoves.enpassantmoves.values():
                            self.pawn_moves.append((y1+1, x1+1))
                    elif x1 != 0 and self.board_pos[y1][x1-1] == "wP":
                        if (y1, x1-1) in ValidMoves.enpassantmoves.values():
                            self.pawn_moves.append((y1+1, x1-1))
        return self.pawn_moves
    
    # this is for attacking moves, like in check, if the user is in check from a pawn attacking
    #as a pawn attacking moves are different from its valid moves
    def pawn_attack(self, y1 ,x1, pieceone):
        self.pieceone = pieceone
        self.y1 = y1
        self.pawn_attack_moves = []
        if self.y1 > 0 and self.y1 != 7:
            if self.pieceone[0] == "w":
                if x1 != 7 and self.board_pos[y1-1][x1+1][0] == "b":
                    self.pawn_attack_moves.append((y1-1, x1+1))
                if x1 != 0 and self.board_pos[y1-1][x1-1][0] == "b":
                    self.pawn_attack_moves.append((y1-1, x1-1))

            elif self.pieceone[0] == "b":
                if x1 != 7 and self.board_pos[y1+1][x1+1][0] == "w":
                    self.pawn_attack_moves.append((y1+1, x1+1))
                if x1 != 0 and self.board_pos[y1+1][x1-1][0] == "w":
                    self.pawn_attack_moves.append((y1+1, x1-1))     

        return self.pawn_attack_moves

    def run_board(self):
        return self.board_pos

    #enpassant
    def findenpassantmoves(self, yxlist, pieceone):
        if len(yxlist) == 2:
            #if two pieces moved
            yx, yx2 = yxlist[0], yxlist[1]
            y1, x1 = yx[0], yx[1]
            y2, x2 = yx2[0], yx2[1]
        else: 
            return ValidMoves.enpassantmoves
        #if piece moved is a pawn
        if pieceone[1] == "P":
            if pieceone[0] == "w":
                if y2 == 4: #if white and is at y4
                    #append the two pieces moved as the valid enpassant currently
                    ValidMoves.enpassantmoves = ({(yx):(yx2)})
            elif pieceone[0] == "b":
                if y2 == 3:
                    #if black and is at y3
                    
                    ValidMoves.enpassantmoves = ({(yx):(yx2)})
    
        return ValidMoves.enpassantmoves
    

    

    