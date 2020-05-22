from board import Board
from random import choice
from time import sleep


with open('preparations.txt') as file:
    prayer = file.read()
with open('for_the_machines.txt') as file:
    the_question = file.read()
with open('meatbag.txt') as file:
    meatbag = file.read()
with open('congrats.txt') as file:
    congrats = file.read()


# The score
humans = 0
machines = 0

o = 'O'
x = 'X'


def main():
    global humans
    global machines

    def read_integer_in_range(a, b) -> int:
        i = a-1
        while not a < i < b:
            n = input(f'Integer from {a+1} to {b-1}: ')
            try:
                n = int(n)
                i = n
            except ValueError:
                print(f'Invalid input: {n} is not an integer')
        return i

    def read_move() -> tuple:
        i = read_integer_in_range(-1, 3)
        j = read_integer_in_range(-1, 3)
        return (i, j)

    def user_move(board):
        while True:
            move = read_move()
            try:
                board.make_a_move(move)
                return
            except ValueError:
                print('Invalid move')

    board = Board()
    user_symbol = choice([o, x])
    print(f'You are playing for {user_symbol}\n')

    user, other_user = ('user', 'computer') if user_symbol == x\
        else ('computer', 'user')
    while not board.game_over():
        if user == 'computer':
            print("Computer's turn:")
            sleep(1)  # for a more realistic game experience
            board.make_a_move(board.decide_move(board.build_tree()))
        else:
            print('Your turn: ')
            user_move(board)
        user, other_user = other_user, user
        print(board)

    if board.win(user_symbol):
        print('Congratulations, you won!\n')
        humans += 1
        print(congrats)
    elif board.win(x if user_symbol is o else o):
        print('Game Over\ncomputer won...\n')
        machines += 1
        print(meatbag)
    else:
        print('draw\n')


def game_loop():
    for line in prayer.split('\n'):
        print(line)
        sleep(1)
    print('\n\n')
    print('Welcome to tic-tac-toe!\n\n')
    while True:
        main()
        choice = input('Quit game? [y/n]: [y] ')
        if choice == 'y':
            break
        print('\n\n')
    print(f'\n\nHuman | Machines\n{humans} {machines}')
    if humans > machines:
        print(the_question, '\n\n')
    print("Thanks for choosing Lame Entertainement!\n\n\
2099, Lame Entertainment Inc.\n")


if __name__ == '__main__':
    game_loop()
