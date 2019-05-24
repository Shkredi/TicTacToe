from board import Board
from random import choice

game_board = Board()
player_turn = choice([1, 2])
c = "X" if player_turn == 1 else 'O'
print('You are', c)
print('-'*20)

if player_turn == 2:
    game_board.make_step(game_board.game_tree())

print(game_board)
while game_board.check() == -1:
    print('-'*5)
    while True:

        try:
            pos = int(input("Type number from 0 to 8: "))
            game_board.make_step(pos)
        except Exception as err:
            print(err)
            continue
        break

    res = game_board.check()
    if res != -1:
        print(game_board)
        if res == 1:
            print("WIN X")
        elif res == 2:
            print("WIN O")
        elif res == 0:
            print("TIE")
        break

    game_board.make_step(game_board.game_tree())
    res = game_board.check()
    if res != -1:
        print(game_board)
        if res == 1:
            print("WIN X")
        elif res == 2:
            print("WIN O")
        elif res == 0:
            print("TIE")
        break

    print('-'*20)
    print(game_board)
