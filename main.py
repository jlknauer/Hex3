import patterns

def main():
    # create an empty 3x3 Hex board
    board_3x3 = patterns.HexBoard(3)
    board_3x3.place_stone(0,1,1)
    print(board_3x3)
    
if __name__ == "__main__":
    main()