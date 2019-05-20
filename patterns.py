# Outline
#
# THE GAME - pattern representations
# 1. Name
# 2. Position
# 3. Contract
# 4. Strategy
# 
# THE PLAYER - interface
# 1. initialize the board
# G <--- Empty 3x3 board
# Stack <--- { G }
# 
# 2. black first move (computer)
# pop G from stack
# add play(G,x) to the stack, where x is any given cell (we will place on the main diagonal)
# while stack is not empty do:
#       get opponent's move x
#       if pattern exists in G in S:
#           pop G from stack
#           add play(G,x) to stack
#       else:
#           pop any G from stack
#           add play(G,0)
#
# PATTERNS
# 
# Bridge
# Position:
#       a b
#      1 x .
#       2 . x
# Contract: create path (a1, x, b2) where x = a2 OR b1
# Strategy: if white plays b1 - black plays a2
#           else if white plays a2 - black plays b1
#           else play a2 OR b1
# Notes: consider generalizing the bridge pattern to the top/bottom, where a cell is paired to 
#       an edge cell
#
# Pair
# Position:
#       a b c
#      1 . . .
#       2 . x .
#        3 . . .      
# Contract: create pair (a1, b2) OR (b2, c3)
# Strategy: if white plays a1 - black plays c3   
#           else if white plays c3 - black plays a1
#           else play a1 OR c3

import numpy as np

# cell states
UNOCCUPIED = 0
BLACK = 1
WHITE = 2

# representation of the game state
class HexBoard():
    # intialize board state to all cells unoccupied
    def __init__(self, board_dimension):
        self.board_dimension = board_dimension
        
        # Create the 2D array to keep track of the board position
        self.board_array = np.zeros((self.board_dimension, self.board_dimension), int)
        
        # TODO: data structure housing all the cells and the coordinates they are mapped to
        self.board_dict = {}
        for x in range(self.board_dimension):
            for y in range(self.board_dimension):
                self.board_dict[(x,y)] = HexCell(x,y)
        
        # TODO: representation of board edges (top/bottom and left/right win conditions)
    def expand(self,pos1):
        color = self.board_dict[pos1].state
        #print(color)
        append_list = []
        return_list = []
        p_list = [(1,0),(0,1),(1,-1),(-1,1),(-1,0),(0,-1)]
        for p in p_list:
            new_pos = (pos1[0]+p[0],pos1[1]+p[1])
            if new_pos[0] < self.board_dimension and new_pos[1] < self.board_dimension and new_pos[0] >= 0 and new_pos[1] >= 0:
                append_list.append(new_pos)
        for pos in append_list:
            cell = self.board_dict[pos]
            if cell.state == color:
                return_list.append(pos)
        return return_list
    def dfs_black(self):
        current_list = []
        drop_list = []
        for i in range(self.board_dimension):
            if self.board_dict[(i,0)].state == 1:
                current_list.append((i,0))
        while current_list != []:
            for pos in current_list:
                print(current_list)
                current_list.extend(self.expand(pos))
                drop_list.append(pos)
                current_list = list(set(current_list).difference(set(drop_list)))
                for pos1 in current_list:
                    if pos1[1] == self.board_dimension - 1:
                        return True
            #print(current_list)
        if len(current_list) == 0:
            return False
    def dfs_white(self):
        current_list = []
        drop_list = []
        for i in range(self.board_dimension):
            if self.board_dict[(0,i)].state == 2:
                current_list.append((0,i))
        while current_list != []:
            for pos in current_list:
                print(current_list)
                current_list.extend(self.expand(pos))
                drop_list.append(pos)
                current_list = list(set(current_list).difference(set(drop_list)))
                for pos1 in current_list:
                    if pos1[0] == self.board_dimension - 1:
                        return True
        if len(current_list) == 0:
            return False
    def detect_win(self):
        if self.dfs_black():
            return "Black wins"
        elif self.dfs_white():
            return "White wins"
        else:
            return "Nobody wins"
    # TODO: printable board representation
    def __repr__(self):
        board = " a b c\n"
        for row in range(self.board_dimension):
            board += (' '*row) + str(row+1)
            for col in self.board_array[row]:
                board += ' ' + str(col)
            board += '\n'
            
        return board
    
    # TODO: methods for starting the game (black first move along main diagonal)
    # TODO: methods for player interface for cell placement
    def place_stone(self, x, y, state):
        # Place a stone at the given x,y coordinate
        self.board_array[y][x] = state
        cell = self.board_dict[(x,y)]
        cell.set_state(state)
    
    # TODO: methods for pattern recognition based on board state (bridge, pair, adjacent)

# representation of individual board cells
class HexCell():
    # initialize cell position and state
    # states: 0 - unoccupied, 1 - black occupied, 2 - white occupied
    def __init__(self, x, y, state=UNOCCUPIED):
        self.x = x
        self.y = y
        self.state = state
        
    def set_state(self, state):
        self.state = state

    def __repr__(self):
        # Not sure how we want this represented
        return str(self.y*3+self.x)