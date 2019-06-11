import string

# cell states for board visualization
UNOCCUPIED = "."
BLACK = "X"
WHITE = "O"

class HexBoard():
    """Class representation of the game board state

    Attributes:
        board_dimension (int): n x n board size 
        game_board (list): two-dimensional array representation of board state
        black_stones (dict): relational container for all black stones
        white_stones (dict): relational container for all white stones
        unoccupied (dict): relational container for all unoccupied cells
        responses (dict): black strategies in response to white placements
    """
    def __init__(self, board_dimension, black_opening):
        """Initializes board and plays the opening move for black

        Arguments:
            board_dimension (int): n x n board size
            black_opening (str): opening move for black
        """
        self.board_dimension = board_dimension

        # intialize empty board
        self.game_board = self.generate_empty_board()

        # ownership containers
        self.black_stones = {}
        self.white_stones = {}
        self.unoccupied = {}

        # initialize all board cells as unoccupied and populate the unoccupied container
        self.initialize_board_cells()

        # black strategies updated for every pattern analysis following black placement
        self.responses = {}
        self.white_move = None

        # black opening move and pattern analysis
        self.black_opening_move(black_opening)
        self.find_patterns()
    
    def __repr__(self):
        return self.board_visualization()

    def board_visualization(self):
        """Constructs string visualization of current board position
        """
        board_visual = "\n"
        spacing = " "
        row_increment = 0

        # generate alphabetical (column) coordinates
        board_visual += spacing
        for coordinate in range(self.board_dimension):
            board_visual += string.ascii_lowercase[coordinate] + spacing
        board_visual += "\n"
        
        # add each row to the visual with a leading numerical (row) coordinate
        for row in self.game_board:
            # single digit coordinate spacing
            if row_increment < 9:
                board_visual += row_increment*spacing + str(row_increment+1)
            # double digit coordinate spacing
            else:
                board_visual += (row_increment-1)*spacing + str(row_increment+1)
            for column in row:
                board_visual += spacing + column
            board_visual += "\n"
            row_increment += 1
        return board_visual
        
    def generate_empty_board(self):
        """Initializes two-dimensional array representation of the game board
        e.g. [[row_1], [row_2], ... ]
        """
        return [[UNOCCUPIED for column in range(self.board_dimension)]
                    for row in range(self.board_dimension)]
    
    def initialize_board_cells(self):
        """Initializes all HexBoard HexCells to unoccupied
        """
        for column in range(self.board_dimension):
            for row in range(self.board_dimension):
                self.unoccupied[(column,row)] = HexCell(column,row)
    
    def place_stone(self, x, y, owner):
        """Places a stone at the designated coordinates for the given player
        
        Arguments:
            x (int): 0-indexed column position
            y (int): 0-indexed row position
            owner (str): one of the globals - BLACK/WHITE
        """
        assert (owner != UNOCCUPIED), "Must play Black or White"
        assert (x >= 0 and x < self.board_dimension), "Column out of range"
        assert (y >= 0 and y < self.board_dimension), "Row out of range"

        self.game_board[y][x] = owner
        stone = self.unoccupied.pop((x,y))
        if owner == WHITE:
            self.white_stones[(x,y)] = stone
        elif owner == BLACK:
            self.black_stones[(x,y)] = stone
        return
    
    def get_player_move(self):
        """Prompts user for white stone placement in standard coordinate notation
        e.g. a1, b5, etc.
        """
        user_input = input("White to move: ")
        x, y = self.zero_coordinates(user_input)
        self.white_move = (x,y)
        self.place_stone(x, y, WHITE)
        return
    
    def black_opening_move(self, opening_move):
        """Places stone for black's opening move

        Arguments:
            opening_move (str): black opening move in standard notation (e.g. a1)
        """
        x, y = self.zero_coordinates(opening_move)
        self.place_stone(x, y, BLACK)
        self.find_patterns()
        return
    
    def find_patterns(self):
        """Populates responses following black move based on current board patterns
        """
        self.responses.clear()
        self.find_pseudobridge()
        return
    
    def black_response(self):
        """Makes next move for black in respect to developed pattern strategies
        """
        # check if white has placed
        if self.white_move != None:
            black_move = self.responses[(self.white_move[0],self.white_move[1])]
            self.place_stone(black_move[0], black_move[1], BLACK)
    
    def black_turn(self):
        """Driver for all the functions to run during black's turn
        """
        self.black_response()
        self.find_patterns()
        return

    def find_pseudobridge(self):
        """Searches black positions for VC to the top/bottom of the board
        """
        for stone in self.black_stones.values():
            # bottom VC
            # check if in second to last row and for the open VC
            if ((stone.x == self.board_dimension-2) and
                (stone.x-1,stone.y+1) in self.unoccupied.keys() and
                (stone.x,stone.y+1) in self.unoccupied.keys()):
                # insert bottom VC strategy into responses
                # white plays bottom left VC
                self.responses[(stone.x-1,stone.y+1)] = (stone.x,stone.y+1)
                # white plays bottom right VC
                self.responses[(stone.x,stone.y+1)] = (stone.x-1, stone.y+1)
            # top VC
            # check if in second row and for open VC
            if ((stone.x == 1) and
                (stone.x,stone.y-1) in self.unoccupied.keys() and
                (stone.x+1,stone.y-1) in self.unoccupied.keys()):
                # insert top VC strategy into responses
                # white plays top left VC
                self.responses[(stone.x,stone.y-1)] = (stone.x+1,stone.y-1)
                # white plays top right VC
                self.responses[(stone.x+1,stone.y-1)] = (stone.x,stone.y-1)
        return
    
    @staticmethod
    def zero_coordinates(standard_coordinates):
        """Converts standard hex coordinate notation to zero-indexed x/y pair
        """
        # parse the column coordinate (alphacharacter) as a 0-index coordiante
        x = string.ascii_lowercase.index(standard_coordinates[0])
        # parse the row coordinate as a 0-index coordinate
        y = int(standard_coordinates[1:]) - 1
        return x, y
    
    @staticmethod
    def standard_coordinates(x, y):
        """Converts zero-index coordinates to standard hex coordinate notation
        """
        column = string.ascii_lowercase[x]
        row = str(y+1)
        return column+row

class HexCell():
    """Class representation of an individual HexBoard Cell
    """
    def __init__(self, column, row, owner=UNOCCUPIED):
        self.x = column
        self.y = row
        self.owner = owner
