import os
import sys
import copy
import random

## some helper functions
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
write = lambda x: sys.stdout.write(x)

ALLOWED_MOVES = ['a', 'w', 's', 'd']

BLOCKS = {
    0: [(1,0), (1,0), (1,1)],
    1: [(0,1), (0,1), (1,1)],
    2: [(0,1), (1,1), (1,0)],
    3: [(1,1), (1,1)],
}

class UnexpectedInput(Exception):
    pass

class IllegalMove(Exception):
    pass

class BlockLocked(Exception):
    pass

class Textris(object):
    def __init__(self):
        self.board = [] ## init empty board 20x20 with contant parts
        for i in range(20):
            self.board.append([4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,])
        self.board.append([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
        self.output_board = copy.deepcopy(self.board) ## board for printing

        self.eog = False # End of game?
        # these will be set at the start of the game
        self.block = None # Current block
        self.x = 1 # Current x position of the block
        self.y = 0 # Current y position of the block

        self.temp_board = [] # temporary board for calculations

    ## operations on the blocks
    def rotate_clockwise(self):
        self.block = zip(*self.block[::-1])

    def rotate_counter_clockwise(self):
        self.block = zip(*self.block)[::-1]

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def validate_input(self, move):
        if move not in ALLOWED_MOVES:
            raise UnexpectedInput, 'Your move is invalid \nValid moves are:\n a - left\n d - right\n s - rotate clockwise\n w - rotate counter clockwise)\n'
        return move

    def make_move(self, valid_input):
        """ Moves the block depending on the key input """
        if valid_input == 'a':
            self.move_left()
        if valid_input == 'd':
            self.move_right()
        if valid_input == 'w':
            self.rotate_counter_clockwise()
        if valid_input == 's':
            self.rotate_clockwise()
        self.y += 1 # and at the same time it moves it down (if it is valid)
        ## Probably it would be a good idea to displace block, check if it is
        ## valid and then move down and again check. But the instructions didn't
        ## consider it.

    def revert_move(self, valid_input):
        """ In case of exception reverts the movement of the block """
        if valid_input == 'a':
            self.move_right()
        if valid_input == 'd':
            self.move_left()
        if valid_input == 'w':
            self.rotate_clockwise()
        if valid_input == 's':
            self.rotate_counter_clockwise()
        self.y -= 1

    def generate_new_block(self):
        self.block = copy.deepcopy(BLOCKS[random.randint(0,3)]) # pick a random block
        self.y = 0 # set position to top and randomly on the x axis
        self.x = random.randint(1,19)

    def isLocked(self):
        """ Tries to move down and checks whether the block is blocked by
            anything below.
        """
        self.y += 1
        try:
            self.calculate_board(use_output = True) # uses output instead of contant board
        except BlockLocked:
            return True
        finally:
            self.y -= 1
        return False

    def play(self, valid_input = None):
        self.generate_new_block() # create first block
        self.calculate_board() # safe - at start will not raise any Exception
        self.draw_board() # draw starting board
        # and here we go...
        while not self.eog:
            try:
                valid_input = self.validate_input(raw_input('Make a move: '))
                self.make_move(valid_input) # set the movement
                self.calculate_board() # check the board for a new state and prere to be drawn
                if self.isLocked(): # check if block is locked on place
                    self.save_output_board() # make the block constant on board
                    self.generate_new_block()
                    try:
                        self.calculate_board() # because, maybe there's no more space?
                    except IllegalMove: # if so...
                        self.draw_board() # draw the last state
                        self.eog = True # and say goodbye.
                        print("Game Over")
                        break # bye bye...
                self.draw_board()
            except UnexpectedInput, e: # input key was unexpected
                self.draw_board()
                print(e)
            except IllegalMove, e: # user cannot move brick to this position
                self.revert_move(valid_input)
                self.draw_board()
                print(e)

    def save_output_board(self): # so you say, block becomes part of the board?
        for row in range(len(self.output_board)): # OK then...
            for column in range(len(self.output_board[row])):
                if self.output_board[row][column] == 1:
                    self.output_board[row][column] = 2
        self.board = copy.deepcopy(self.output_board)


    def calculate_board(self, use_output = False):
        # clone the board and let's place some block on it
        ## unless you just want to make small stem ahead
        self.temp_board = copy.deepcopy(self.output_board if use_output else self.board)
        for row in range(len(self.block)):
            for column in range(len(self.block[0])):
                try:
                    self.temp_board[self.y+row][self.x+column] = self.board[self.y+row][self.x+column]+self.block[row][column]
                except IndexError: # your block is out of the array
                    raise IllegalMove, 'Cannot rotate that way it moves out of border'
        if any(5 in row for row in self.temp_board): # you stepped on the border
            raise IllegalMove, 'Cannot move on the border'
        if not use_output:
            if any(3 in row for row in self.temp_board): # you stepped on the bottom (incl. other locked blocks)
                raise IllegalMove, "Cannot move block here"
            self.output_board = copy.deepcopy(self.temp_board) # temp is OK? then we keep it to be drawn soon
        if any(3 in row for row in self.temp_board): # your block stepped on something in this __TRY__.
            raise BlockLocked

    def draw_board(self):
        # Let's make it clear...
        clear()
        # The board will be drawn now:
        for row in range(21):
            for column in range(22):
                write('*' if self.output_board[row][column] > 0 else ' ')
            write('\n')

if __name__=='__main__':
    Textris().play()
