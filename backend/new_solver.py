import numpy as np
import os
import sys
import time

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
        min_options = sys.maxsize
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

    def load_board(self, filename):
        try:
            self.board = np.loadtxt(filename, dtype=int)
            for i in range(self.SIZE):
                for j in range(self.SIZE):
                    if self.board[i][j] != 0:
                        self.place_num(i, j, self.board[i][j])
            return True
        except Exception as e:
            print(f"Error loading board from file: {e}")
            return False

    def save_board(self, filename):
        try:
            np.savetxt(filename, self.board, fmt='%d')
            return True
        except Exception as e:
            print(f"Error saving board to file: {e}")
            return False


def count_rows_in_file(filename):
    try:
        with open(filename) as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        return 0


def generate_output_filename(input_filename):
    root, ext = os.path.splitext(input_filename)
    return f"{root}_output{ext}"


def main():
    print("\n================== SUDOKU SOLVER ==================\n")
    filename = 'sudoku_board.txt'

    size = count_rows_in_file(filename)

    if size == 9:
        SIZE = 9
        SQRT_SIZE = 3
    elif size == 16:
        SIZE = 16
        SQRT_SIZE = 4
    else:
        print("The puzzle size is either invalid or unrecognized.")
        return

    solver = SudokuSolver(size)

    if not solver.load_board(filename):
        print("Failed to load board from file.")
        return

    start = time.time()
    result = solver.heuristic_solve()
    end = time.time()

    if result:
        print(f"Sudoku solved in {end - start:.6f} seconds.\n")
        output_filename = generate_output_filename(filename)
        solver.save_board(output_filename)
        solver.print_board()
        print("\n====================================================")
    else:
        print("No solution exists.")


if __name__ == "__main__":
    main()
