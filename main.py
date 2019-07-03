import patterns
def main():
    n = 8
    # create an empty nxn Hex board
    board_nxn = patterns.HexBoard(n)
    pos_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    #board_nxn.place_stone(0, 2, 1)
    #board_nxn.place_stone(3, 2, 1)
    board_nxn.place_stone(1, 6, 1)
    
    board_nxn.place_stone(1,2,1)
    board_nxn.place_stone(2,2,1)
    
    print(board_nxn)
    print("Black Bridges : ",end='')
    print(board_nxn.find_bridge(1))
    print("Black 432s : ",end='')
    print(board_nxn.find_432())
    print("Black Six Patterns : ",end='')
    print(board_nxn.find_six())
    while board_nxn.detect_win() == 0:
        print("\n")
        pos = input("Enter move (ie a2): ")
        color = 2
        try:
            assert pos[0] in pos_dict
            assert 1 <= int(pos[1::]) <= n
        except:
            print("Invalid values")
        else:
            board_nxn.place_stone(pos_dict[pos[0]], int(pos[1])-1, color)
            print(board_nxn)
            if board_nxn.detect_win() == 0:
                print("Nobody wins")             
                #print("Black adjacent pairs : ",end='')
                #print(board_nxn.find_neighbors(1))
                                    
                print("Black Bridges : ",end='')
                print(board_nxn.find_bridge(1))
                print("Black 432s : ",end='')
                print(board_nxn.find_432())

            elif board_nxn.detect_win() == 1:
                print("Game ends, black wins and no need to check patterns")
            else:
                print("Game ends, white wins and no need to check patterns")
                
if __name__ == "__main__":
    main()