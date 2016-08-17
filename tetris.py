import os
import sys

# clear the screen for drawing
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
write = lambda x: sys.stdout.write(x)

ALLOWED_MOVES = ['a', 'w', 's', 'd']

BLOCKS = {
    1: [(1,0), (1,0), (1,1)],
    2: [(0,1), (0,1), (1,1)],
    3: [(0,1), (1,1), (1,0)],
    4: [(1,1), (1,1)],
}

class UnexpectedInput(Exception):
    pass

class Tetris(object):
    def __init__(self):
        self.board = [[0]*20]*20 ## init empty board 20x20
        self.block = 4
        self.x = 0
        self.y = 0

    ## operations on the blocks
    def rotate_clockwise(self, block):
        return zip(*block[::-1]) # TODO: check if valid (or move automatically)

    def rotate_counter_clockwise(self, block):
        return zip(*block)[::-1] # TODO: check if valid (or move automatically)

    def move_right(self):
        self.x -= 1 # TODO: check if valid

    def move_left(self):
        self.x += 1 # TODO: check if valid


    def validate_input(self, move):
        if move not in ALLOWED_MOVES:
            raise UnexpectedInput, 'Your move is invalid \nValid moves are:\n a - left\n d - right\n s - rotate clockwise\n w - rotate counter clockwise)\n'
        return move

    def read_move(self, valid_move = None):
        while not valid_move:
            try:
                valid_move = self.validate_input(raw_input('Make a move: '))
            except UnexpectedInput, e:
                write(e)
        return valid_move

    def draw_board(self):
        clear()
        for i in range(21):
            write('*')
            for j in range(20):
                write('*' if i==20 else ' ')
            write('*\n')

if __name__=='__main__':
    t = Tetris()
    t.draw_board()
    t.read_move()
