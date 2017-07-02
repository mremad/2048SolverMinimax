import random

SIZE = 4

UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

class Game:
    def __init__(self):
        self.board = [0]*SIZE

    def initialize_board(self):
        for idx, row in enumerate(self.board):
            self.board[idx] = [0]*SIZE
        row_idx = random.randint(0,SIZE-1)
        col_idx = random.randint(0,SIZE-1)

        self.board[row_idx][col_idx] = 2

    def count_empty_cells(self, board):
        count = 0
        for row in board:
            for val in row:
                if val < 2:
                    count += 1
        return count
    def print_board(self, board):
        print "**************************"
        for row in board:
            for val in row:
                if val > 0:
                    print "%d\t"%val,
                else:
                    print " \t",
            print "\n",

    def get_possible_cells(self, board):
        possibilities = []
        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                if val < 2:
                    poss = (row_idx, col_idx)
                    possibilities.append(poss)

        return possibilities

    def make_computer_move(self, board, cell, value):
        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE

        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                new_board[row_idx][col_idx] = board[row_idx][col_idx]

        new_board[cell[0]][cell[1]] = value

        return new_board

    def transpose(self,board):
        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE

        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                new_board[col_idx][row_idx] = board[row_idx][col_idx]

        return new_board

    def reverse(self,board):
        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE

        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                new_board[row_idx][SIZE - col_idx - 1] = board[row_idx][col_idx]

        return new_board

    def merge_left(self,board):
        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE

        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                if val < 2:
                    continue
                if col_idx + 1 < SIZE:
                    if board[row_idx][col_idx+1] == val:
                        new_board[row_idx][col_idx] = board[row_idx][col_idx] + board[row_idx][col_idx+1]
                        board[row_idx][col_idx+1] = 0
                    else:
                        new_board[row_idx][col_idx] = board[row_idx][col_idx]
                else:
                    new_board[row_idx][col_idx] = board[row_idx][col_idx]
        return new_board

    def compress_left(self,board):
        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE

        for row_idx, row in enumerate(board):
            new_col = 0
            for col_idx, val in enumerate(row):
                if val >= 2:
                    new_board[row_idx][new_col] = val
                    new_col += 1

        return new_board

    def get_board_key(self, board):
        #self.score = self.calculate_board_score(board)
        return ';'.join([' '.join([str(num) for num in row]) for row in board])
    def player_turn(self, direction, board):

        old_key = self.get_board_key(board)
        if direction == LEFT:
            new_board = self.compress_left(board)
            new_board = self.merge_left(new_board)
            new_board = self.compress_left(new_board)
        elif direction == UP:
            new_board = self.transpose(board)
            new_board = self.compress_left(new_board)
            new_board = self.merge_left(new_board)
            new_board = self.transpose(self.compress_left(new_board))
        elif direction == DOWN:
            new_board = self.transpose(board)
            new_board = self.reverse(new_board)
            new_board = self.compress_left(new_board)
            new_board = self.merge_left(new_board)
            new_board = self.transpose(self.reverse(self.compress_left(new_board)))
        elif direction == RIGHT:
            new_board = self.reverse(board)
            new_board = self.compress_left(new_board)
            new_board = self.merge_left(new_board)
            new_board = self.reverse(self.compress_left(new_board))
        new_key = self.get_board_key(new_board)

        if new_key != old_key:
            return new_board
        else:
            return None

    def computer_turn(self, board):

        new_board = [0]*SIZE
        for idx, row in enumerate(new_board):
            new_board[idx] = [0]*SIZE
        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                new_board[row_idx][col_idx] = board[row_idx][col_idx]

        possibilities = self.get_possible_cells(board)
        possible_values = [2,4]

        chosen_cell_idx = random.randint(0,len(possibilities) - 1)
        chosen_val_idx = random.randint(0,len(possible_values) - 1)

        chosen_cell = possibilities[chosen_cell_idx]
        chosen_value = possible_values[chosen_val_idx]

        new_board[chosen_cell[0]][chosen_cell[1]] = chosen_value

        return new_board

def main():
    new_game = Game()
    new_game.initialize_board()
    while(True):
        new_board = new_game.computer_turn(new_game.board)
        new_game.board = new_board
        new_game.print_board(new_game.board)
        x = raw_input("Enter a direction: ")
        new_board = new_game.player_turn(x, new_game.board)
        new_game.board = new_board
        print "**************************"

if __name__ == "__main__":
    main()