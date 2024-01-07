import math
import time

class SudokuSolver:
    def __init__(self, size):
        self.size = size
        self.sqrt_size = int(math.sqrt(size))
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.row_used = [[False for _ in range(size + 1)] for _ in range(size)]
        self.col_used = [[False for _ in range(size + 1)] for _ in range(size)]
        self.box_used = [[False for _ in range(size + 1)] for _ in range(size)]

    def is_safe(self, row, col, num):
        return not self.row_used[row][num] and not self.col_used[col][num] and not self.box_used[row // self.sqrt_size * self.sqrt_size + col // self.sqrt_size][num]

    def heuristic_solve(self):
        row, col = self.find_best_unassigned_location()
        if row is None:
            return True  # Puzzle solved

        for num in range(1, self.size + 1):
            if self.is_safe(row, col, num):
                self.place_num(row, col, num)
                if self.heuristic_solve():
                    return True
                self.remove_num(row, col, num)
        return False

    def find_best_unassigned_location(self):
        min_options = self.size + 1
        selected_row = selected_col = None

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    options = self.count_options(r, c)
                    if options < min_options:
                        min_options = options
                        selected_row, selected_col = r, c

        return selected_row, selected_col

    def count_options(self, row, col):
        count = 0
        for num in range(1, self.size + 1):
            if self.is_safe(row, col, num):
                count += 1
        return count

    def place_num(self, row, col, num):
        self.board[row][col] = num
        self.row_used[row][num] = True
        self.col_used[col][num] = True
        self.box_used[row // self.sqrt_size * self.sqrt_size + col // self.sqrt_size][num] = True

    def remove_num(self, row, col, num):
        self.board[row][col] = 0
        self.row_used[row][num] = False
        self.col_used[col][num] = False
        self.box_used[row // self.sqrt_size * self.sqrt_size + col // self.sqrt_size][num] = False

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

def main(sudoku_board):
    size = len(sudoku_board)

    if size == 9:
        SIZE = 9
    elif size == 16:
        SIZE = 16
    else:
        print("The puzzle size is either invalid or unrecognized.")
        return None  # Return None if the puzzle size is invalid

    solver = SudokuSolver(SIZE)
    solver.board = sudoku_board

    start = time.time()

    if solver.heuristic_solve():
        end = time.time()
        print("Sudoku solved in {:.2f} milliseconds.\n".format((end - start) * 1000))
        solver.print_board()
        return solver.board  # Return the solved board
    else:
        print("No solution exists.")
        return None  # Return None if no solution exists

def solve(board):
    # Example usage:
    example_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    solved_board = main(board)
    return solved_board