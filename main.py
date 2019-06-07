import patterns
def main():
    n = 4
    # create an empty nxn Hex board
    board_nxn = patterns.HexBoard(n)
    pos_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
    board_nxn.place_stone(1, 1, 1)
    print(board_nxn)
    while board_nxn.detect_win() == 0:
        print("\n")
        pos = input("Enter move (ie a2): ")
        #color = int(input("Enter color (0/1/2): "))
        color = 2
        try:
            assert 0 <= color <= 2
            assert pos[0] in pos_dict
            assert 1 <= int(pos[1]) <= 3
        except:
            print("Invalid values")
        else:
            board_nxn.place_stone(pos_dict[pos[0]], int(pos[1])-1, color)
            print(board_nxn)
            if board_nxn.detect_win() == 0:
                print("Nobody wins")             
                print("Black adjacent pairs : ",end='')
                print(board_nxn.find_neighbors(1))
                         
                print("Black Bridges : ",end='')
                print(board_nxn.find_substrategies())
                
            elif board_nxn.detect_win() == 1:
                print("Game ends,Black wins and no need to check patterns")
            else:
                print("Game ends,White wins and no need to check patterns")
                
if __name__ == "__main__":
    main()