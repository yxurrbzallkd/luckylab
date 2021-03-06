from btree import BinaryTree
from btnode import Node
from random import randint


def random_index(lst):
    return 0 if len(lst) < 1 else randint(0, len(lst)-1)


x = 'X'
o = 'O'


class Board:
    def __init__(self):
        self._board = [[None, None, None],
                       [None, None, None],
                       [None, None, None]]
        self._n_moves = 0
        self._last_move = None

    def __getitem__(self, position):
        return self._board[position]

    def __setitem__(self, position, item):
        self[position] = item

    def __str__(self):
        string = ''
        for i in self._board:
            string += '|'
            for j in i:
                string += str(j) if j else ' '
            string += '|\n'
        return string

    def current_symbol(self):
        return o if self._n_moves % 2 else x

    def make_a_move(self, move: tuple) -> bool:
        '''Make a move, if it is invalid raise ValueError'''
        if self[move[0]][move[1]] or \
            not (-1 < move[0] < 3) or \
                not(-1 < move[1] < 3):
            raise ValueError('Invalid move')
        self[move[0]][move[1]] = self.current_symbol()
        self._n_moves += 1
        self._last_move = move

    def win(self, player_symbol: str) -> bool:
        '''Return True if player won, False otherwise'''
        if self._n_moves < 6:
            return False
        for i in range(3):
            if player_symbol == self[i][0] == self[i][1] == self[i][2]:
                return True
            if player_symbol == self[0][i] == self[1][i] == self[2][i]:
                return True
        if player_symbol == self[0][0] == self[1][1] == self[2][2]:
            return True
        if player_symbol == self[0][2] == self[1][1] == self[2][0]:
            return True
        return False

    def clear(self):
        self._board = [[None for i in range(3)] for i in range(3)]

    def lose(self, player_symbol) -> bool:
        '''Return True if player lost, False otherwise'''
        return self.win(x if player_symbol == o else o)

    def draw(self):
        '''Return True if draw'''
        return (not self.win(x) and not self.win(o) and self._n_moves > 0)\
            and self._n_moves == 9

    def empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if not self[i][j]]

    def build_tree(self):
        '''Build a tree for analyzing outcomes of a random game

        Algorithm:
        1. Make a tree
        2. recursively:
            a) pick a random move, update board
            b) if won, write 1 into tree leaf,
               if lost, write -1 into tree leaf
               if draw, write 0 into tree leaf
               else: a)
            c) clear move
            d) make another move, if possible
            e) b)
        3. return the tree
        '''

        tree = BinaryTree(Node(None))
        # save to preserve board's initial state
        last_move = self._last_move

        def extend_tree(tree, player_symbol):
            available_moves = self.empty_cells()
            next_symbol = o if player_symbol is x else x

            if self.win(self.current_symbol()):
                tree.insert_left(Node(1, tree.root))
                return
            if self.lose(self.current_symbol()):
                tree.insert_left(Node(-1, tree.root))
                return
            elif self.draw():
                tree.insert_right(Node(0, tree.root))
                return

            move1 = available_moves.pop(random_index(available_moves))
            self.make_a_move(move1)

            tree.insert_left(Node(move1))
            extend_tree(tree.left_child, next_symbol)

            self[move1[0]][move1[1]] = None
            self._n_moves -= 1

            if available_moves:
                move2 = available_moves.pop(random_index(available_moves))
                self.make_a_move(move2)

                tree.insert_right(Node(move2))
                extend_tree(tree.right_child, next_symbol)

                self[move2[0]][move2[1]] = None
                self._n_moves -= 1

        extend_tree(tree, self.current_symbol())
        self._last_move = last_move  # return board to its initial state
        return tree

    def decide_move(self, tree):
        '''Given a tree as generated by Board.build_tree\
            pick a starategically better move'''

        def recurse(tree):
            if tree is None or tree.root.data is None:
                return 0
            if isinstance(tree.root.data, int):
                return tree.root.data
            return recurse(tree.left_child)+recurse(tree.right_child)

        move1 = tree.left_child.root.data
        if not tree.right_child:
            return move1
        move2 = tree.right_child.root.data
        score1, score2 = recurse(tree.left_child), recurse(tree.right_child)

        return move1 if score1 > score2 else move2

    def game_over(self):
        if self.win(x) or self.win(o) or self.draw():
            return True
        return False


if __name__ == '__main__':
    b = Board()
    b.make_a_move((0, 0))
    b.make_a_move((0, 1))
    b.make_a_move((0, 2))
    b.make_a_move((1, 0))
    b.make_a_move((1, 2))
    b.make_a_move((2, 0))
    b.make_a_move((1, 1))
    b.make_a_move((2, 1))
    tree = b.build_tree()
    print(b.make_a_move(b.decide_move(tree)))
