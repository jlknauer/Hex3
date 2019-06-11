import patterns

def main():
    board = patterns.HexBoard(3, "b2")
    
    while(True):
        print(board)
        board.get_player_move()
        board.black_turn()

if __name__ == "__main__":
    main()