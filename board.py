from btree import LinkedBinaryTree as BTree
from random import choice

COMBINATIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
WIN1 = 1
WIN2 = 2
TIE = 0
CONTINUE = -1


class Board():
    """Represent game field for TicTacToe"""

    def __init__(self, field = None):
        self.field = [None]*9
        if field is not None:
            self.field = field
        self.steps = []
        self.turn = 1

    def __str__(self):
        return self.print_field(self.field)

    @staticmethod
    def print_field(field):
        s = ''
        for i in range(3):
            for j in range(3):
                k = 3*i+j
                if field[k] == 1:
                    s += 'X'
                elif field[k] == 2:
                    s += 'O'
                else:
                    s += str(k)
            s += '\n'
        return s

    @staticmethod
    def check_field(field):
        """Check field"""
        res = {'w1':False, 'w2':False}
        for comb in COMBINATIONS:
            line = [field[i] for i in comb]
            if line == [1, 1, 1]:
                res['w1'] = True
            if line == [2, 2, 2]:
                res['w2'] = True

        if res['w1'] == res['w2'] == True:
            raise ValueError("Impossible situation")

        if res['w1']:
            return WIN1
        if res['w2']:
            return WIN2
        if field.count(None) == 0:
            return TIE

        return CONTINUE

    def check(self):
        return self.check_field(self.field)

    def make_step(self, pos):
        """Make step of game"""
        if pos < 0 or pos >= 9:
            raise IndexError("Position have to be between 0 and 8")
        positions = [i for i in range(9) if self.field[i] is None]
        if pos not in positions:
            raise IndexError("Position have marked yet")

        self.steps.append(pos)
        self.field[pos] = self.turn
        self.turn = 3 - self.turn
        res = self.check_field(self.field)
        return res

    @staticmethod
    def random_step(field):
        """Make random step"""
        pos = choice([i for i in range(9) if field[i] is None])
        turn = 2 - field.count(None)%2
        new_field = field.copy()
        new_field[pos] = turn
        return new_field, pos

    def game_tree(self):
        """Build game tree and return step"""
        def helper(field, pos=-1):
            tree = BTree()
            res = self.check_field(field)
            if res == WIN1:
                tree.add_root(tuple([field, 1, 1, pos]))
                return tree
            if res == WIN2:
                tree.add_root(tuple([field, -1, 1, pos]))
                return tree
            if res == TIE:
                tree.add_root(tuple([field, 0, 1, pos]))
                return tree

            tree.add_root(field)
            root = tree.root()

            left = helper(*self.random_step(field))
            right = helper(*self.random_step(field))

            points = left.root().element()[1]+right.root().element()[1]
            count = left.root().element()[2]+right.root().element()[2]
            tree.replace(root, tuple([field, points, count, pos]))

            tree.attach(root, left, right)
            return tree

        tree = helper(self.field)
        root = tree.root()
        left = tree.left(root).element()
        right = tree.right(root).element()

        l = left[1]/left[2]
        r = right[1]/right[2]

        if self.turn == 1:
            if l >= r:
                pos = left[3]
            else:
                pos = right[3]
        else:
            if l <= r:
                pos = left[3]
            else:
                pos = right[3]
        return pos

