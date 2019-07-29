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
#
# Jing Yang patterns: https://www.researchgate.net/publication/228970285_A_New_Solution_for_7x7_Hex_Game
# Hayward paper w/ patterns: https://webdocs.cs.ualberta.ca/~hayward/papers/yang7.pdf
#
# CLEANUP:
# 432 pattern (finding and replying)
# Certain patterns checking empty cells inefficient
#
# ISSUES
# 432 only represented in 4 cases
# Stealing priority positions
# Contracts don't really exist, finds all possible patterns even if some overlap which can cause problems
#
# Currently missing JY patterns 7,8

import numpy as np
import random
# cell states
UNOCCUPIED = 0
BLACK = 1
WHITE = 2

# representation of the game state
class HexBoard():
    # intialize board state to all cells unoccupied
    def __init__(self, board_dimension):
        self.substrategies = []
        self.board_dimension = board_dimension
        self.unoccupied = []
        self.move_list = []
        # Create the 2D array to keep track of the board position
        self.board_array = np.zeros((self.board_dimension, self.board_dimension), int)
        self.priority_list = ['c5', 'd3']
        # Populates a dictionary with an x,y key corresponding to a cell object
        self.board_dict = {}
        for x in range(self.board_dimension):
            for y in range(self.board_dimension):
                self.board_dict[(x,y)] = HexCell(x,y,self.board_dimension)
                self.unoccupied.append((x,y))
        
    def expand(self,pos1):
        # Neighbour search, used for DFS to find a winning path
        color = self.board_dict[pos1].get_state()
        append_list = []
        return_list = []
        # p_list contains the potential neighbouring cells with x,y relative to
        # the current position
        p_list = [(1,0),(0,1),(1,-1),(-1,1),(-1,0),(0,-1)]
        for p in p_list:
            # Find the new position (neighbour) and ensure it is within the
            # bounds of the board. If it is, add it to append_list since it is
            # a neighbour
            new_pos = (pos1[0]+p[0],pos1[1]+p[1])
            if new_pos[0] < self.board_dimension and new_pos[1] < self.board_dimension and new_pos[0] >= 0 and new_pos[1] >= 0:
                append_list.append(new_pos)
                
        # For all the neighbouring cells, add the ones that contain the same
        # colour cell as the original, then return those
        for pos in append_list:
            cell = self.board_dict[pos]
            if cell.get_state() == color:
                return_list.append(pos)
        return return_list

    # search for black wins
    def dfs_black(self):
        # Performs a DFS looking for a black win. Goes top to bottom on the board
        current_list = []
        drop_list = []
        
        # Check all cells in the first row, any that are black get added to the
        # current list
        for i in range(self.board_dimension):
            if self.board_dict[(i,0)].get_state() == 1:
                current_list.append((i,0))
                
        # Iterate until the current list has no more cells
        while current_list != []:
            for pos in current_list:
                # Add all neighbours with the same colour cell to the list
                current_list.extend(self.expand(pos))
                # Add the current cell to the list of cells we've already checked
                drop_list.append(pos)
                # Update the current list so it contains no cells that have 
                # already been checked
                current_list = list(set(current_list).difference(set(drop_list)))
                for pos1 in current_list:
                    # If any cell in the current list has reached the last row,
                    # then a winning path has been found, so return true
                    if pos1[1] == self.board_dimension - 1:
                        return True
            
        # No winning path was found, return false
        if len(current_list) == 0:
            return False
        
    
    def dfs_white(self):
        # Performs a DFS looking for a white win. Goes left to right on the board
        current_list = []
        drop_list = []
        for i in range(self.board_dimension):
            # For all the cells in the first column, if the cell contains a
            # white stone, add it to the current list
            if self.board_dict[(0,i)].get_state() == 2:
                current_list.append((0,i))
                
        # Iterate until the current list has no more cells left
        while current_list != []:
            for pos in current_list:
                # Find other positions connecting to the current cell with the
                # same colour
                current_list.extend(self.expand(pos))
                # Add current position to drop list to show it has been checked
                drop_list.append(pos)
                # Remove already checked cells from the current list
                current_list = list(set(current_list).difference(set(drop_list)))
                for pos1 in current_list:
                    if pos1[0] == self.board_dimension - 1:
                        # Have reached the end of the board with a path, so
                        # white has a winning path
                        return True
        
        # All items in the current list have been checked, no win exists for white
        if len(current_list) == 0:
            return False
        
    def detect_win(self):
        # Returns a 1 if black has won, a 2 if white has won, or a 0 if no one
        # has won
        if self.dfs_black():
            return 1
        elif self.dfs_white():
            return 2
        else:
            return 0
        
    def __repr__(self):
        # Returns a string representation of the board
        board = " a b c d e f g h\n"
        for row in range(self.board_dimension):
            board += (' '*row) + str(row+1)
            for col in self.board_array[row]:
                board += ' ' + str(col)
            board += '\n'
        return board
    
    def place_stone(self, x, y, state):
        # Places a stone with the given colour at a specific cell
        cell = self.board_dict[(x,y)]
        
        # Check the cell is valid to play in, if not return
        if cell.get_state() == UNOCCUPIED:                
            # Place a stone at the given x,y coordinate
            cell.set_state(state)
            self.board_array[y][x] = state
        else:
            print("Cell occupied, choose another cell")
            return
        
        #for pairs in self.find_432():
            #for move in pairs:
                #if move not in self.move_list:
                    #self.move_list.append(move)
            
        if (x,y) in self.unoccupied:
            self.unoccupied.remove((x,y))    
        if state == WHITE:
            x,y = self.search_strategies(x,y)
            try:
                self.place_stone(x,y,BLACK)
                # Remove any patterns that no longer exist
                self.substrategies = [pattern for pattern in self.substrategies if self.check_all_empty(self.change_pattern(pattern[0:len(pattern)-1]))]
                if len(self.substrategies) == 0:
                    self.find_substrategies()                
            except:
                coord = random.choice(self.unoccupied)
                x = coord[0]
                y = coord[1]
                self.place_stone(x,y,BLACK)
                    
    def find_substrategies(self):
        # Finds the sub-patterns within the board
        singles = self.find_single_patterns()
        adjacents = self.find_adjacent_patterns()
        self.substrategies = singles + adjacents
    
    def search_strategies(self, x,y):
        white_move = coord_2_pos(x,y)
        # Find the strategy (if it exists) that white played in, then make a
        # replying move in that substrategy
        for strat in self.substrategies:
            if white_move in strat:
                return self.get_move(strat, white_move)
                
        #if self.priority_list != [] and white_move not in self.priority_list:
            #move = self.priority_list.pop()
            #coord = pos_2_coord(move)
            #x = coord[0]
            #y = coord[1]
            #return x,y
        
        # White move did not threaten any strategies, so choose a random strategy
        # to play in
        if len(self.substrategies) != 0:
            strat = random.choice(self.substrategies)
            return self.get_move(strat, white_move)
        else:
            # No strategy, play randomly
            coord = random.choice(self.unoccupied)
            x = coord[0]
            y = coord[1]
        
        return x,y
    
    def get_move(self, strat, white_move):
        # Find the pattern white is threatening and reply
        # If there's time this function should be optimized
        pattern_id = strat[len(strat)-1]
        if pattern_id == 2: # Bridge is pattern 2
            move = self.reply_bridge(strat, white_move)
            return move
        elif pattern_id == 9:
            # Split option with 5 as the split
            move = self.reply_two_part(strat, white_move, 5)
        else:
            # Other options are all split options with a triangle,
            # only need to call the one function
            move = self.reply_two_part(strat, white_move)
            
        self.decompose_pattern(pattern_id, strat, move)
        return move
    
    def decompose_pattern(self, pattern_id, pattern, move):
        # Decomposes a specified pattern based on the move index into subgames.
        # Does not accomodate bridge or 432 as of right now. 
        # move is the black stone that gets placed
        if type(move) == tuple:
            move = coord_2_pos(move[0], move[1])
            
        # Remove the substrategy as it no longer exists
        self.substrategies.remove(pattern)
        index = pattern.index(move) # Get the index of the move
        if pattern_id == 3 or pattern_id == 6:
            # Double triangle, one bridge gets formed
            if index == 0:
                self.substrategies.append(pattern[1:3] + [2])
            else:
                self.substrategies.append(pattern[4:6] + [2])
                
        elif pattern_id == 4 or pattern_id == 5: # 432 pattern should be implemented here as well
            if index == 0:
                self.substrategies.append(pattern[1:3] + [2])
            else:
                self.substrategies.append(pattern[4:6] + [2])
                self.substrategies.append(pattern[6:8] + [2])
                
        elif pattern_id == 7:
            if index == 0:
                self.substrategies.append(pattern[1:3] + [2])
            else:
                self.substrategies.append(pattern[4:6] + [2])
                # Way of adding this pattern WILL need to be changed upon redoing 432 pattern
                self.substrategies.append(pattern[6:14] + [5])
                
        elif pattern_id == 9:
            if index == 0:
                self.substrategies.append(pattern[1:3] + [2])
                self.substrategies.append(pattern[3:5] + [2])
            else:
                self.substrategies.append(pattern[6:8] + [2])
                self.substrategies.append(pattern[8:10] + [2])
        return
    
    def find_single_patterns(self):
        # Finds all patterns that only require a single cell being black
        # coloured to work
        return_list = []
        for pos in self.board_dict:
            if self.board_dict[pos].get_state() == BLACK:
                # For all black coloured cells check if they make a known pattern
                return_list = self.find_bridge(1, pos, return_list)
                return_list = self.find_432(pos, return_list)
                return_list = self.find_jyp9(pos, return_list)
        
        return return_list
    
    def find_bridge(self, color, pos, return_list=[]):
        cell = self.board_dict[pos]
        # Find the bridges associated with that cell
        cell_bridges = cell.get_bridges()
        for cell_bridge in cell_bridges:
            # Get the other cell that gets bridged to
            cell_bridge = self.board_dict[cell_bridge]
            if cell_bridge.get_state() == color:
                # If the bridge cell is also the color we are looking for
                # and the cells between them are empty, add the cells
                # to the return list
                pairs = list(set(cell.get_neighbours()) & set(cell_bridge.get_neighbours()))
                if self.board_dict[pairs[0]].get_state() == UNOCCUPIED and self.board_dict[pairs[1]].get_state() == UNOCCUPIED:
                    return_list.append([coord_2_pos(pairs[0][0],pairs[0][1]),coord_2_pos(pairs[1][0],pairs[1][1])] + [2])
        
        # Find bridges that are edge bridges
        cell_nbrs = cell.get_neighbours()
        for nbr in cell_nbrs:
            if self.board_dict[nbr].get_state() == UNOCCUPIED:
                # Get the shared cells of the neighbour and cell
                bridge_cell = set(cell.get_neighbours()) & set(self.board_dict[nbr].get_neighbours())
                # Iterate through the shared cells
                for overlap_cell in bridge_cell:
                    if self.board_dict[overlap_cell].get_state() == UNOCCUPIED:
                        # If both cells are unoccupied and black edges, then a bridge exists between them
                        if self.board_dict[overlap_cell].is_black_edge() and self.board_dict[nbr].is_black_edge():
                            return_list.append([coord_2_pos(nbr[0],nbr[1]),coord_2_pos(overlap_cell[0],overlap_cell[1])] + [2])
                                    
        return return_list
    
    def find_432(self, pos, return_list):
        # Finds open 432 pattern positions and adds them to the return_list
        potential_patterns = self.board_dict[pos].get_432()
        
        for pattern in potential_patterns:
            cells_to_check = pattern[1:3] + pattern[6::]
            # Pattern must be fully empty and connected to exist
            if self.check_all_empty(pattern) and self.connected_ud_pattern(cells_to_check):
                pattern = self.change_pattern(list(pattern)) + [5]
                if pattern not in return_list:
                    return_list.append(pattern)
                    
        return return_list
    
    def find_adjacent_patterns(self):
        # Finds patterns that require two adjacent black coloured cells
        return_list = []
        for pos in self.board_dict:
            if self.board_dict[pos].get_state() != BLACK:
                continue
            
            x = pos[0]
            y = pos[1]
            # An adjacent cell must be black to have this pattern work
            adjacents = [(x-1,y), (x+1,y)]
            for coord in adjacents:
                # Check the coordinate exists in the board
                if coord[0] >= 0 and coord[0] < self.board_dimension:
                    if self.board_dict[coord].get_state() == BLACK:
                        # Two adjacent black cells exist
                        # Patterns with "jyp#" stands for Jing Yang Pattern # 
                        return_list = self.find_double_triangle(pos, coord, return_list)
                        return_list = self.find_jyp3(pos, return_list)
                        return_list = self.find_jyp4(pos, return_list)
                        
            # Next set of adjacents for patterns
            adjacents = [(x+1,y-1), (x-1,y+1), (x,y-1), (x,y+1)]
            for coord in adjacents:
                # Check coordinate exists on the board
                if coord[0] >= 0 and coord[0] < self.board_dimension and coord[1] >= 0 and coord[1] < self.board_dimension:
                    if self.board_dict[coord].get_state() == BLACK:
                        # Adjacent black cells exist here, check corresponding patterns
                        return_list = self.find_pattern7(pos, return_list, adjacents.index(coord)//2)
                        return_list = self.find_pattern8(pos, return_list, adjacents.index(coord)//2)
                        
        return return_list
    
    def find_jyp3(self, pos, return_list):
        # Finds the 3rd Jing Yang pattern
        potential_patterns = []
        # We'll choose to position based on the first given black cell
        x = pos[0]
        y = pos[1]
        if x >= 2 and y < self.board_dimension-2 and self.board_dict[(x, y+1)].get_state() == WHITE:
            # Pattern having a white stone here means could have a down pattern
            pattern = [(x-1,y+1), (x-2,y+2), (x-1,y+2), (x+1,y+1), (x,y+2), (x+1,y+2)]
            if self.check_all_empty(pattern):
                potential_patterns.append(pattern + [3])
        
        if x < self.board_dimension-2 and y > 1 and self.board_dict[(x+1, y-1)].get_state() == WHITE:
            # Pattern having a white stone here means could have an up pattern
            pattern = [(x,y-1), (x,y-2), (x+1,y-2), (x+2,y-1), (x+2,y-2), (x+3,y-2)]
            if self.check_all_empty(pattern):
                potential_patterns.append(pattern + [3])
        
        # Now need to check all the potential patterns are connected
        for pattern in potential_patterns:
            if self.connected_ud_pattern(pattern):
                pattern = self.change_pattern(pattern[0:len(pattern)-1]) + [pattern[len(pattern)-1]]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def find_jyp4(self, pos, return_list):
        # Finds the 4th Jing Yang pattern
        potential_patterns = []
        
        x = pos[0]
        y = pos[1]
        if x > 0 and x < self.board_dimension-2 and y < self.board_dimension-2 and \
           self.board_dict[(x,y+2)].get_state() == WHITE:
            # Need these conditions for the down-right version of this pattern
            potential_patterns.append([(x-1,y+2), (x-1,y+1), (x,y+1), (x+2,y+1), (x+2,y), (x+1,y+1), (x+1,y+2), (x+2,y+2)])
        
        if x > 2 and x < self.board_dimension-1 and y < self.board_dimension-2 and \
             self.board_dict[(x-1,y+2)].get_state() == WHITE:
            # Need these conditions for the down-left version of this pattern
            potential_patterns.append([(x,y+2), (x+1,y+1), (x,y+1), (x-2,y+1), (x-1,y), (x-1,y+1), (x-3,y+2), (x-2,y+2)])
                
        if x > 0 and x < self.board_dimension-2 and y > 1 and self.board_dict[(x+1,y-2)].get_state() == WHITE:
            # Need these conditions for the up-left version of this pattern
            potential_patterns.append([(x+2,y-2), (x+2,y-1), (x+1,y-1), (x-1,y-1), (x-1,y), (x,y-1), (x,y-2), (x-1,y-2)])
                
        if x < self.board_dimension-4 and y > 1 and self.board_dict[(x+2,y-2)].get_state() == WHITE:
            # Need these conditions for the up-right version of this pattern
            potential_patterns.append([(x+1,y-2), (x,y-1), (x+1,y-1), (x+3,y-1), (x+2,y), (x+2,y-1), (x+3,y-2), (x+4,y-2)])
        
        # Any potential patterns that are fully connected up/down depending on
        # the pattern get added to the return list
        for pattern in potential_patterns:
            cells_to_be_checked = [pattern[0]] + pattern[6::]
            # Check cells are empty and connected
            if self.check_all_empty(pattern) and self.connected_ud_pattern(cells_to_be_checked):
                pattern = self.change_pattern(pattern) + [4]
                if pattern not in return_list:
                    return_list.append(pattern)
            
        return return_list
    
    def find_double_triangle(self, pos1, pos2, return_list):
        # Finds 6 open spots by 2 adjacent black coloured cells
        # pos and coord are the 2 adjacent cells that are black coloured
        potential_patterns = []

        # Find the minimum x position to begin generating patterns
        if pos1[0] < pos2[0]:
            min_x_pos = pos1
        else:
            min_x_pos = pos2
            
        x = min_x_pos[0]
        y = min_x_pos[1]
        if x > 0 and y < self.board_dimension-2:
            # Can have a down six pattern
            pattern = [(x-1,y+2), (x-1,y+1), (x,y+1), (x+1,y+1), (x,y+2), (x+1,y+2)]
            empty = self.check_all_empty(pattern)
            if empty:
                potential_patterns.append(pattern + [6])
                
        if x + 1 < self.board_dimension-1 and y > 1:
            # Can have an up six pattern
            pattern = [(x+2,y-2), (x+2,y-1), (x+1,y-1), (x,y-1), (x+1,y-2), (x,y-2)]
            empty = self.check_all_empty(pattern)
            if empty:
                potential_patterns.append(pattern + [6])
                                
        # Lastly need to check the potential sixes connect two sides
        for pattern in potential_patterns:
            if self.connected_ud_pattern(pattern):
                pattern = self.change_pattern(pattern[0:len(pattern)-1]) + [pattern[len(pattern)-1]]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def find_pattern7(self, pos, return_list, case):
        # Finds "Local Pattern 5" in the Hayward document (see comments at start
        # for link). Use number 7 since 5 is already 432 pattern
        # Case determines the way the adjacent cells are
        potential_patterns = []
        x = pos[0]
        y = pos[1]
        
        if case == 0:
            if x > 2 and x < self.board_dimension-2 and y < self.board_dimension-3 and \
               self.board_dict[(x-1,y+2)].get_state() == WHITE:
                # Need these conditions to form a down-right 7 pattern
                potential_patterns.append([(x-2,y+2), (x-3,y+3), (x-2,y+3), (x+1,y+1), (x+1,y),\
                                           (x,y+1), (x,y+2), (x-1,y+3), (x,y+3), (x+2,y+2),\
                                           (x+2,y+1), (x+1,y+2), (x+1,y+3), (x+2,y+3)])
                
            if x > 1 and x < self.board_dimension-3 and y > 2 and self.board_dict[(x+1,y-2)].get_state() == WHITE:
                # Need these conditions to form an up-left 7 pattern
                potential_patterns.append([(x+2,y-2), (x+3,y-3), (x+2,y-3), (x-1,y-1), (x-1,y),\
                                           (x,y-1), (x,y-2), (x+1,y-3), (x,y-3), (x-2,y-2),\
                                           (x-2,y-1), (x-1,y-2), (x-1,y-3), (x-2,y-3)])
                
        else:
            if x < self.board_dimension-5 and y > 2 and self.board_dict[(x+1,y-2)].get_state() == WHITE:
                # Need these conditions to form an up-right 7 pattern
                potential_patterns.append([(x,y-2), (x,y-3), (x+1,y-3), (x+2,y-1), (x+1,y),\
                                           (x+1,y-1), (x+2,y-2), (x+2,y-3), (x+3,y-3), (x+4,y-2),\
                                           (x+3,y-1), (x+3,y-2), (x+4,y-3), (x+5,y-3)])
                
            if x > 4 and y < self.board_dimension-3 and self.board_dict[(x-1,y+2)].get_state() == WHITE:
                # Need these conditions to form a down-left 7 pattern
                potential_patterns.append([(x,y+2), (x,y+3), (x-1,y+3), (x-2,y+1), (x-1,y),\
                                           (x-1,y+1), (x-2,y+2), (x-2,y+3), (x-3,y+3), (x-4,y+2),\
                                           (x-3,y+1), (x-3,y+2), (x-4,y+3), (x-5,y+3)])
            
        # Now need to check each potential pattern is empty and connects as expected
        for pattern in potential_patterns:
            cells_to_check = pattern[1:3] + pattern[7:9] + pattern[12::]
            if self.check_all_empty(pattern) and self.connected_ud_pattern(cells_to_check):
                pattern = self.change_pattern(pattern) + [7]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def find_pattern8(self, pos, return_list, case):
        # Finds "Local Pattern 4" in the Hayward document (see comments at start
        # for link). Use number 8 since 4 is already a pattern
        potential_patterns = []
        x = pos[0]
        y = pos[1]
        
        if case == 0:
            if x > 1 and x < self.board_dimension-2 and y < self.board_dimension-3 and \
               self.board_dict[(x-2,y+2)].get_state() == WHITE:
                # Can have a down-right 8 pattern
                potential_patterns.append([(x+1,y), (x,y+1), (x+1,y+1), (x+2,y+1), (x-1,y+2),\
                                           (x,y+2), (x+1,y+2), (x+2,y+2), (x-2,y+3),\
                                           (x-1,y+3), (x,y+3), (x+1,y+3), (x+2,y+3)])
            
            if x > 1 and x < self.board_dimension-2 and y > 2 and self.board_dict[(x+2,y-2)].get_state() == WHITE:
                # Can have an up-left 8 pattern
                potential_patterns.append([(x-1,y), (x,y-1), (x-1,y-1), (x-2,y-1), (x+1,y-2),\
                                           (x,y-2), (x-1,y-2), (x-2,y-2), (x+2,y-3),\
                                           (x+1,y-3), (x,y-3), (x-1,y-3), (x-2,y-3)])
        else:
            if x > 4 and y < self.board_dimension-3 and self.board_dict[(x,y+2)].get_state() == WHITE:
                # Need these conditions for a down-left 8 pattern
                potential_patterns.append([(x-1,y), (x-1,y+1), (x-2,y+1), (x-3,y+1), (x-1,y+2),\
                                           (x-2,y+2), (x-3,y+2), (x-4,y+2), (x-1,y+3),\
                                           (x-2,y+3), (x-3,y+3), (x-4,y+3), (x-5,y+3)])
                
            if x < self.board_dimension-5 and y > 2 and self.board_dict[(x,y-2)].get_state() == WHITE:
                # Need these conditions for an up-right 8 pattern
                potential_patterns.append([(x+1,y), (x+1,y-1), (x+2,y-1), (x+3,y-1), (x+1,y-2),\
                                           (x+2,y-2), (x+3,y-2), (x+4,y-2), (x+1,y-3),\
                                           (x+2,y-3), (x+3,y-3), (x+4,y-3), (x+5,y-3)])
            
        # Check each pattern to see if it is empty and connected
        for pattern in potential_patterns:
            cells_to_check = pattern[8::]
            if self.check_all_empty(pattern) and self.connected_ud_pattern(cells_to_check):
                pattern = self.change_pattern(pattern) + [8]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def find_jyp9(self, pos, return_list):
        # Finds the 9th Jing Yang pattern
        potential_patterns = []
        
        x = pos[0]
        y = pos[1]
        if x > 2 and x < self.board_dimension-1 and y < self.board_dimension-2 and \
           self.board_dict[(x-1,y+2)].get_state() == WHITE:
            # Need these conditions to form a down 9 pattern
            potential_patterns.append([(x-2,y+1), (x-1,y), (x-1,y+1), (x-3,y+2), (x-2,y+2),\
                                       (x+1,y+1), (x+1,y), (x,y+1), (x,y+2), (x+1,y+2)])
            
        if x > 0 and x < self.board_dimension-3 and y > 1 and self.board_dict[(x+1,y-2)].get_state() == WHITE:
            # Need these conditions to form an up 9 pattern
            potential_patterns.append([(x-1,y-1), (x-1,y), (x,y-1), (x,y-2), (x-1,y-2),\
                                       (x+2,y-1), (x+1,y), (x+1,y-1), (x+2,y-2), (x+3,y-2)])
            
        # Check that each pattern only has empty cells and is connected
        for pattern in potential_patterns:
            # Cells to be checked to ensure the pattern connects
            cells_to_check = pattern[3:5] + pattern[8::]
            if self.check_all_empty(pattern) and self.connected_ud_pattern(cells_to_check):
                pattern = self.change_pattern(pattern) + [9]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def connected_ud_pattern(self, pattern):
        # Determines if all cells in potential patterns are connected up or down
        # Important to note this function does not allow side (same y) connections
        all_connected = True
        # Don't include the last element since it just identifies the pattern
        for cell in pattern[0:len(pattern)-1]:
            if self.board_dict[cell].is_black_edge():
                continue
            else:
                nbrs = self.board_dict[cell].get_neighbours()
                nbrs = [nbr for nbr in nbrs if not nbr[1] == cell[1]]
                # Check the neighbour is connected above or below
                connected = False
                for nbr in nbrs:
                    if self.board_dict[nbr].get_state() == BLACK:
                        connected = True
                        break
                
                if not connected:
                    all_connected = False
                    
        # If all the cells connect up or down the pattern exists
        if all_connected:
            return True
        else:
            return False
    
    def check_all_empty(self, cells_to_check):
        # Takes a list of cells and checks that each cell is unoccupied
        # cells_to_check should be in coordinate form, not position
        for cell in cells_to_check:
            if self.board_dict[cell].get_state() != UNOCCUPIED:
                # Cell is taken, all cells are not empty
                return False
            
        return True
    
    def reply_bridge(self, pattern, white_move):
        # Finds the replying move when a bridge has been threatened
        if white_move in pattern:
            self.substrategies.remove(pattern)
            # Remove the white move so black can take the other cell
            pattern.remove(white_move)
        # Return the replying move
        return pos_2_coord(pattern[0])
        
    def reply_two_part(self, pattern, white_move, split=3):
        # This function takes a pattern that can be broken into two parts, where
        # if played in one part the replying move is in the other part. The
        # replying moves are at the start of the split in each case
        part1 = pattern[0:split]
        part2 = pattern[split::]
        
        if white_move in part1:
            return pos_2_coord(part2[0])
        else:
            return pos_2_coord(part1[0])
    
    def change_pattern(self, pattern):
        if type(pattern[0]) == str:
            # Converts a pattern from a list of positions to a list of coordinates
            for i in range(len(pattern)):
                pattern[i] = pos_2_coord(pattern[i])
                
        else:
            # Converts a pattern from a list of coordinates to a list of positions
            for i in range(len(pattern)):
                pattern[i] = coord_2_pos(pattern[i][0], pattern[i][1])
        return pattern

# representation of individual board cells
class HexCell():
    # initialize cell position and state
    # states: 0 - unoccupied, 1 - black occupied, 2 - white occupied
    def __init__(self, x, y, board_dimension, state=UNOCCUPIED):
        
        self.x = x
        self.y = y
        # State is black, white, or unoccupied
        self.state = state
        self.board_dimension = board_dimension

        # BLACK_EDGE is true if the cell is either the first or last row
        self.BLACK_EDGE = False
        # WHITE_EDGE is true if the cell is either the first or last column
        self.WHITE_EDGE = False
        if self.x == 0 or self.x == self.board_dimension-1:
            self.WHITE_EDGE = True
        if self.y == 0 or self.y == self.board_dimension-1:
            self.BLACK_EDGE = True
            
        # Keeps track of 3 of the cells neighbours
        self.neighbours = [(x+1,y), (x+1,y-1), (x,y+1), (x,y-1), (x-1,y),(x-1,y+1)]
        self.neighbours = [coord for coord in self.neighbours if not \
                           (coord[0] < 0 or coord[0] >= self.board_dimension or coord[1] < 0 or coord[1] >= self.board_dimension)]

        self.bridges = [(x+1,y+1), (x-1,y+2), (x-2,y+1)]
        self.bridges = [coord for coord in self.bridges if not \
                           (coord[0] < 0 or coord[0] >= self.board_dimension or coord[1] < 0 or coord[1] >= self.board_dimension)]
        
        self.four32 = self.generate_432_patterns(x,y)
        
    def set_state(self, state):
        self.state = state
        
    def get_neighbours(self):
        return self.neighbours
    
    def get_bridges(self):
        return self.bridges
    
    def get_432(self):
        return self.four32
    
    def get_state(self):
        return self.state
    
    def is_black_edge(self):
        return self.BLACK_EDGE
    
    def generate_432_patterns(self, x, y):
        # Generates top to bottom 432 patterns
        four32 = [[(x-1,y+1),(x-2,y+2),(x-1,y+2), (x+1,y+1),(x+1,y),(x,y+1),(x,y+2),(x+1,y+2)],\
                  [(x,y+1),(x,y+2),(x-1,y+2), (x-2,y+1),(x-1,y),(x-1,y+1),(x-3,y+2),(x-2,y+2)],\
                  [(x,y-1),(x,y-2),(x+1,y-2), (x+2,y-1),(x+1,y),(x+1,y-1),(x+2,y-2),(x+3,y-2)],\
                  [(x+1,y-1),(x+1,y-2),(x+2,y-2), (x-1,y-1),(x-1,y),(x,y-1),(x-1,y-2),(x,y-2)]]
        
        # Goes through the four32 array and removes any patterns that have invalid
        # coordinates contained in them
        rm_list = []            
        for pattern in four32:
            new_pattern = [coord for coord in pattern if not \
                       (coord[0] < 0 or coord[0] >= self.board_dimension or coord[1] < 0 or coord[1] >= self.board_dimension)]            
            if len(new_pattern) < 8:
                # One coordinate was invalid, entire pattern does not work now
                rm_list.append(pattern)
        while len(rm_list) > 0:
            # Remove the pattern
            four32.remove(rm_list[0])
            rm_list.remove(rm_list[0])
        
        return four32
    
    def __repr__(self):
        # Represent in board coordinate form
        return coord_2_pos(self.x,self.y)
    
def coord_2_pos(x,y):
    # Changes a coordinate into board coordinate form
    pos_dict = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    x = pos_dict[x]
    y = str(y+1)
    return x + y

def pos_2_coord(pos):
    # Changes a board coordinate into normal coordinates
    pos_dict = {"a": 0, "b": 1, "c": 2, "d": 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    x = pos_dict[pos[0]]
    y = pos[1]
    return (int(x), int(y)-1)
