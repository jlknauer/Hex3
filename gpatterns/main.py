import gpatterns

def main():
    board_3x3 = gpatterns.HexBoard(3)
    print(board_3x3)
    while(True):
        board_3x3.get_next_move()
        print(board_3x3)
        board_3x3.search_strategies(gpatterns.BLACK)

if __name__ == "__main__":
    main()