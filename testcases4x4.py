import patterns
def main():
    n = 4
    #Case 1
    print("Case1:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,2)
    board_nxn.place_stone(1,1,2)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
    #case 2
    print("\n Case2:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,1)
    board_nxn.place_stone(1,1,1)
    board_nxn.place_stone(2,2,1)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
    #case 3
    print("\n Casen:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,2)
    board_nxn.place_stone(1,0,2)
#    board_nxn.place_stone(0,1,2)
    board_nxn.place_stone(0,2,2)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
    #case4
    print("\n Case4:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,2)
    board_nxn.place_stone(1,0,2)
#    board_nxn.place_stone(0,1,2)
    board_nxn.place_stone(0,2,2)
#    board_nxn.place_stone(2,1,2)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
    #case5
    print("\n Case5:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,2)
    board_nxn.place_stone(1,0,2)
    board_nxn.place_stone(0,1,2)
    board_nxn.place_stone(0,2,2)
#    board_nxn.place_stone(2,1,2)
    board_nxn.place_stone(2,0,2)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
    #case6
    print("\n Case6:")
    board_nxn = patterns.HexBoard(n)
    board_nxn.place_stone(0,0,1)
    board_nxn.place_stone(1,1,1)
    board_nxn.place_stone(2,2,1)
    board_nxn.place_stone(0,2,2)
    board_nxn.place_stone(1,2,2)
    print(board_nxn)
    if board_nxn.detect_win() == 0:
        print("Nobady wins")
        print("Black adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(1))
        print("White adjacent pairs : ",end='')
        print(board_nxn.find_neighbors(2))
        print("Black Bridges : ",end='')
        print(board_nxn.find_bridge(1))
        print("White Bridges : ",end='')
        print(board_nxn.find_bridge(2))
    elif board_nxn.detect_win() == 1:
        print("Game ends,Black wins and no need to check patterns")
    else:
        print("Game ends,White wins and no need to check patterns")
if __name__ == "__main__":
    main()