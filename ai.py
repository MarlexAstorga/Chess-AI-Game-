import random, copy
from check import ChessRules
from castling import Castling
class MinMax(Castling, ChessRules):
    def __init__(self , coeffficient):
        self.coefficient = coeffficient
        self.pieces_scores = {"K": 0, "Q": 10, "R": 5, "B": 3, "H": 3, "P": 1} #chess piece values
        self.checkmateScore = 1000 #max
        self.stalemateScore = 0 #stalemate
        self.score = 0 #current score
        self.scores = {} #scores list
    
    def scoreMaterial(self, board_pos):
        #scores pieces on board
        self.score = 0
        for row in board_pos:
            for piece in row:
                if piece[0] == "w":
                    #if white add + is good for white
                    self.score += self.pieces_scores[piece[1]]
                    #if black subtract -negative is good for black
                elif piece[0] == "b":
                    self.score -= self.pieces_scores[piece[1]]
                
        return self.score
    
    def findBestMove(self, validmoves, board_pos, turn):
        turnMultipler = 1 if turn == "white" else -1 #white is positive, black is negative
        opponentMinMaxScore = self.checkmateScore #high score initally
        bestMove = None
        temp_boardpos = board_pos #temp board so original is not changed
        validmoves = list(validmoves.items())
        random.shuffle(validmoves) #random shuffles the moves so its not the same original opening moves
        validmoves = dict(validmoves)
        for start, end in validmoves.items(): #black
            for move in end: #goes through every move
                temp_boardpos = copy.deepcopy(board_pos) #temp board, doesnt alter original
                self.revert_board(temp_boardpos)
                temp_boardpos = self.moveCOORDS(temp_boardpos, start, move) #moves that move in board
                
                temp_castling = Castling(temp_boardpos, "white")
                temp_castles = temp_castling.validcastlesides #finds valid castles
                temp_rules = ChessRules(temp_boardpos, None, "white", None, temp_castles)
                opponentMoves, opponentAttacks = temp_rules.valid_moves(temp_boardpos, False) #finds opponents moves
                temp_rules.check()
                check = temp_rules.in_check(temp_boardpos) #finds check
                opponentNewMoves, __ = temp_rules.popping_invalid(opponentMoves) #newmoves if check is involved
                if opponentNewMoves != 'F':
                    opponentMoves = opponentNewMoves
                if self.ifcheckmate(validmoves, check): #if game is in checkmate
                    opponentMaxScore = -self.checkmateScore #max score is -1000 for black
                elif self.ifstalemate(validmoves, check): #if stalemate
                    opponentMaxScore = self.stalemateScore #maxscore is 0
                else:
                    opponentMaxScore = -self.checkmateScore #else -1000 worst case                                                     
                
                temp_boardpos1 = temp_boardpos #new tempboard
                for start1, end1 in opponentMoves.items(): #white, trying to find best move
                    for move1 in end1: #goes through opponentmoves
                        temp_boardpos1 = copy.deepcopy(temp_boardpos) #new tempboard doesnt alter new
                        self.revert_board(temp_boardpos1)
                        temp_boardpos1 = self.moveCOORDS(temp_boardpos1, start1, move1)#moves opponent move in temp board
                        check1 = temp_rules.in_check(temp_boardpos1) #checks for check
                        if self.ifcheckmate(opponentMoves, check1):
                            self.score = self.checkmate #if checkmate score 1000 for white
                        elif self.ifstalemate(opponentMoves, check1):
                            self.score = self.stalemateScore #if stalemate score 0
                        else:
                            self.score = -turnMultipler * self.scoreMaterial(temp_boardpos1) #scores board for black
                        if self.score > opponentMaxScore: #if score > than previous score
                            opponentMaxScore = self.score #new opponentMax Score = self.score, best score for white,opponent of AI
                            
                            
                        self.revert_board(temp_boardpos1)
                
                self.scores[(start, move)] = opponentMaxScore #stores scores in dictionary with move
                #if opponents score is less than current MinMax score, minmax score is that
                #trying to find the lowest score possible for the opponent(white), which is best move for ai
                if opponentMaxScore < opponentMinMaxScore:
                    opponentMinMaxScore = opponentMaxScore
                    bestMove = (start, move)
                
                self.revert_board(temp_boardpos)
        #sorts moves by score from lowest to highest
        self.scores = sorted(self.scores.items(), key=lambda item: item[1])
        lowest_move, lowest_value = self.scores[0] #bottom score
        highest_move, highest_value = self.scores[-1]
        n = len(self.scores)
        if n % 2 == 1: #medium score
            median_move, median_value = self.scores[n // 2]
        else:
            median_move, median_value = self.scores[n // 2]
        if self.coefficient < 0.33: #beginner
            return lowest_move
        elif self.coefficient >= 0.33 and self.coefficient < 0.66: #medium
            return median_move
        elif self.coefficient >= 0.66: #hard
            return bestMove
        
        
    def scoresreturn(self):
        return self.scores
        
    def moveCOORDS(self, board_pos, start, move):
        #moves in board and returns
        y, x = start[0], start[1]
        y1, x1 = move[0], move[1]
        board_pos[y1][x1] = board_pos[y][x]
        board_pos[y][x] = "__"
        
        return board_pos
    
    def ifcheckmate(self, newvalidmoves, check):
        #checks if checkmate
        temp = []
        if check == True:
            for (y,x), end in newvalidmoves.items():
                for (a,b) in end:
                    temp.append((a,b))
        
            if (len(temp)) == 0:
                return True
            else: 
                return False
        return False

    def ifstalemate(self, newvalidmoves, check):
        #checks if stalemate
        temp = []
        if check == False:
            for (y,x), end in newvalidmoves.items():
                for (a,b) in end:
                    temp.append((a,b))
        
            if (len(temp)) == 0:
                return True
            else: 
                return False
        return False