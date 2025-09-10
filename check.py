import pygame
import copy
pygame.init()
from valid import ValidMoves  # this is your other file where all movement logic is stored

# This class builds on top of ValidMoves and adds actual game rules like check, checkmate etc.
class ChessRules(ValidMoves):
    def __init__(self, board_pos, validmovelist, turn, yxlist, validcastlesides):
        super().__init__(board_pos)
        self.validmovelist = validmovelist  # list of current player's valid moves
        self.turn = turn  # whose turn it is, "white" or "black"
        self.validcastlesides = validcastlesides  # info about which sides castling is allowed
        self.checkbool = False  # flag to say if the king is in check
        self.checkmate = False  # flag to say if it’s checkmate
        self.yxlist = yxlist
        self.promotingpawn = []  # history of moves, usually 2 most recent (for en passant, etc.)

    def boardpieces(self, board_pos):
        # gets all pieces on the board and returns their position and type in a dict
        piecedict = {}
        for y in range(8):
            for x in range(8):
                self.piece = board_pos[y][x]
                if self.piece != "__":  # if square isn't empty
                    piecedict.update({(y, x): self.piece})
        return piecedict

    def opposite(self):
        # flips turn to the other player
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"
        return self.turn

    def valid_moves(self, board_pos, opponent):
        # gets all valid moves for current turn or all attack squares for opponent
        attack_moves = {}
        validmoves = {}
        for (y, x), piece in self.boardpieces(board_pos).items():
            # white's turn
            if self.turn == "white":
                if piece[0] == "w" and opponent == False:  # own pieces, regular valid moves
                    validmoves.update({(y, x): self.valid_functions(y, x, piece, False)})
                elif piece[0] == "w" and piece[1] != "K" and opponent == True:  # attack squares
                    attack_moves.update({(y, x): self.valid_functions(y, x, piece, True)})
            # black's turn
            elif self.turn == "black":
                if piece[0] == "b" and opponent == False:
                    validmoves.update({(y, x): self.valid_functions(y, x, piece, False)})
                elif piece[0] == "b" and piece[1] != "K" and opponent == True:
                    attack_moves.update({(y, x): self.valid_functions(y, x, piece, True)})

        return validmoves, attack_moves

    def check(self):
        # checks if the current player would put themselves in check with any move
        invalid_move = {}  
        valid_move = {}    
        board_pos = copy.deepcopy(self.board_pos) #stores temp version so original board not messed with
        validmoves, _ = self.valid_moves(board_pos, False) #all valid moves
        tempcheck = False
        for (starty, startx), end in validmoves.items():
            for (endy, endx) in end: #goes through every validmove
                checkbool = False  # assume not in check
                self.revert_board(board_pos)  # reset board to current
                temp_boardpos = copy.deepcopy(board_pos)  # make temp board
                temp_piece = temp_boardpos[starty][startx]
                #moves the validmove in a temporary board
                temp_boardpos[endy][endx] = temp_piece
                temp_boardpos[starty][startx] = "__"
                
                # switch turn to enemy and gets their attack moves
                self.opposite()
                self.tempcheck(temp_boardpos)
                _, attack_moves = self.valid_moves(temp_boardpos, True)
                self.opposite()
                self.revert_board(board_pos)  # restore original turn
                # get the king’s position after the move
                kingyx = self.kingyx_find(temp_boardpos)

                # go through each of opponent's attack moves
                for (starty2, startx2), end in attack_moves.items():
                    if checkbool: #end attack moves loop if check is true
                        break
                    for (endy2, endx2) in end:
                        if kingyx == (endy2, endx2):  # if king is under attack
                            checkbool = True #check is true
                            tempcheck = True
                            break

                # if move puts us in check, mark it as invalid
                if checkbool: #if check is true
                    if (starty, startx) not in invalid_move: #if its not already in invalid moves
                        invalid_move[(starty, startx)] = [] #empty it
                    invalid_move[(starty, startx)].append((endy, endx)) #append move that is invalid now because was in check

        return invalid_move, tempcheck, valid_move

    def valid_functions(self, y, x, piece, opponent):
        # decides which piece movement function to use based on type
        if piece[1] == "P":
            if not opponent:
                return ValidMoves.pawn_valid(self, y, x, piece)
            else:
                return ValidMoves.pawn_attack(self, y, x, piece)
        elif piece[1] == "H":
            return ValidMoves.horse_valid(self, y, x, piece)
        elif piece[1] == "B":
            return ValidMoves.bishop_valid(self, y, x, piece)
        elif piece[1] == "R":
            return ValidMoves.rook_valid(self, y, x, piece)
        elif piece[1] == "Q":
            return ValidMoves.queen_valid(self, y, x, piece)
        elif piece[1] == "K":
            return ValidMoves.king_valid(self, y, x, piece, self.validcastlesides, self.turn)

    def kingyx_find(self, board_pos):
        # find where the king is for current player
        king_piece = "wK" if self.turn == "white" else "bK"
        for y in range(8):
            for x in range(8):
                if board_pos[y][x] == king_piece:
                    return (y, x)
        return None

    def popping_invalid(self, temp_validmoves):
        # removes moves that leave king in check
        invalid_move, checkbool, _ = self.check()
        if checkbool:
            for key, value in invalid_move.items():
                if key in temp_validmoves:
                    temp_validmoves[key] = [move for move in temp_validmoves[key] if move not in value]
            return temp_validmoves, checkbool
        return "F", "F"

    def in_check(self, temp_board_pos):
        # checks if the current player's king is in check on a given board
        kingyx = self.kingyx_find(temp_board_pos)
        self.opposite()
        _, attack_moves = self.valid_moves(temp_board_pos, True)
        self.opposite()

        for (starty, startx), end in attack_moves.items():
            for (endy, endx) in end:
                if kingyx == (endy, endx):
                    return True
        return False

    def blackPawnPromotion(self, board_pos):
        # promotes pawn to queen if it gets to final rank, for ai
        for i in range(0, 8):
            if board_pos[7][i] == "bP":
                board_pos[7][i] = "bQ"
        return board_pos


    #checks if pawn promotion is valid
    def checkIfPawnPromotion(self, board_pos):
          for i in range(0, 8):
            if board_pos[0][i] == "wP":
                self.promotingpawn = [0, i] #current valid pawn promotion 
                return True 
            if board_pos[7][i] == "bP":
                self.promotingpawn = [7, i] #current valid pawn promotion 
                return True
    
    def changePawn(self, board_pos, input):
        y, x = self.promotingpawn[0], self.promotingpawn[1] #promotion pawn coordinates
        if self.turn == "white": #if its whitee turn
            if input == "Q": #if input was Q
                board_pos[y][x] = "wQ" #make the pawn to a queen
            if input == "H":
                board_pos[y][x] = "wH"
            if input == "B":
                board_pos[y][x] = "wB"
            if input == "R":
                board_pos[y][x] = "wR"

        if self.turn == "black":
            if input == "Q":
                board_pos[y][x] = "bQ"
            if input == "B":
                board_pos[y][x] = "bB"
            if input == "R":
                board_pos[y][x] = "bR"
            if input == "H":
                board_pos[y][x] = "bH"
        
        return board_pos

    def update_board(self, new_board_pos):
        self.board = copy.deepcopy(new_board_pos)

