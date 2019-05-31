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
    
    def __repr__(self):
        board_visual = ""
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