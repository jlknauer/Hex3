def main():
    pattern = ['d2', 'c3', 'b3', 'd3', 'a4', 'b4', 'c4', 'd4']
    reply432(change_pattern(pattern), pos_2_coord('c2'))
    
    #pattern = ['a3', 'a2', 'b2', 'c2', 'a1', 'b1', 'c1', 'd1']
    #reply432(change_pattern(pattern), pos_2_coord('b3'))
    
    #pattern = ['c2', 'b3', 'c3', 'd3', 'a4', 'b4', 'c4', 'd4']
    #reply432(change_pattern(pattern), pos_2_coord('d2'))
    
    #pattern = ['b3', 'a2', 'b2', 'c2', 'a1', 'b1', 'c1', 'd1']
    #reply432(change_pattern(pattern), pos_2_coord('a3'))

def pos_2_coord(pos):
    # Changes a board coordinate into normal coordinates
    pos_dict = {"a": 0, "b": 1, "c": 2, "d": 3}
    x = pos_dict[pos[0]]
    y = pos[1]
    return (int(x), int(y)-1)

def reply432(pattern, black_pos):
    max_x_dist = 0
    max_x_pos = None
    for coord in pattern:
        dist = coord[0] - black_pos[0] # Distance between x values
        if abs(dist) > abs(max_x_dist):
            max_x_dist = dist
            max_x_pos = coord
            
    find_neighbours(max_x_pos[0], max_x_pos[1])
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