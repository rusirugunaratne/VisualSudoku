import numpy as np
import time
from typing import List

class SudokuSolver:
    def __init__(self, size):
        self.SIZE = size
        self.SQRT_SIZE = int(size ** 0.5)
        self.board = np.zeros((size, size), dtype=int)
        self.rowUsed = np.zeros((size, size + 1), dtype=bool)
        self.colUsed = np.zeros((size, size + 1), dtype=bool)
        self.boxUsed = np.zeros((size, size + 1), dtype=bool)

    def is_safe(self, row, col, num):
        return not self.rowUsed[row][num] and not self.colUsed[col][num] and not self.boxUsed[row // self.SQRT_SIZE * self.SQRT_SIZE + col // self.SQRT_SIZE][num]

    def heuristic_solve(self):
        unassigned_location = self.find_best_unassigned_location()
        if unassigned_location is None:
            return True  # Puzzle solved

        row, col = unassigned_location

        for num in range(1, self.SIZE + 1):
            if self.is_safe(row, col, num):
                self.place_num(row, col, num)
                if self.heuristic_solve():
                    return True
                self.remove_num(row, col, num)

        return False

    def find_best_unassigned_location(self):
        min_options = self.SIZE + 1
        unassigned_location = None

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.board[row][col] == 0:
                    options = self.count_options(row, col)
                    if options < min_options:
                        min_options = options
                        unassigned_location = (row, col)

        return unassigned_location

    def count_options(self, row, col):
        return sum(self.is_safe(row, col, num) for num in range(1, self.SIZE + 1))

    def place_num(self, row, col, num):
        self.board[row][col] = num
        self.rowUsed[row][num] = True
        self.colUsed[col][num] = True
        self.boxUsed[row // self.SQRT_SIZE * self.SQRT_SIZE + col // self.SQRT_SIZE][num] = True

    def remove_num(self, row, col, num):
        self.board[row][col] = 0
        self.rowUsed[row][num] = False
        self.colUsed[col][num] = False
        self.boxUsed[row // self.SQRT_SIZE * self.SQRT_SIZE + col // self.SQRT_SIZE][num] = False

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))
        print()

    def solve_from_input(self, input_board):
        if len(input_board) != self.SIZE or any(len(row) != self.SIZE for row in input_board):
            print("Invalid input board size.")
            return None

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if 1 <= input_board[i][j] <= self.SIZE:
                    self.place_num(i, j, input_board[i][j])

        start = time.time()
        result = self.heuristic_solve()
        end = time.time()

        if result:
            print(f"Sudoku solved in {end - start:.6f} seconds.\n")
            return self.get_solved_board()
        else:
            print("No solution exists.")
            return None

    def get_solved_board(self):
        return self.board.tolist()

def solver(input_puzzle):
    print("\n================== SUDOKU SOLVER ==================\n")

    size = len(input_puzzle)

    if size == 9:
        SIZE = 9
        SQRT_SIZE = 3
    elif size == 16:
        SIZE = 16
        SQRT_SIZE = 4
    else:
        print("The puzzle size is either invalid or unrecognized.")
        return

    solver = SudokuSolver(SIZE)

    solved_board = solver.solve_from_input(input_puzzle)

    if solved_board:
        solver.print_board()

    return solved_board
