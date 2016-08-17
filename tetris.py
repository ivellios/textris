import os
import sys
import copy

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

class IllegalMove(Exception):
    pass

class Tetris(object):
    def __init__(self):
        self.board = []## init empty board 20x20
        for i in range(20):
            self.board.append([4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,])
        self.board.append([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
        self.block = 4
        self.x = 1
        self.y = 0
        self.output_board = copy.deepcopy(self.board)
        self.eog = False

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

    def play(self, valid_move = None):
        self.calculate_board()
        self.draw_board()
        while not self.eog:
            while not valid_move:
                try:
                    valid_move = self.validate_input(raw_input('Make a move: '))
                    self.calculate_board(valid_move)
                except UnexpectedInput, e:
                    write(e)
                except IllegalMove, e:
                    write(e)
            self.draw_board()
            valid_move = None

    def get_random_x(self):
        return 5 ## TODO: randomize starting location

    def calculate_board(self, valid_move = None):
        if valid_move:
            self.output_board = copy.deepcopy(self.board)
            self.y += 1
            if valid_move == 'a':
                self.x -= 1
            if valid_move == 'd':
                self.x += 1
        block = BLOCKS[self.block]
        for i in range(len(block)):
            for j in range(len(block[0])):
                self.output_board[self.y+i][self.x+j] = self.board[self.y+i][self.x+j]+block[i][j]
        if 5 in self.output_board:
            raise IllegalMove, 'Cannot move on the border'
        if 3 in self.output_board:
            pass

    def draw_board(self):
        clear()
        for i in range(21): # for each row
            for j in range(22): # for each column
                write(str(self.output_board[i][j]) if self.output_board[i][j] > 0 else ' ') # FIXME: change print to *
            write('\n')

if __name__=='__main__':
    Tetris().play()
