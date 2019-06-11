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
    """
    def __init__(self, board_dimension):
        self.board_dimension = board_dimension

        # intialize empty board
        self.game_board = self.generate_empty_board()

        # ownership containers
        self.black_stones = {}
        self.white_stones = {}
        self.unoccupied = {}

        # initialize all board cells as unoccupied and populate the unoccupied container
        self.initialize_board_cells()
    
    def __repr__(self):
        return self.board_visualization()

    def board_visualization(self):
        board_visual = "\n"
        spacing = " "
        row_increment = 0

        # generate alphabetical (column) coordinates
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
        return [[UNOCCUPIED for column in range(self.board_dimension)]
                    for row in range(self.board_dimension)]
    
    def initialize_board_cells(self):
        for column in range(self.board_dimension):
            for row in range(self.board_dimension):
                self.unoccupied[(column,row)] = HexCell(column,row)
                

class HexCell():
    """Class representation of an individual HexBoard Cell
    """
    def __init__(self, column, row, owner=UNOCCUPIED):
        self.x = column
        self.y = row
        self.owner = owner
