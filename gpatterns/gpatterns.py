import string

# cell states
UNOCCUPIED = "."
BLACK = "X"
WHITE = "O"

# class representation of the game board state
class HexBoard():
    # initialize board state to all cells unoccupied and wait for first move
    def __init__(self, board_dimension):
        self.board_dimension = board_dimension

        # two-dimensional array of board state for visual representation
        self.game_board = [[UNOCCUPIED for column in range(board_dimension)]
                            for row in range(board_dimension)]
        
        # ownership containers
        self.black_stones = {}
        self.white_stones = {}
        self.unoccupied = {}
        
        # initialize all board cells to unoccupied
        for x in range(self.board_dimension):
            for y in range(self.board_dimension):
                self.unoccupied[(x,y)] = HexCell(x,y)
        
        self.white_response = (0,0)
        self.responses = {}
    
    # prints out current board state to the terminal 
    def __repr__(self):
        board_visual = "\n"
        spacing = " "
        row_increment = 0

        # generate alphabetical (horizontal) coordinates
        for coordinate in range(self.board_dimension):
            board_visual += string.ascii_lowercase[coordinate] + spacing
        board_visual += '\n'
        
        # add each row to the representation with a leading numerical (vertical) coordiante
        for row in self.game_board:
            # single digit coordinate spacing
            if row_increment < 9:
                board_visual += row_increment*spacing + str(row_increment+1)
            # double digit coordinate spacing
            else:
                board_visual += (row_increment-1)*spacing + str(row_increment+1)
            # board_visual += row_increment * spacing
            for column in row:
                board_visual += spacing + column
            board_visual += '\n'
            row_increment += 1
        return board_visual
    
    # places white/black stone at designated coordinates and updates board position
    def place_stone(self, x, y, player):
        self.game_board[y][x] = player
        stone = self.unoccupied.pop((x,y))
        if player == WHITE:
            self.white_stones[(x,y)] = stone
        elif player == BLACK:
            self.black_stones[(x,y)] = stone
        
        print("WHITE STONES: ", self.white_stones)
        print("BLACK STONES: ", self.black_stones)
        print("UNOCCUPIED: ", self.unoccupied)
        return
    
    def get_next_move(self):
        # move input as <PLAYER> <LETTER><NUMBER>
        # e.g. to play white a3: w a3
        # note: the horizontal coordinates will be zero indexed on input (ascii letters), but
        # the vertical coordinates will not, hence -1 in the y parameter for place_stone
        user_input = input()
        # play white stone
        if user_input[0] == 'w':
            self.place_stone(string.ascii_lowercase.index(user_input[2]), int(user_input[3:])-1, WHITE)
            self.white_response = (string.ascii_lowercase.index(user_input[2]), int(user_input[3:])-1)
            print(self.white_response)
            if self.white_response in self.responses.keys():
                print("BLACK RESPONSE TO WHITE: ", string.ascii_lowercase[self.responses[self.white_response][0]], self.responses[self.white_response][1]+1)
        # play black stone
        elif user_input[0] == 'b':
            self.place_stone(string.ascii_lowercase.index(user_input[2]), int(user_input[3:])-1, BLACK)
        return
    
    def find_pseudobridge(self, player):
        if player == BLACK:
            for cell in self.black_stones.values():
                if (cell.x-1,cell.y+1) in self.unoccupied.keys() and (cell.x,cell.y+1) in self.unoccupied.keys():
                    print("BOTTOM VC EXISTS")
                    # insert strategy into responses
                    # white plays bottom left VC
                    self.responses[cell.x-1,cell.y+1] = (cell.x,cell.y+1)
                    # white plays bottom right VC
                    self.responses[cell.x,cell.y+1] = (cell.x-1, cell.y+1)
                if (cell.x,cell.y-1) in self.unoccupied.keys() and (cell.x+1,cell.y-1) in self.unoccupied.keys():
                    # insert strategy into responses
                    # white plays top left VC
                    self.responses[cell.x,cell.y-1] = (cell.x+1,cell.y-1)
                    # white plays top right VC
                    self.responses[cell.x+1,cell.y-1] = (cell.x,cell.y-1)
                    print("TOP VC EXISTS")
        return
    
    def search_strategies(self, player):
        self.responses.clear()
        self.find_pseudobridge(player)
        if player == BLACK:
            print("BLACK STRATEGIES: ", self.responses)
        return

class HexCell():
    # initialize cell with coordinates and ownership
    def __init__(self, x, y, owner=UNOCCUPIED):
        self.x = x
        self.y = y
        self.owner = owner
    
    def __repr__(self):
        return 'HexCell(%s%s)' % (string.ascii_lowercase[self.x], self.y+1)
