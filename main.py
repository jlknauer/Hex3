import patterns
def main():
    # create an empty 3x3 Hex board
    board_3x3 = patterns.HexBoard(3)
    pos_dict = {'a': 0, 'b': 1, 'c': 2}
    print(board_3x3)
    while board_3x3.detect_win() == 0:
        pos = input("Enter move (ie a2): ")
        color = int(input("Enter color (0/1/2): "))
        try:
            assert 0 <= color <= 2
            assert pos[0] in pos_dict
            assert 1 <= int(pos[1]) <= 3
        except:
            print("Invalid values")
        else:
            board_3x3.place_stone(pos_dict[pos[0]], int(pos[1])-1, color)
            print(board_3x3)
            if board_3x3.detect_win() == 0:   
                print("Nobady wins")             
                print("Black adjacent pairs : ",end='')
                print(board_3x3.find_neighbors(1))
                print("White adjacent pairs : ",end='')
                print(board_3x3.find_neighbors(2))            
                print("Black Bridges : ",end='')
                print(board_3x3.find_bridge(1))
                print("White Bridges : ",end='')
                print(board_3x3.find_bridge(2))
            elif board_3x3.detect_win() == 1:
                print("Game ends,Black wins and no need to check patterns")
            else:
                print("Game ends,White wins and no need to check patterns")
if __name__ == "__main__":
    main()