import copy 
# initiates all the pieces on the boards
# board = [["a ","b ","c ","d ","e ","f ","g ","h "]]

# b_pieces_1 = [8, "bR", "bK", "bB", "bKi", "bQ", "bB", "bK", "bR"]
# b_pieces_2 = [7, "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]

# w_pieces_1 = [1, "wR", "wK", "wB", "wKi", "wQ", "wB", "wK", "wR"]
# w_pieces_2 = [2, "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]

# board.append(b_pieces_1)
# board.append(b_pieces_2)
# for i in range(5):
#     board.append([7-i,"  ","  ","  ","  ","  ","  ","  ","  "])

# board.append(w_pieces_2)
# board.append(w_pieces_1)
# for i in range(10):
#     print(board[i])

#holds locations and pieces on the board
#(x,y) in array needs board[y][x] 
#board limits x = 1-8, y = 1-8
w_loc = [(1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8),
         (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7)]
b_loc = [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
         (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2)]

## 1st pos in location tuple = x therefore needed second when accessing the array
## print(board[w_loc[0][1]][w_loc[0][0]]) 

#can find location of each piece in the location array
w_pieces = ["wR", "wK", "wB", "wQ", "wKi", "wB", "wK", "wR",
            "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",]
b_pieces = ["bR", "bK", "bB", "bQ", "bKi", "bB", "bK", "bR",
            "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]

#holds captured pieces 
c_pieces_w = []
c_pieces_b = []

#0 white turn, 1 when they select a piece (same for 2 and 3 for black)
turn = 0
selection = 100

#holds the list of moves made
valid_moves = []

piece_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']

#variable to store winner and game running 
winner = ''
game_over = False

#function to draw the board with the pieces
def draw_board():
    #draws an empty board
    board = [["", "a ","b ","c ","d ","e ","f ","g ","h "]]
    for i in range(9):
        board.append([8-i,"  ","  ","  ","  ","  ","  ","  ","  "])

    #iterates through white pieces finding the index and their locations
    for index in enumerate(w_pieces):
        board[w_loc[index[0]][1]][w_loc[index[0]][0]] = index[1]

    for index in enumerate(b_pieces):
        board[b_loc[index[0]][1]][b_loc[index[0]][0]] = index[1]

    for i in range(9):
        print(board[i])
    
    return board

#check all possible moves for the king given the colour and the pos
def check_king(pos, col, fr_list, en_list):
    moves = []

    #checks all 8 surrounding squares 
    targets = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
    for i in range(8):
        target = (pos[0]+targets[i][0], pos[1] + targets[i][1])
        #cant move off board and into fellow colours
        if target not in fr_list and 1<=target[0]<=8 and 1<=target[1]<=8:
            moves.append(target)
    
    return moves

#queen moves like a rook and a bishop so use those functions and combine
def check_queen(pos, col, fr_list, en_list):
    moves = check_rook(pos, col, fr_list, en_list)
    moves_2 = check_bishop(pos, col, fr_list, en_list)
    for i in range(len(moves_2)):
        moves.append(moves_2[i])
    return moves

def check_rook(pos, col, fr_list, en_list):
    moves = []

    #check different directions and with a chain to see how far they can move
    for i in range(4):
        chain = 1
        path = True
        #upwards
        if i == 0:
            x=0
            y=1
        #down
        elif i == 1:
            x=0
            y=-1
        #right
        elif i == 2:
            x=1
            y=0
        #left
        else:
            x=-1
            y=0
        while path:
            #chains moves as far as it can
            if (pos[0] + (chain * x), pos[1] + (chain * y)) not in fr_list and \
                1 <= pos[0] + (chain * x) <= 8 and 1 <= pos[1] + (chain * y) <= 8:
                moves.append((pos[0] + (chain * x), pos[1] + (chain * y)))
                #stops if in enemy or friend list
                if (pos[0] + (chain * x), pos[1] + (chain * y)) in en_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves

#operates same as rook just different directions
def check_bishop(pos, col, fr_list, en_list):
    moves = []

    #check different directions and with a chain to see how far they can move
    for i in range(4):
        chain = 1
        path = True
        #upwards
        if i == 0:
            x=1
            y=1
        #down
        elif i == 1:
            x=-1
            y=1
        #right
        elif i == 2:
            x=-1
            y=-1
        #left
        else:
            x=1
            y=-1
        while path:
            #chains moves as far as it can
            if (pos[0] + (chain * x), pos[1] + (chain * y)) not in fr_list and \
                1 <= pos[0] + (chain * x) <= 8 and 1 <= pos[1] + (chain * y) <= 8:
                moves.append((pos[0] + (chain * x), pos[1] + (chain * y)))
                #stops if in enemy or friend list
                if (pos[0] + (chain * x), pos[1] + (chain * y)) in en_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves

#pawns can have double moves and takes
def check_pawn(pos, col):
    moves_list = []
    if col != 'w':
        #allows one forward move
        if (pos[0], pos[1] + 1) not in w_loc and \
                (pos[0], pos[1] + 1) not in b_loc and pos[1] <= 7:
            moves_list.append((pos[0], pos[1] + 1))
        #double move at start
        if (pos[0], pos[1] + 2) not in w_loc and \
                (pos[0], pos[1] + 2) not in b_loc and pos[1] == 2:
            moves_list.append((pos[0], pos[1] + 2))
        #tests the taking at diagonals
        if (pos[0] + 1, pos[1] + 1) in w_loc:
            moves_list.append((pos[0] + 1, pos[1] + 1))
        if (pos[0] - 1, pos[1] + 1) in w_loc:
            moves_list.append((pos[0] - 1, pos[1] + 1))
    else:
        if (pos[0], pos[1] - 1) not in w_loc and \
                (pos[0], pos[1] - 1) not in b_loc and pos[1] > 1:
            moves_list.append((pos[0], pos[1] - 1))
        if (pos[0], pos[1] - 2) not in w_loc and \
                (pos[0], pos[1] - 2) not in b_loc and pos[1] == 7:
            moves_list.append((pos[0], pos[1] - 2))
        if (pos[0] + 1, pos[1] - 1) in b_loc:
            moves_list.append((pos[0] + 1, pos[1] - 1))
        if (pos[0] - 1, pos[1] - 1) in b_loc:
            moves_list.append((pos[0] - 1, pos[1] - 1))
    return moves_list

#knight moves like a king 8 squares max to go to
def check_knight(pos, col, fr_list, en_list):
    moves = []

    #checks all 8 surrounding squares 
    targets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
    for i in range(8):
        target = (pos[0]+targets[i][0], pos[1] + targets[i][1])
        #cant move off board and into fellow colours
        if target not in fr_list and 1<=target[0]<=8 and 1<=target[1]<=8:
            moves.append(target)
    
    return moves

#test all possible moves for a players
def check_opts(pieces, locs, turn, fr_list=None, en_list=None):
    if fr_list is None or en_list is None:
        if turn == 'w':
            fr_list = w_loc
            en_list = b_loc
        else:
            fr_list = b_loc
            en_list = w_loc

    moves = []
    all_moves = []
    for i in range(len(pieces)):
        for i in range(len(pieces)):
            location = locs[i]
            piece = pieces[i]
            if piece == 'bP' or piece == 'wP':
                moves = check_pawn(location, turn)
            elif piece == 'bK' or piece == 'wK':
                moves = check_knight(location, turn, fr_list, en_list)
            elif piece == 'bB' or piece == 'wB':
                moves = check_bishop(location, turn, fr_list, en_list)
            elif piece == 'bR' or piece == 'wR':
                moves = check_rook(location, turn, fr_list, en_list)
            elif piece == 'bQ' or piece == 'wQ':
                moves = check_queen(location, turn, fr_list, en_list)
            elif piece == 'bKi' or piece == 'wKi':
                moves = check_king(location, turn, fr_list, en_list)
            all_moves.append(moves)
    return all_moves

#checks all the valid moves for a piece thats been selected
def check_valid_moves():
    if turn<2:
        options_list = w_opts
    else:
        options_list = b_opts
    valid_options = options_list[selection]
    return valid_options

#draws moves as o's on the array
def draw_valid(moves, board):
    for i in range(len(moves)):
        board[moves[i][1]][moves[i][0]] = "o "
    for i in range(9):
        print(board[i])

#testing check
def test_check(turn, w_pieces_sim, w_loc_sim, b_pieces_sim, b_loc_sim, w_opts_sim, b_opts_sim):
    if turn == 1:  # Testing if white is in check (after black's move)
        if 'wKi' in w_pieces_sim:
            k_index = w_pieces_sim.index('wKi')
            k_loc = w_loc_sim[k_index]
            for moves in b_opts_sim:
                if k_loc in moves:
                    return True
    else: 
        if 'bKi' in b_pieces_sim:
            k_index = b_pieces_sim.index('bKi')
            k_loc = b_loc_sim[k_index]
            for moves in w_opts_sim:
                if k_loc in moves:
                    return True
    return False

#filters move that puts king in check
#if none for all pieces needs to state a win
def filter_check(moves, selection, turn):
    print("Test check moves in form: ", moves)
    legal_moves = []

    # Copy lists to avoid modifying the global game state
    fr_loc = w_loc if turn < 2 else b_loc
    fr_pieces = w_pieces if turn < 2 else b_pieces
    en_loc = b_loc if turn < 2 else w_loc
    en_pieces = b_pieces if turn < 2 else w_pieces

    original_pos = fr_loc[selection]

    for move in moves:
        print("Filter check move: ", move)
        #copy again to simulate
        fr_loc_sim = copy.deepcopy(fr_loc)
        fr_pieces_sim = copy.deepcopy(fr_pieces)
        en_loc_sim = copy.deepcopy(en_loc)
        en_pieces_sim = copy.deepcopy(en_pieces)

        #simulate the move
        fr_loc_sim[selection] = move

        #simulates removing piece if needed
        if move in en_loc_sim:
            en_index = en_loc_sim.index(move)
            en_loc_sim.pop(en_index)
            en_pieces_sim.pop(en_index)

        # Combine simulated versions of both players
        if turn < 2:
            w_loc_sim, w_pieces_sim = fr_loc_sim, fr_pieces_sim
            b_loc_sim, b_pieces_sim = en_loc_sim, en_pieces_sim
        else:
            b_loc_sim, b_pieces_sim = fr_loc_sim, fr_pieces_sim
            w_loc_sim, w_pieces_sim = en_loc_sim, en_pieces_sim

        #print("Black locations: ", b_loc_sim, "Black Pieces: ", b_pieces_sim)

        # Generate simulated move options for both players
        w_opts_sim = check_opts(w_pieces_sim, w_loc_sim, 'w', w_loc_sim, b_loc_sim)
        b_opts_sim = check_opts(b_pieces_sim, b_loc_sim, 'b', b_loc_sim, w_loc_sim)

        #test for check after moves
        if not test_check(turn, w_pieces_sim, w_loc_sim, b_pieces_sim, b_loc_sim, w_opts_sim, b_opts_sim):
            legal_moves.append(move)
    
    return legal_moves

#test for a checkmate
def checkmate_test(turn):
    #creates an array of possible moves
    poss_moves = []

    #turn will be 0 after black moved
    if turn == 0:
        pieces = w_pieces
        loc = w_loc
        print("Testing for white in checkmate: ", turn)
    else:
        pieces = b_pieces
        loc = b_loc
        print("Testing for black in checkmate: ", turn)

    for selection in range(len(pieces)):
        piece = [pieces[selection]]
        current_loc = [loc[selection]]
        moves = check_opts(piece, current_loc, turn)
        flat_moves = [move for sublist in moves for move in sublist]
        #print("moves:", sublist)
        legal_moves = filter_check(flat_moves, selection, turn)
        for i in range(len(legal_moves)):
            poss_moves.append(legal_moves[i])

    #print(poss_moves)  
    
    if not poss_moves:
        return True

    return False


#main game loop
#starts by getting all the options 
b_opts = check_opts(b_pieces, b_loc, 'b')
w_opts = check_opts(w_pieces, w_loc, 'w')

turn = 0

run = True
while run and game_over == False:
    board = draw_board()

    #asks for a board selection from player
    square = input("Enter square (e.g b5): ")
    try:
        letters = ["a","b","c","d","e","f","g","h"]
        if(1<=int(square[1])<=8):
            coords = (letters.index(square[0])+1,9-int(square[1]))
        else:
            raise ValueError
    except:
        print("Invalid square try again")
        continue

    if turn <= 1:
        #gets the piece on the square selected
        if coords in w_loc:
            selection = w_loc.index(coords)
            if turn == 0:
                turn = 1
                print("White selected: ", w_pieces[selection])

            if selection != 100:
                valid_moves = check_valid_moves()
                print("Valid moves in form: ", valid_moves)
                valid_moves = filter_check(valid_moves, selection, turn)
                draw_valid(valid_moves,board)
                if len(valid_moves) == 0:
                    print("No valid moves, try again")
                    continue
            
            #checks move coords in valid moves
            square = input("Enter valid square to move to: ")
            try:
                if(1<=int(square[1])<=8):
                    move_coords = (letters.index(square[0])+1,9-int(square[1]))
                else:
                    raise ValueError
            except:
                print("Invalid square try again")
                continue

            if move_coords in valid_moves:
                #adjusts location of piece
                w_loc[selection] = move_coords
                #check if its taking a black piece
                if move_coords in b_loc:
                    b_piece = b_loc.index(move_coords)
                    c_pieces_w.append(b_pieces[b_piece])
                    b_pieces.pop(b_piece)
                    b_loc.pop(b_piece)
                #updates the options for the pieces
                b_opts = check_opts(b_pieces, b_loc, 'b')
                w_opts = check_opts(w_pieces, w_loc, 'w')
                turn = 2
                print("White turn done")
                selection = 100
                valid_moves = []
                if checkmate_test(turn):
                    print("White wins")
                    winner = 'w'
            else:
                print("Not a valid move")
                continue

    if turn > 1:
        print("black turn")
        #gets the piece on the square selected
        if coords in b_loc:
            selection = b_loc.index(coords)
            if turn == 2:
                turn = 3
                print("Black selected: ", b_pieces[selection])

            if selection != 100:
                valid_moves = check_valid_moves()
                valid_moves = filter_check(valid_moves, selection, turn)
                draw_valid(valid_moves,board)
                if len(valid_moves) == 0:
                    print("No valid moves, try again")
                    continue
            
            #checks move coords in valid moves
            square = input("Enter valid square to move to: ")
            try:
                if(1<=int(square[1])<=8):
                    move_coords = (letters.index(square[0])+1,9-int(square[1]))
                else:
                    raise ValueError
            except:
                print("Invalid square try again")
                continue

            if move_coords in valid_moves:
                #adjusts location of piece
                b_loc[selection] = move_coords
                #check if its taking a black piece
                if move_coords in w_loc:
                    w_piece = w_loc.index(move_coords)
                    c_pieces_b.append(w_pieces[w_piece])
                    #checks if the piece taken was a king
                    if w_pieces[w_piece] == 'wKi':
                        winner = 'b'
                    w_pieces.pop(w_piece)
                    w_loc.pop(w_piece)
                #updates the options for the pieces
                b_opts = check_opts(b_pieces, b_loc, 'b')
                w_opts = check_opts(w_pieces, w_loc, 'w')
                turn = 0
                print("Black turn done")
                if checkmate_test(turn):
                    print("Black wins")
                    winner = 'b'
                selection = 100
                valid_moves = []
            else:
                print("Not a valid move")
                continue
    
    if winner != '':
        game_over = True
