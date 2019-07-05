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
#
# ISSUES
# 432 only represented in 4 cases
# Stealing priority positions

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
        # TODO: representation of board edges (top/bottom and left/right win conditions)
        
    def expand(self,pos1):
        # Neighbour search, used for DFS to find a winning path
        color = self.board_dict[pos1].state
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
            if cell.state == color:
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
            if self.board_dict[(i,0)].state == 1:
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
            if self.board_dict[(0,i)].state == 2:
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
    
    # TODO: methods for starting the game (black first move along main diagonal)
    # TODO: methods for player interface for cell placement
    def place_stone(self, x, y, state):
        cell = self.board_dict[(x,y)]
        # Check the cell is valid to play in, if not return
        if cell.state == UNOCCUPIED:
            # Place a stone at the given x,y coordinate
            substrategies = self.find_substrategies()
            cell.set_state(state)
            self.board_array[y][x] = state
        else:
            print("Cell occupied, choose another cell")
            return
        
        for pairs in self.find_432():
            for move in pairs:
                if move not in self.move_list:
                    self.move_list.append(move)
            
        if (x,y) in self.unoccupied:
            self.unoccupied.remove((x,y))    
        if state == WHITE:
            x,y = self.search_strategies(x,y,substrategies)
            try:
                self.place_stone(x,y,BLACK)
            except:
                coord = random.choice(self.unoccupied)
                x = coord[0]
                y = coord[1]
                self.place_stone(x,y,BLACK)
                    
    def find_substrategies(self):
        bridges = self.find_bridge(1)
        four32s = self.find_432()
        adjacents = self.find_adjacent_patterns()
        return bridges + adjacents + four32s
    
    def search_strategies(self, x,y, substrategies):
        white_move = coord_2_pos(x,y)
        # Find the strategy (if it exists) that white played in, then make a
        # replying move in that substrategy
        for strat in substrategies:
            if white_move in strat:
                return self.get_move(strat, white_move)
                
        if self.priority_list != [] and white_move not in self.priority_list:
            move = self.priority_list.pop()
            coord = pos_2_coord(move)
            x = coord[0]
            y = coord[1]
            return x,y
        
        # White move did not threaten any strategies, so choose a random strategy
        # to play in
        if substrategies != []:
            strat = random.choice(substrategies)
            return self.get_move(strat, white_move)
        else:
            # No strategy, play randomly
            coord = random.choice(self.unoccupied)
            x = coord[0]
            y = coord[1]
        
        return x,y
    
    def get_move(self, strat, white_move):
        # Find the pattern white is threatening and reply
        if strat[len(strat)-1] == 2: # Bridge is pattern 2
            move = self.reply_bridge(strat[0:len(strat)-1], white_move)
        elif strat[len(strat)-1] == 5: # 432 strategy
            # Only other option is the 432 strategy
            black_pos = strat[len(strat)-2]
            move = self.reply432(strat[0:len(strat)-1], black_pos, white_move)
        else:
            # Other options are all split options, only need to call the one function
            move = self.reply_two_part(strat[0:len(strat)-1], white_move)
        return move        
    
    # TODO: methods for pattern recognition based on board state (bridge, pair, adjacent)
    def find_bridge(self,color):
        return_list = []
        # Iterate through all cells
        for pos in self.board_dict:
            pos_color = self.board_dict[pos].state
            # If the cell has the same color we are looking for
            if pos_color == color:
                cell = self.board_dict[pos]
                # Find the bridges associated with that cell
                cell_bridges = cell.get_bridges()
                for cell_bridge in cell_bridges:
                    # Get the other cell that gets bridged to
                    cell_bridge = self.board_dict[cell_bridge]
                    if cell_bridge.state == color:
                        # If the bridge cell is also the color we are looking for
                        # and the cells between them are empty, add the cells
                        # to the return list
                        pairs = list(set(cell.get_neighbours()) & set(cell_bridge.get_neighbours()))
                        if self.board_dict[pairs[0]].state == UNOCCUPIED and self.board_dict[pairs[1]].state == UNOCCUPIED:
                            return_list.append([coord_2_pos(pairs[0][0],pairs[0][1]),coord_2_pos(pairs[1][0],pairs[1][1])] + [2])
                
                # Find bridges that are edge bridges
                cell_nbrs = cell.get_neighbours()
                for nbr in cell_nbrs:
                    if self.board_dict[nbr].state == UNOCCUPIED:
                        # Get the shared cells of the neighbour and cell
                        bridge_cell = set(cell.get_neighbours()) & set(self.board_dict[nbr].get_neighbours())
                        # Iterate through the shared cells
                        for overlap_cell in bridge_cell:
                            if self.board_dict[overlap_cell].state == UNOCCUPIED:
                                # If both cells are unoccupied and black edges, then a bridge exists between them
                                if self.board_dict[overlap_cell].is_black_edge() and self.board_dict[nbr].is_black_edge():
                                    return_list.append([coord_2_pos(nbr[0],nbr[1]),coord_2_pos(overlap_cell[0],overlap_cell[1])] + [2])
                                    #cell_nbrs.remove(overlap_cell)
                                    
        return return_list
    
    def find_432(self):
        # Return all 432 patterns that are on the board
        return_list = []
        for pos in self.board_dict:
            # Can only have the 432 pattern if the cell contains a black cell
            if self.board_dict[pos].state == BLACK:
                cell = self.board_dict[pos]
                
                # Get all possible 432 patterns at that cell, then verify they
                # exist
                patterns = cell.get_432()
                for cell_432s in patterns:
                    temp_list = []
                    for cell_432 in cell_432s:
                        cell_432 = self.board_dict[cell_432]
                        temp_list.append(coord_2_pos(cell_432.x,cell_432.y))
                        
                        # The cells must be unoccupied to have the 432 pattern
                        if cell_432.state != UNOCCUPIED:
                            temp_list = []
                            break
                        
                    if temp_list != []:
                        edges = True
                        
                        # Determine whether the 432 is in an up or down formation
                        y_change = -1
                        if pos_2_coord(temp_list[4])[1] > pos_2_coord(temp_list[3])[1]:
                            y_change = 1
                        
                        connected_list = []
                        for cell_to_check in temp_list[4::]:
                            if not self.board_dict[pos_2_coord(cell_to_check)].is_black_edge():
                                # Not at an edge, must check the 432 can still exist
                                edges = False
                                
                            if not edges:
                                # Check that all cells are connected above or below
                                # to a black edge
                                cell_coords = pos_2_coord(cell_to_check)
                                neighbours = self.board_dict[cell_coords].get_neighbours()
                                
                                # Find the coordinates that need to be checked for
                                # connection to allow for the 432 pattern to exist
                                coords = [coord for coord in neighbours if \
                                          cell_coords[1] + y_change == coord[1]]
                                
                                # Check that the required neighbours can connect above
                                # or below, one of the neighbours must be black
                                for nbr in coords:
                                    if self.board_dict[nbr].state == BLACK:
                                        connected_list.append(cell_coords)
                                        break
                                
                        if edges or len(connected_list) == 4:
                            # 432 exists, add it to the return list
                            temp_list.append(coord_2_pos(pos[0],pos[1]))
                            return_list.append(temp_list + [5])
                            
        return return_list
    
    def find_adjacent_patterns(self):
        # Finds patterns that require two adjacent black coloured cells
        return_list = []
        for pos in self.board_dict:
            if self.board_dict[pos].state != BLACK:
                continue
            
            # An adjacent cell must be black to have this pattern work
            adjacents = [(pos[0]-1,pos[1]), (pos[0]+1,pos[1])]
            for coord in adjacents:
                # Check the coordinate exists in the board
                if coord[0] >= 0 and coord[0] < self.board_dimension:
                    if self.board_dict[coord].state == BLACK:
                        # Two adjacent black cells exist
                        # Patterns with "jyp#" stands for Jing Yang Pattern # 
                        return_list = self.find_double_triangle(pos, coord, return_list)
                        return_list = self.find_jyp3(pos, coord, return_list)
                        return_list = self.find_jyp4(pos, coord, return_list)
                        
        return return_list
    
    def find_jyp3(self, pos1, pos2, return_list):
        # Finds the 3rd Jing Yang pattern
        potential_patterns = []
        # We'll choose to position based on the first given black cell
        x = pos1[0]
        y = pos1[1]
        if x >= 2 and y < self.board_dimension-2 and self.board_dict[(x, y+1)].state == WHITE:
            # Pattern having a white stone here means could have a down pattern
            pattern = [(x-1,y+1), (x-2,y+2), (x-1,y+2), (x+1,y+1), (x,y+2), (x+1,y+2)]
            if self.check_all_empty(pattern):
                potential_patterns.append(pattern + [3])
        
        elif x < self.board_dimension-2 and y > 1 and self.board_dict[(x+1, y-1)].state == WHITE:
            # Pattern having a white stone here means could have an up pattern
            pattern = [(x,y-1), (x,y-2), (x+1,y-2), (x+2,y-1), (x+2,y-2), (x+3,y-2)]
            if self.check_all_empty(pattern):
                potential_patterns.append(pattern + [3])
        
        else:
            # Pattern does not exist since it doesn't have the white stone required
            return return_list
        
        # Now need to check all the potential patterns are connected
        for pattern in potential_patterns:
            if self.connected_ud_pattern(pattern):
                pattern = self.change_pattern(pattern[0:len(pattern)-1]) + [pattern[len(pattern)-1]]
                if pattern not in return_list:
                    return_list.append(pattern)
        
        return return_list
    
    def find_jyp4(self, pos1, pos2, return_list):
        # Finds the 4th Jing Yang pattern
        potential_patterns = []
        
        x = pos1[0]
        y = pos1[1]
        if x > 0 and x < self.board_dimension-2 and y < self.board_dimension-2 and \
           self.board_dict[(x,y+2)].state == WHITE:
            # Need these conditions for the downward version of this pattern
            pattern = [(x-1,y+2), (x-1,y+1), (x,y+1), (x+2,y+1), (x+2,y), (x+1,y+1), (x+1,y+2), (x+2,y+2)]
            if self.check_all_empty(pattern):
                # If all cells empty we will have this pattern if both sides connect
                potential_patterns.append(pattern + [4])
                
        elif x > 0 and x < self.board_dimension-2 and y > 1 and self.board_dict[(x+1,y-2)].state == WHITE:
            # Need these conditions for the upward version of this pattern
            pattern = [(x+2,y-2), (x+2,y-1), (x+1,y-1), (x-1,y-1), (x-1,y), (x,y-1), (x,y-2), (x-1,y-2)]
            if self.check_all_empty(pattern):
                potential_patterns.append(pattern + [4])
                
        else:
            # Pattern doesn't exist for these adjacent cells, return
            return return_list
        
        # Any potential patterns that are fully connected up/down depending on
        # the pattern get added to the return list
        cells_to_be_checked = [pattern[0]] + pattern[6:8]
        for pattern in potential_patterns:
            if self.connected_ud_pattern(cells_to_be_checked):
                pattern = self.change_pattern(pattern[0:len(pattern)-1]) + [pattern[len(pattern)-1]]
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
                    if self.board_dict[nbr].state == BLACK:
                        connected = True
                        break
                
                if not connected:
                    all_connected = False
                    
        # If all the cells connect up or down the pattern exists
        if all_connected:
            return True
        else:
            return False
    
    def find_open4x4(self):
        # Finds connected 4x4 positions with all cells being empty
        # Currently do not use, issues come with how strategies has been implemented
        # and how this pattern would be used
        return_list = []
        for x in range(self.board_dimension-3):
            for y in range(self.board_dimension-3):
                # Cells contains the potential cells for the 4x4 pattern
                cells = self.find_4x4(x,y)
                
                # Check all the cells are empty
                empty = self.check_all_empty(cells)
                if empty:
                    # Need to check that both sides are connected now
                    pass
            
        return return_list
    
    def find_4x4(self, x, y):
        # Finds a 4x4 grid using the x,y given, moving from left to right
        return_list = []
        for plus_x in range(4):
            for plus_y in range(4):
                return_list.append((x+plus_x, y+plus_y))
                
        return return_list
    
    def check_all_empty(self, cells_to_check):
        # Takes a list of cells and checks that each cell is unoccupied
        # cells_to_check should be in coordinate form, not position
        for cell in cells_to_check:
            if self.board_dict[cell].state != UNOCCUPIED:
                # Cell is taken, all cells are not empty
                return False
            
        return True
    
    def reply_bridge(self, pattern, white_move):
        # Finds the replying move when a bridge has been threatened
        if white_move in pattern:
            # Remove the white move so black can take the other cell
            pattern.remove(white_move)
        # Return the replying move
        return pos_2_coord(pattern[0])
    
    def reply432(self, pattern, black_pos, white_move):
        # Finds a replying move in the 432 pattern
        # Convert all patterns/moves into coordinate form
        pattern = self.change_pattern(pattern)
        black_pos = pos_2_coord(black_pos)
        white_move = pos_2_coord(white_move)
        
        # The max x distance between cells can tell us what type of 432 pattern
        # we're dealing with
        max_x_dist = 0
        max_x_pos = None
        for coord in pattern:
            dist = coord[0] - black_pos[0] # Distance between x values
            if abs(dist) > abs(max_x_dist):
                max_x_dist = dist
                max_x_pos = coord
                
        # Find the corner part of the triangle for the 432 pattern and the connecting
        # cell for the other 5 cells
        if abs(max_x_dist) >= 3:
            triangle_pos = (max_x_pos[0] - max_x_dist, max_x_pos[1])
            
            # Find connection cell for 5 pattern
            if (max_x_pos[0] + 1, max_x_pos[1] - 1) in pattern:
                five_pos = (max_x_pos[0] + 1, max_x_pos[1] - 1)
            else:
                five_pos = (max_x_pos[0] - 1, max_x_pos[1] + 1)
        else:
            triangle_pos = max_x_pos
            
            # Find connecting cell for 5 pattern
            if (max_x_pos[0] - 3, max_x_pos[1] + 1) in pattern:
                five_pos = (max_x_pos[0] - 3, max_x_pos[1] + 1)
            else:
                five_pos = (max_x_pos[0] + 3, max_x_pos[1] - 1)
            
        # Find the last two cells to complete the triangle
        triangle = [triangle_pos] + list(set(pattern) & set(self.board_dict[triangle_pos[0], triangle_pos[1]].get_neighbours()))
        
        if white_move in triangle or white_move not in pattern:
            # Need to perform replying move in other 5 cells
            return five_pos
            
        else:
            # Need to perform replying move in triangle
            y_coords = ''
            for coord in triangle:
                y_coords += str(coord[1])
            
            # The replying move is the one with a different y coordinate
            for num in y_coords:
                count = 0
                for item in y_coords:
                    if item == num:
                        count += 1
                if count == 1:
                    # Only one of this y coordinate exists, so we need the cell
                    # with that coordinate
                    return triangle[y_coords.index(num)]
        return
        
    def reply_two_part(self, pattern, white_move):
        # This function takes a pattern that can be broken into two parts, where
        # if played in one part the replying move is in the other part. The
        # replying moves are at the start of the split in each case
        part1 = pattern[0:3]
        part2 = pattern[3::]
        
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
    
    def is_black_edge(self):
        return self.BLACK_EDGE
    
    def generate_432_patterns(self, x, y):
        # Generates top to bottom 432 patterns
        four32 = [[(x+1,y), (x,y+1),(x-1,y+1),(x+1,y+1), (x-2,y+2),(x-1,y+2),(x,y+2),(x+1,y+2)],\
                  [(x-1,y), (x,y+1),(x-1,y+1),(x-2,y+1), (x-3,y+2),(x-2,y+2),(x-1,y+2),(x,y+2)],\
                  [(x+1,y), (x,y-1),(x+1,y-1),(x+2,y-1), (x,y-2),(x+1,y-2),(x+2,y-2),(x+3,y-2)],\
                  [(x-1,y), (x-1,y-1),(x,y-1),(x+1,y-1), (x-1,y-2),(x,y-2),(x+1,y-2),(x+2,y-2)]]
        
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
