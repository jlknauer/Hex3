def main():
    pattern = ['d2', 'c3', 'b3', 'd3', 'a4', 'b4', 'c4', 'd4'] # Bottom Right
    print(reply432(change_pattern(pattern), pos_2_coord('c2'), pos_2_coord('b3')))
    
    pattern = ['a3', 'a2', 'b2', 'c2', 'a1', 'b1', 'c1', 'd1'] # Top Left
    print(reply432(change_pattern(pattern), pos_2_coord('b3'), pos_2_coord('c2')))
    
    pattern = ['c2', 'b3', 'c3', 'd3', 'a4', 'b4', 'c4', 'd4'] # Bottom Left
    print(reply432(change_pattern(pattern), pos_2_coord('d2'), pos_2_coord('d3')))
    
    pattern = ['b3', 'a2', 'b2', 'c2', 'a1', 'b1', 'c1', 'd1'] # Top Right
    print(reply432(change_pattern(pattern), pos_2_coord('a3'), pos_2_coord('a2')))

def pos_2_coord(pos):
    # Changes a board coordinate into normal coordinates
    pos_dict = {"a": 0, "b": 1, "c": 2, "d": 3}
    x = pos_dict[pos[0]]
    y = pos[1]
    return (int(x), int(y)-1)

def reply432(pattern, black_pos, white_move):
    # Finds a replying move in the 432 pattern
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
    triangle = [triangle_pos] + list(set(pattern) & set(find_neighbours(triangle_pos[0], triangle_pos[1])))
    print(triangle)
    
    if white_move in triangle:
        # Need to perform replying move in other 5 cells
        #five_pattern = []
        #for cell in pattern:
            #if cell not in triangle:
                #five_pattern.append(cell)
        return five_pos
        
    else:
        # Need to perform replying move in triangle
        y_coords = ''
        for coord in triangle:
            y_coords += str(coord[1])
        
        for num in y_coords:
            count = 0
            for item in y_coords:
                if item == num:
                    count += 1
            if count == 1:
                return triangle[y_coords.index(num)]
    return

def change_pattern(pattern):
    for i in range(len(pattern)):
        pattern[i] = pos_2_coord(pattern[i])
    return pattern

def find_neighbours(x,y):
    neighbours = [(x+1,y), (x+1,y-1), (x,y+1), (x,y-1), (x-1,y),(x-1,y+1)]
    neighbours = [coord for coord in neighbours if not \
                  (coord[0] < 0 or coord[0] >= 4 or coord[1] < 0 or coord[1] >= 4)]
    return neighbours

main()