import pygame
import json
import copy, random
import time
from sys import exit
from button import Button
from boardBackground import Board
from game import Moving
from game1 import Moving1
from valid import ValidMoves
from checking import CheckingMoves
from check import ChessRules
from castling import Castling
from ai import MinMax
from learning import learningChess

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Marlex NEA Chess AI")
clock = pygame.time.Clock()
test_font = pygame.font.SysFont("Arial", 30)
game_active = False



move_sound = pygame.mixer.Sound("move-self.mp3")
capture_sound = pygame.mixer.Sound("capture.mp3")
text = Button(0 ,0 ,None)
#screen
screen = pygame.display.set_mode((800, 600))
width, height = 600, 800
rows, cols = 8, 8
square_size = width // cols
board_pos = [
    ["bR","bH","bB","bQ","bK","bB","bH","bR"],
    ["bP","bP","bP","bP","bP","bP","bP","bP"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["wP","wP","wP","wP","wP","wP","wP","wP"],
    ["wR","wH","wB","wQ","wK","wB","wH","wR"],
]

board_pos1 = [
    ["__","__","__","__","bK","bB","__","__"],
    ["__","__","__","__","__","__","wR","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["wR","__","__","wK","__","__","__","__"],
]
board_pos2 = [
    ["__","bP","__","__","bK","bB","__","__"],
    ["__","__","__","bH","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","bR","__","__","__","__","__"],
    ["__","__","__","__","__","__","__","__"],
    ["__","__","__","__","wP","wP","wP","__"],
    ["wR","__","__","wQ","wK","__","__","wR"],
]

board_pos3 = [
    ["__","bP","__","__","bK","bB","__","__"],
    ["__","__","bP","bH","bP","__","__","__"],
    ["bP","__","__","__","__","__","__","__"],
    ["__","__","__","__","__","wP","bP","__"],
    ["__","__","bR","__","__","__","__","__"],
    ["__","bB","__","__","__","__","__","__"],
    ["__","__","__","__","wP","wP","__","__"],
    ["__","__","__","wQ","wK","__","__","wR"],
]

turn = "white"
#https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

#buttons
playButton = Button(400, 100, "Play")
learnButton = Button(400, 200, "Learn")
aiButton = Button(400, 100, "AI")
soloButton = Button(400, 200, "Solo")
backButton = Button(400, 300, "Back") #back button
exitButton = Button(400, 300, "Exit") #exit
xButton = Button(780, 20, "X")
checkText = Button(700, 400, "Check!")
backButton2 = Button(400, 400, "Back")
checkmateButton = Button(400, 200, "Checkmating")
castlingButton = Button(400, 100, "Castling")
enpassantButton = Button(400, 300, "En Passant")


#objects
board_ob = Board(screen, width, height, rows, cols, square_size, board_pos)
game_ob = Moving(screen, width, height, rows, cols, square_size, board_pos)
game_ob1 = Moving1(screen, width, height, rows, cols, square_size, board_pos)
valid_ob = ValidMoves(board_pos)
learn_ob = learningChess(screen, width, height, rows, cols, square_size, board_pos1)
learn_castleOb = learningChess(screen, width, height, rows, cols, square_size, board_pos2)
learn_enpOb = learningChess(screen, width, height, rows, cols, square_size, board_pos3)
check = False
incheck = False
pawnPromotion = False
promotionInput = ""
cmvalidmove = False
cmdone = False
capturedpieces = []
validText = ""
piecemoves = None
var1 = False
valmoves = None
part = 0 
startTime = 0


#images
board_ob.load_image("images/bB_img.png", "bB")
board_ob.load_image("images/bH_img.png", "bH")
board_ob.load_image("images/bK_img.png", "bK")
board_ob.load_image("images/bP_img.png", "bP")
board_ob.load_image("images/bR_img.png", "bR")
board_ob.load_image("images/bQ_img.png", "bQ")

board_ob.load_image("images/wB_img.png", "wB")
board_ob.load_image("images/wH_img.png", "wH")
board_ob.load_image("images/wK_img.png", "wK")
board_ob.load_image("images/wP_img.png", "wP")
board_ob.load_image("images/wR_img.png", "wR")
board_ob.load_image("images/wQ_img.png", "wQ")

learn_ob.pieces = board_ob.pieces.copy()
learn_castleOb.pieces = board_ob.pieces.copy()
learn_enpOb.pieces = board_ob.pieces.copy()


#menu screens
def main():
    global game_active #game active
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if pressed window close button
                pygame.quit() #end program
                exit()
            else: 
                game_active = True # game is active
            if event.type == pygame.MOUSEBUTTONDOWN: #mouse collision
                if playButton.collide(event): #if playbutton pressed run play function
                    play()

                if learnButton.collide(event):
                    learn() #if learnbutton pressed run learn function

                if exitButton.collide(event):
                    pygame.quit() #if exitbutton pressed end program
                    exit()


        if game_active: #if game true
            screen.fill((0, 128, 0)) #background
            playButton.update(screen) #print to screen buttons
            learnButton.update(screen)
            exitButton.update(screen)
        pygame.display.update()

def learn():
    global game_active
    while True: 
        for event in pygame.event.get():
            #if pressed window close button
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            #collisions for mouse with buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton2.collide(event):
                    main()

                if checkmateButton.collide(event):
                    cmWindow()

                if castlingButton.collide(event):
                    castWindow()
                
                if enpassantButton.collide(event):
                    enpWindow()
        #if game active run these buttons on screen
        if game_active:
            screen.fill((0, 128, 0))
            backButton2.update(screen)
            checkmateButton.update(screen)
            castlingButton.update(screen)
            enpassantButton.update(screen)
        pygame.display.update()

def play(): 
    global game_active
    while True:
        #play function
        #print buttons on screen
        screen.fill((0,128,0)) #green background
        aiButton.update(screen)
        soloButton.update(screen)
        backButton.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if pressed window close button
                pygame.quit()
                exit()
            
            #collisions for mouse with buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.collide(event):
                    main()
                
                if soloButton.collide(event):
                    soloWindow()

                if aiButton.collide(event):
                    aiWindow()
                    

        pygame.display.update() #updating screen


#board
def board(check):
    
    
    board_ob.check()
    board_ob.background(screen) #8x8 board printed
    board_ob.print_images(screen) #piece images printed
    xButton.update(screen) #x button top right
    board_ob.print_capturedPieces(capturedpieces, screen)
    if check == True and game_active == True:
        checkText.update(screen) #if dheck true print check on screen
    if piecemoves != None and not var1:
        game_ob.printing_validMoves(piecemoves, screen) #printing valid squares on screen
    if turn == "white": #printing turn on screen
        turnText = Button(700, 350, "white's turn")
    else: turnText = Button(700, 350, "black's turn")
    if pawnPromotion == True: #text for valid pawn promotion
        text.paraText(30, "Pawn Promotion!", 700, 450, screen)
        text.paraText(30, "press Q,K,B,R! for a", 700, 500, screen)
        text.paraText(20, "queen, king, bishop or rook", 700, 550, screen)
    if game_active == False and check == True: #text if checkmate
        text.paraText(30, "checkmate!", 700, 500, screen)
        text.paraText(30, "click x to go back", 700, 550, screen)
    if game_active == False and check == False: #text if draw
        text.paraText(30, "draw!", 700, 500, screen)
        text.paraText(30, "click x to go back", 700, 550, screen)
    turnText.update(screen) #text for white or black turn
    
    pygame.display.update()

def aiboard(check):
    
    
    board_ob.check()
    board_ob.background(screen) #8x8 board printed
    board_ob.print_images(screen) #piece images printed
    xButton.update(screen) #x button top right
    board_ob.print_capturedPieces(capturedpieces, screen)
    if incheck == True and game_active == True:
        checkText.update(screen) #if dheck true print check on screen
    if piecemoves != None and not var1:
        game_ob.printing_validMoves(piecemoves, screen) #printing valid squares on screen
    if turn == "white": #printing turn on screen
        turnText = Button(700, 300, "white's turn")
    else: turnText = Button(700, 300, "black's turn")
    turnText.update(screen) #turn text
    userscore, aiscore = record() #scores from json file record
    userscore, aiscore = str(userscore), str(aiscore) #int to str
    userscore, aiscore = f"User: {userscore}", f"AI: {aiscore}" #user score ai score displayed
    text.paraText(30, userscore, 650, 20, screen)
    text.paraText(30, aiscore, 650, 40, screen)
    if pawnPromotion == True: #text for valid pawn promotion
        text.paraText(30, "Pawn Promotion!", 700, 450, screen)
        text.paraText(30, "press Q,K,B,R! for a", 700, 500, screen)
        text.paraText(20, "queen, king, bishop or rook", 700, 550, screen)
    if game_active == False and incheck == True:  #text if checkmate
        text.paraText(30, "checkmate!", 700, 500, screen)
        text.paraText(30, "click x to go back", 700, 550, screen)
    if game_active == False and incheck == False: #text if draw
        text.paraText(30, "draw!", 700, 500, screen)
        text.paraText(30, "click x to go back", 700, 550, screen)
    pygame.display.update()


#chessgame for solo
def soloChessGame(events):
    global x1, y1, x2, y2, pieceone, piecetwo, checking_ob, valid_ob, yxlist, check, piecemoves, var1, game_active, pawnPromotion, check_ob, board_pos, capturedpieces
    mouse = pygame.mouse.get_pos() #mouse
    for event in events:
        if event.type == pygame.QUIT:  #events
            pygame.quit()
            exit()

        if pawnPromotion: #pawn promotion
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_q: #if user presses Q key
                    promotionInput = "Q"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput) #changes pawn on board to queen
                    pawnPromotion = False
                    continue
                #similar for R, B, H key
                if event.key == pygame.K_r:
                    promotionInput = "R"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                if event.key == pygame.K_b:
                    promotionInput = "B"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                if event.key == pygame.K_h:
                    promotionInput = "H"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                else:
                    # if none of keys pressed, return until one is
                    print("Invalid")
            return
                
    
        if event.type == pygame.MOUSEBUTTONDOWN: #every time its clicked run these
            game_ob.piece_xy(mouse) #give mouse coords
            
            yxlist, selectlist = game_ob.piece_selection() #piece selected
            y1, x1, y2, x2 = game_ob.co_ords() #coords of piece
            
            if y1 >= 8 or x1 >= 8 or y2 >= 8 or x2 >= 8:
                return #if click is not with in range
            pieceone, piecetwo = game_ob.piece_name() # piece names
            castling_ob = Castling(board_pos, turn) # finding castles 
            validcastlesides = castling_ob.validcastlesides
            #class for checking valid moves
            checking_ob = CheckingMoves(x1, y1, x2, y2, pieceone, piecetwo, board_pos, yxlist, validcastlesides, turn)
            #class for rules like check, promotion
            check_ob = ChessRules(board_pos, checking_ob.validlist, turn, yxlist, validcastlesides)
            reset(yxlist, selectlist) #resets yxlist after two pieces selected
            print(yxlist)
            check_ob.boardpieces(board_pos) #puts all pieces on board in a dictionary
            validmoves, attack_moves = check_ob.valid_moves(board_pos, False)  #validmoves for turn
            check = check_ob.in_check(board_pos) #if king is in check
            invalidmoves, _, _, = check_ob.check()  #invalid moves regarding check
            var1 = validmoving1(validmoves, invalidmoves, check, yxlist) #if move is valid
            newvalidmoves, _ = check_ob.popping_invalid(validmoves) #new moves if theres invalid moves
            piecemoves = validmoves.get((y1, x1), []) #valid moves of clicked square
            if newvalidmoves != "F":
                piecemoves = newvalidmoves.get((y1, x1), []) #new valid moves of clicked square if theres invalidmoves
            var = validmoving(newvalidmoves, yxlist, check) #if newmove is valid
            valid_ob.findenpassantmoves(yxlist, pieceone) #finds en passant moves
            moving_move(pieceone, newvalidmoves, check, var, var1) #moves pieces on board if valid
            capturedpieces = (game_ob.capturedpieces) #captured pieces
            #print(var, var1)
            #print(board_pos)
            if (check_ob.checkIfPawnPromotion(board_pos)):
                pawnPromotion = True #if pawn promotion is valid, run pawn promotion section
                return

            if draw(board_pos): #if draw
                game_active = False
            if newvalidmoves != "F":
                if stalemate(newvalidmoves, check):
                    game_active = False
            else:
                if stalemate(validmoves, check):
                    game_active = False
            if checkmate(validmoves, check):
                game_active = False #if draw
        
        

    

#ai chessgame
def soloAiGame(events):
    global x1, y1, x2, y2, pieceone, piecetwo, checking_ob, valid_ob, yxlist, validcastlesides, var1, check_ob, var, turn, piecemoves, game_active, check_ob, pawnPromotion, board_pos, capturedpieces, incheck
    mouse = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
       
        if pawnPromotion:
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_q:
                    promotionInput = "Q"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                if event.key == pygame.K_r:
                    promotionInput = "R"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                if event.key == pygame.K_b:
                    promotionInput = "B"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                if event.key == pygame.K_h:
                    promotionInput = "H"
                    print(promotionInput)
                    check_ob.changePawn(board_pos, promotionInput)
                    pawnPromotion = False
                    continue
                else:
                    print("Invalid")
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and turn == "white":
            game_ob1.piece_xy(mouse)
            yxlist, selectlist = game_ob1.piece_selection()
            y1, x1, y2, x2 = game_ob1.co_ords()
            if y1 >= 8 or x1 >= 8 or y2 >= 8 or x2 >= 8:
                return
            
            pieceone, piecetwo = game_ob1.piece_name()
            castling_ob = Castling(board_pos, turn)
            castling_ob.haspiecesmoved()
            validcastlesides = castling_ob.validcastlesides
            checking_ob = CheckingMoves(x1, y1, x2, y2, pieceone, piecetwo, board_pos, yxlist, validcastlesides, turn)
            check_ob = ChessRules(board_pos, checking_ob.validlist, turn, yxlist, validcastlesides)
            reset(yxlist, selectlist)
            print(yxlist)
            check_ob.boardpieces(board_pos)
            validmoves, attack_moves = check_ob.valid_moves(board_pos, False) 
            check = check_ob.in_check(board_pos)
            invalidmoves, _, _, = check_ob.check()
            var1 = validmoving1(validmoves, invalidmoves, check, yxlist)
            newvalidmoves, _ = check_ob.popping_invalid(validmoves)
            piecemoves = validmoves.get((y1, x1), [])
            if newvalidmoves != "F":
                piecemoves = newvalidmoves.get((y1, x1), [])
            var = validmoving(newvalidmoves, yxlist, check)
            valid_ob.findenpassantmoves(yxlist, pieceone)
            aimoving_move(pieceone, newvalidmoves, check, var, var1)
            capturedpieces = (game_ob1.capturedpieces)
            if (check_ob.checkIfPawnPromotion(board_pos)):
                pawnPromotion = True
                return   
            #if its a draw, or checkmate before the ai move

            
            if var1 or var: #if whites move was valid first
                coeffficient = recordcoefficient() #coefficient from record
                switch_turn() #black turn
                check_ob.opposite() #black turn
                check_ob.board_pos = board_pos #updating board
                oppVM, __ = check_ob.valid_moves(board_pos, False) #opponents valid moves
                incheck = check_ob.in_check(board_pos) # if in check
                check_ob.check() 
                oppNVM, _ = check_ob.popping_invalid(oppVM) #opponents new moves if theres invalid moves
                ai_ob = MinMax(coeffficient) #minmax class
                if checkmate(oppNVM, incheck): #if no valid moves and in check
                    print("user checkmate")
                    
                    addToRecord(1, 0) #add score to json file of user
                    game_active = False
                    return
                if draw(board_pos):
                    game_active = False #if draw
                if oppNVM != "F":
                    randomMove = ai_ob.findBestMove(oppNVM, board_pos, "black") #if new moves pass in new moves
                else:
                    randomMove = ai_ob.findBestMove(oppVM, board_pos, "black") #if not pass validmoves
                if randomMove != None:
                    print(randomMove)
                    move_piece(randomMove) #moves piece on board
                check_ob.blackPawnPromotion(board_pos) #automatically promotes pawn to queen for ai
                
                switch_turn()
                check_ob.opposite()
                check_ob.board_pos = board_pos #updates board
                incheck = check_ob.in_check(board_pos) #find check
                VmAfterAi, __ = check_ob.valid_moves(board_pos, False) #vm for white
                check_ob.check()
                NvmAfterAi, _ = check_ob.popping_invalid(VmAfterAi)
                if NvmAfterAi != "F":
                    VmAfterAi = NvmAfterAi 
                if draw(board_pos):
                    game_active = False #if draw after ai move
                    capturedpieces = []
                elif checkmate(VmAfterAi, incheck): #if checkmate after ai move
                    capturedpieces = []
                    print("ai checkmate")
                    addToRecord(0, 1)  # add score to json file of ai
                    game_active = False 
                elif stalemate(VmAfterAi, incheck): 
                    print("stalemate")
                    game_active = False
                    capturedpieces = []
                pygame.display.update()
                      


#validmoving 
def validmoving(newvalidmoves, yxlist, check):
    if len(yxlist) == 2: #if len of two selected piece 
        yx1 = yxlist[0] #coordinates
        yx2 = yxlist[1]
        y1 = yx1[0]
        x1 = yx1[1]
        y2 = yx2[0]
        x2 = yx2[1]
    else:
        
        return False
    if check == True: #if true
        for (starty, startx), end in newvalidmoves.items(): 
            for (endy, endx) in end: #goes through moves
                if [(y1,x1),(y2,x2)] == [(starty, startx),(endy, endx)]:
                    return True  #if move picked by user is in valid moves return True
    return False #else return False

def validmoving1(validmoves, invalidmoves, check, yxlist):
    if len(yxlist) == 2: #if length is two
        yx1 = yxlist[0] #coordinates
        yx2 = yxlist[1]
        y1 = yx1[0]
        x1 = yx1[1]
        y2 = yx2[0]
        x2 = yx2[1]
    else: 
        return False
    for key, values in invalidmoves.items():#goes through invalid moves
        if key in validmoves:  #if start_move in invalidmoves
            validmoves[key] = [move for move in validmoves[key] if move not in values]  #pops invalid moves
    validmoves = {k: v for k, v in validmoves.items() if v} #removes empty moves
    if check == False:
        for (starty, startx), end in validmoves.items():
            for (endy, endx) in end:
                #if move is in now in new valid moves
                if [(y1,x1),(y2,x2)] == [(starty, startx),(endy, endx)]:
                    return True
    return False

#validmoving for solo
def moving_move(pieceone, newvalidmoves, check, var, var1):
    global turn, pawnvalidmove
    pawnvalidmove = False
    validmove = True
    if validmove in checking_ob.validlist: #if move is a valid in validlist
        if check == True: #if itwas a check
            if var:                    
                if pieceone[1] == "P":
                    turn, move = game_ob.sideturn(checking_ob.checking_pawn()) #change turn if true
                    game_ob.movepos(checking_ob.checking_pawn()) #move it in board if true
                elif pieceone[1] == "H":
                    turn, move = game_ob.sideturn(checking_ob.checking_horse())
                    game_ob.movepos(checking_ob.checking_horse())
                elif pieceone[1] == "B":
                    turn, move = game_ob.sideturn(checking_ob.checking_bishop())
                    game_ob.movepos(checking_ob.checking_bishop())
                elif pieceone[1] == "R":
                    turn, move = game_ob.sideturn(checking_ob.checking_rook())
                    game_ob.movepos(checking_ob.checking_rook())
                elif pieceone[1] == "Q":
                    turn, move = game_ob.sideturn(checking_ob.checking_queen())
                    game_ob.movepos(checking_ob.checking_queen())
                elif pieceone[1] == "K":
                    turn, move = game_ob.sideturn(checking_ob.checking_king())
                    game_ob.movepos(checking_ob.checking_king())
                
            else: return
        elif check == False and var1 == True: #if its not check and is a valid move
            if pieceone[1] == "P": #if its a pawn
                pawnvalidmove = (checking_ob.checking_pawn())
                turn, move = game_ob.sideturn(pawnvalidmove) #switch turn if a valid move
                
                game_ob.movepos(pawnvalidmove) #move it in the board if it is a valid move
            elif pieceone[1] == "H":
                turn, move = game_ob.sideturn(checking_ob.checking_horse())
                game_ob.movepos(checking_ob.checking_horse())
            elif pieceone[1] == "B":
                turn, move = game_ob.sideturn(checking_ob.checking_bishop())
                game_ob.movepos(checking_ob.checking_bishop())
            elif pieceone[1] == "R":
                turn, move = game_ob.sideturn(checking_ob.checking_rook())
                game_ob.movepos(checking_ob.checking_rook())
            elif pieceone[1] == "Q":
                turn, move = game_ob.sideturn(checking_ob.checking_queen())
                game_ob.movepos(checking_ob.checking_queen())
            elif pieceone[1] == "K":
                turn, move = game_ob.sideturn(checking_ob.checking_king())
                game_ob.movepos(checking_ob.checking_king())
            
        else: return



#validmoving for ai
def aimoving_move(pieceone, newvalidmoves, check, var, var1):
    #same as moving move
    global turn, pawnvalidmove
    pawnvalidmove = False
    validmove = True
    if validmove in checking_ob.validlist:
        if check == True and turn == "white": #always white turn
            if var:                    
                #no side turns as always white
                if pieceone[1] == "P":
                    game_ob1.movepos(checking_ob.checking_pawn())
                elif pieceone[1] == "H":
                    game_ob1.movepos(checking_ob.checking_horse())
                elif pieceone[1] == "B":
                    
                    game_ob1.movepos(checking_ob.checking_bishop())
                elif pieceone[1] == "R":
                    
                    game_ob1.movepos(checking_ob.checking_rook())
                elif pieceone[1] == "Q":
                   
                    game_ob1.movepos(checking_ob.checking_queen())
                elif pieceone[1] == "K":
                    
                    game_ob1.movepos(checking_ob.checking_king())
            else: return
        elif check == False and var1 == True and turn == "white":
            if pieceone[1] == "P":
                pawnvalidmove = (checking_ob.checking_pawn())
                game_ob1.movepos(pawnvalidmove)
            elif pieceone[1] == "H":
                game_ob1.movepos(checking_ob.checking_horse())
            elif pieceone[1] == "B":
                game_ob1.movepos(checking_ob.checking_bishop())
            elif pieceone[1] == "R":
                game_ob1.movepos(checking_ob.checking_rook())
            elif pieceone[1] == "Q":
                game_ob1.movepos(checking_ob.checking_queen())
            elif pieceone[1] == "K":
                game_ob1.movepos(checking_ob.checking_king())
        else: return
    

#endgame states
def checkmate(newvalidmoves, check):
    temp = []
    if check == True:
        for (y,x), end in newvalidmoves.items():
            for (a,b) in end:
                temp.append((a,b)) #appends in temp list
        #if list empty means no valid moves and check istrue
        #so its checkmate
        if (len(temp)) == 0:
            return True
        else: 
            return False
    return False

def stalemate(newvalidmoves, check):
    temp = []
    if check == False:
        for (y,x), end in newvalidmoves.items():
            for (a,b) in end:
                temp.append((a,b))
        #if list empty means no valid moves and check is false
        #so its checkmate
        if (len(temp)) == 0:
            return True
        else: 
            return False
    return False

def draw(board_pos):
    pieces = []
    for row in board_pos:
        for piece in row:
            if piece != "__":
                pieces.append(piece)
    #draw situations
    if len(pieces) == 2:
        return True #only kings left
    if len(pieces) == 3:
        if "wH" in pieces or "bH" in pieces: #if these pieces are left plus kings
            return True
        if "wB" in pieces or "bB" in pieces:
            return True
    if len(pieces) == 4:
        if "bB" in pieces: #if only these pieces are available
            if "wH" in pieces or "wB" in pieces:
                return True
        if "bH" in pieces:
            if "wH" in pieces or "wB" in pieces:
                return True
    return False



 
#random move
def ai(moves):
    for start, end in list(moves.items()):
        if end == []:
            moves.pop(start, end)
    key, value = random.choice(list(moves.items()))
    while len(value) >= 2:
        value.pop(random.randint(0, len(value)-1))
    
    value = value[0]
    return (key, value)
            


#method
def move_piece(move):
    #moves piece in board
    start_pos, end_pos = move
    board_pos[end_pos[0]][end_pos[1]] = board_pos[start_pos[0]][start_pos[1]]
    board_pos[start_pos[0]][start_pos[1]] = "__"
    move_sound.play()
    return board_pos

def switch_turn():
    #swaps turn
    global turn
    turn = "black" if turn == "white" else "white"

def reset(yxlist, selectlist):
    #pops second piece clicked if move not valid
    validmove = True
    if len(selectlist) == 2:
        if validmove in checking_ob.validlist:
            return yxlist, selectlist
        else:
            yxlist.pop(0)
            selectlist.pop(0)
    return yxlist, selectlist

def record():
    #json file returns scores
    with open("score1.json", "r") as f:
        data = json.load(f)
    return list(data.values())[0], list(data.values())[1],

def recordcoefficient():
    with open("score1.json", "r") as f: #opening
        data = json.load(f)
    userScore = list(data.values())[0] #list as in dictionary before
    aiScore = list(data.values())[1]
    coefficient = userScore / (aiScore+userScore) #coefficient
    #user / total always between 0-1
    return coefficient

def addToRecord(user, ai):
    #passses arguments if 0, 1 adds 1 to ai score
    with open("score1.json", "r") as f: #loads json file
        scores = json.load(f)
    scores["white"] += user
    scores["ai(black)"] += ai
    with open("score1.json", "w") as f:
        json.dump(scores, f) #stores back into json file

def reset_board_position():
    global board_pos, turn, check, pawnPromotion, game_active, capturedpieces, piecemoves, var1, valmoves, cmvalidmove, cmdone
    # Reset to the default starting position
    board_pos = [
        ["bR","bH","bB","bQ","bK","bB","bH","bR"],
        ["bP","bP","bP","bP","bP","bP","bP","bP"],
        ["__","__","__","__","__","__","__","__"],
        ["__","__","__","__","__","__","__","__"],
        ["__","__","__","__","__","__","__","__"],
        ["__","__","__","__","__","__","__","__"],
        ["wP","wP","wP","wP","wP","wP","wP","wP"],
        ["wR","wH","wB","wQ","wK","wB","wH","wR"],
    ]
    # Reset game state variables
    turn = "white"
    check = False
    pawnPromotion = False
    game_active = True
    capturedpieces = []
    piecemoves = None
    var1 = False
    valmoves = None
    # Update the board object with the new position
    board_ob.board_pos = board_pos
    game_ob.board_pos = board_pos
    game_ob1.board_pos = board_pos
    game_ob.capturedpieces = []
    game_ob1.capturedpieces = []
    board_ob.board_pos = board_pos
    valid_ob.board_pos = board_pos

    game_ob1.turn = "white"
    game_ob.turn = "white" 


#combining functions



def soloWindow():
    while True:
        clock.tick(60) #fps
        events = pygame.event.get() #events
        for event in events:
            if event.type == pygame.QUIT: #window close button
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if xButton.collide(event):
                        reset_board_position() # Reset board position before going back
                        main() #goes back
                      
        board(check) #board
        soloChessGame(events) #runs solo game
        
def aiWindow():
    while True:
        clock.tick(60) #fps
        events = pygame.event.get() #events
        for event in events:
            if event.type == pygame.QUIT: #window close button
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if xButton.collide(event):
                        reset_board_position() # Reset board position before going back
                        main() #goes back
                      
        aiboard(check) #board
        soloAiGame(events)#runs ai game
        
def cmWindow():
    while True:
        clock.tick(60) #fps
        events = pygame.event.get() #events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: #window close button
                    if xButton.collide(event):
                        main() #goes back

        cmboard(events) #board
        cmGame(events) #runs checkmate game
        pygame.display.update()

def castWindow():
    while True:
        clock.tick(60) #fps
        events = pygame.event.get() #events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: #window close button
                    if xButton.collide(event):
                        main() #goes back

        castboard(events)  #board
        castGame(events) #runs castling game

def enpWindow():
    while True:
        clock.tick(60) #fps
        events = pygame.event.get() #events
        for event in events: #window close button
            if event.type == pygame.MOUSEBUTTONDOWN: #goes back
                    if xButton.collide(event):
                        main()

        enpboard(events) #board
        enpGame(events) #runs en passant game


#learning section


def cmboard(events):
    global cmdone
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() #window close button
            exit()
    #8x8 board
    learn_ob.background(screen)
    #piece images
    learn_ob.print_images(screen)
    #x back button
    xButton.update(screen)
    # text on right side explaining game
    text.paraText(17, "Checkmating involves checking the", 700, 100, screen)
    text.paraText(18, "opponents King, and removing", 700, 140, screen)
    text.paraText(18, "all opponents valid moves", 700, 180, screen)
    text.paraText(18, "Find the checkmating move!", 700, 220, screen)
    if valmoves != None:
        #printing valid squares on board
        game_ob.printing_validMoves(valmoves, screen)
    #moves piece on board if valid
    if cmvalidmove and not cmdone:
        move_sound.play()
        learn_ob.movepiece([(7,0), (0,0)])
        cmdone = True
        
        
    pygame.display.update()

def cmGame(events):
    global cmvalidmove, validText, valmoves
    mouse = pygame.mouse.get_pos()
    # mouse position
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_ob.piece_xy(mouse)
            yxlist, selectlist = game_ob.piece_selection() #pieces selected
            cmy1, cmx1, y2, x2 = game_ob.co_ords() # rows and cols
            temp_castling = Castling(board_pos1, "white") #valid castles
            temp_castles = temp_castling.validcastlesides
            temp_rules = ChessRules(board_pos1, None, "white", None, temp_castles)
            validmoves, __  = temp_rules.valid_moves(board_pos1, False) #valid moves
            
            
            valmoves = validmoves.get((cmy1, cmx1), []) #valid moves of first click
            if len(yxlist) == 2:
                if (y2, x2) == (0, 0): #if moves correct position
                    cmvalidmove = True #valid
                    validText = "Correct!" 

                else:
                    cmvalidmove = False #false
                    validText = "Try Again"
            
    if cmvalidmove:
        text.paraText(30, validText, 700, 400, screen) #correct!
    if cmvalidmove == False:
        text.paraText(30, validText, 700, 400, screen) #try again
    
    pygame.display.update()

def castboard(events):
    global cmdone
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() #window close button
            exit()
    #8x8 board
    learn_castleOb.background(screen)
    #piece images
    learn_castleOb.print_images(screen)
    #x back button
    xButton.update(screen)
    # text on right side explaining game
    text.paraText(17, "Castling involves putting the", 700, 100, screen)
    text.paraText(18, "King in safety with the ", 700, 140, screen)
    text.paraText(18, "rook.", 700, 180, screen)
    text.paraText(18, "Find the castling move!", 700, 220, screen)
    if valmoves != None:
        #printing valid squares on board
        game_ob.printing_validMoves(valmoves, screen)
    #moves piece on board if valid
    if cmvalidmove and not cmdone:
        move_sound.play()
        learn_castleOb.movepiece([(7,4), (7,6)])
        learn_castleOb.movepiece([(7,7), (7,5)])
        cmdone = True
        
        
    pygame.display.update()

def castGame(events):
    global cmvalidmove, validText, valmoves
    mouse = pygame.mouse.get_pos()
    # mouse position
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_ob.piece_xy(mouse)
            yxlist, selectlist = game_ob.piece_selection() #pieces selected
            cmy1, cmx1, y2, x2 = game_ob.co_ords()# rows and cols
            temp_castling = Castling(board_pos2, "white")  #valid castles
            temp_castles = temp_castling.validcastlesides
            temp_rules = ChessRules(board_pos2, None, "white", None, temp_castles) #valid moves
            validmoves, __  = temp_rules.valid_moves(board_pos2, False) 
            
            
            valmoves = validmoves.get((cmy1, cmx1), [])#valid moves of first click
            if len(yxlist) == 2:
                if (y2, x2) == (7, 6): #if moves correct position
                    cmvalidmove = True #valid
                    validText = "Correct!"

                else:
                    cmvalidmove = False
                    validText = "Try Again" #false
            
    if cmvalidmove:
        text.paraText(30, validText, 700, 400, screen)
    if cmvalidmove == False:
        text.paraText(30, validText, 700, 400, screen)
    
    pygame.display.update()


def enpboard(events):
    global cmdone

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit() #window close button
            exit()
    #8x8 board
    learn_enpOb.background(screen)
    #piece images
    learn_enpOb.print_images(screen)
    #x back button
    xButton.update(screen)
    # text on right side explaining game
    text.paraText(17, "En passant is a tricky", 700, 100, screen)
    text.paraText(18, "move with the pawn, its a ", 700, 140, screen)
    text.paraText(18, "hidden attacking move", 700, 180, screen)
    text.paraText(18, "Find the enpassant move!", 700, 220, screen)

    if valmoves != None:
        #printing valid squares on board
        game_ob.printing_validMoves(valmoves, screen)
    #moves piece on board if valid
    if cmvalidmove and not cmdone:
        move_sound.play()
        learn_enpOb.movepiece([(3,5), (2, 4)])
        cmdone = True

    pygame.display.update()

def enpGame(events):
    global cmvalidmove, validText, valmoves, part, startTime

    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    mouse = pygame.mouse.get_pos()

    # game part 0 starts this first
    if part == 0:  
        if current_time - startTime >= 2000:  # 2 seconds passed
            learn_enpOb.movepiece([(1, 4), (3, 4)])  # Move the black pawn
            part = 1  #next phase
            startTime = current_time
        
    #then this
    elif part == 1: 
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_ob.piece_xy(mouse)
                yxlist, selectlist = game_ob.piece_selection()
                cmy1, cmx1, y2, x2 = game_ob.co_ords()

                temp_castling = Castling(board_pos3, "white") #castles
                temp_castles = temp_castling.validcastlesides 
                temp_rules = ChessRules(board_pos3, None, "white", None, temp_castles) #rules
                validmoves, __ = temp_rules.valid_moves(board_pos3, False) #validmoves
                valmoves = validmoves.get((cmy1, cmx1), [])
                if (cmy1, cmx1) == (3, 5): #if clicked pawn
                    valmoves = [(2,5), (2,4)] #valid moves
                print(valmoves)
                if len(yxlist) == 2:
                    if (y2, x2) == (2, 4): #if moved correct square
                        cmvalidmove = True
                        validText = "Correct!"
                    else:
                        cmvalidmove = False
                        validText = "Try Again"

        if cmvalidmove: # Update the screen with the new state
            text.paraText(30, validText, 700, 400, screen)
        elif cmvalidmove == False:
            text.paraText(30, validText, 700, 400, screen)

   
    
    pygame.display.update()



main()
pygame.display.update()

