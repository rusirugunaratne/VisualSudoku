#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <atomic>
#include <mutex>
#include <sstream>

int SIZE;
int SQRT_SIZE;
std::mutex mtx;
std::atomic<bool> solved(false);

struct SudokuSolver {
    std::vector<std::vector<int>> board;
    std::vector<std::vector<bool>> rowUsed, colUsed, boxUsed;

    SudokuSolver() : board(SIZE, std::vector<int>(SIZE)),
                     rowUsed(SIZE, std::vector<bool>(SIZE + 1)),
                     colUsed(SIZE, std::vector<bool>(SIZE + 1)),
                     boxUsed(SIZE, std::vector<bool>(SIZE + 1)) {}

    bool isSafe(int row, int col, int num) const {
        return !rowUsed[row][num] && !colUsed[col][num] && !boxUsed[row / SQRT_SIZE * SQRT_SIZE + col / SQRT_SIZE][num];
    }

    bool heuristicSolve() {
        int row, col;
        if (!findBestUnassignedLocation(row, col))
            return true; // Puzzle solved

        for (int num = 1; num <= SIZE; num++) {
            if (isSafe(row, col, num)) {
                placeNum(row, col, num);
                if (heuristicSolve())
                    return true;
                removeNum(row, col, num);
            }
        }
        return false;
    }

    bool findBestUnassignedLocation(int &row, int &col) {
        int minOptions = SIZE + 1;
        bool found = false;
        for (int r = 0; r < SIZE; r++) {
            for (int c = 0; c < SIZE; c++) {
                if (board[r][c] == 0) {
                    int options = countOptions(r, c);
                    if (options < minOptions) {
                        minOptions = options;
                        row = r;
                        col = c;
                        found = true;
                    }
                }
            }
        }
        return found;
    }

    int countOptions(int row, int col) const {
        int count = 0;
        for (int num = 1; num <= SIZE; num++) {
            if (isSafe(row, col, num)) count++;
        }
        return count;
    }

    void placeNum(int row, int col, int num) {
        board[row][col] = num;
        rowUsed[row][num] = true;
        colUsed[col][num] = true;
        boxUsed[row / SQRT_SIZE * SQRT_SIZE + col / SQRT_SIZE][num] = true;
    }

    void removeNum(int row, int col, int num) {
        board[row][col] = 0;
        rowUsed[row][num] = false;
        colUsed[col][num] = false;
        boxUsed[row / SQRT_SIZE * SQRT_SIZE + col / SQRT_SIZE][num] = false;
    }

    void printBoard(std::ostream& os = std::cout) const {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                os << board[i][j] << " ";
            }
            os << std::endl;
        }
    }

    bool loadBoard(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            return false;
        }

        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                file >> board[i][j];
                if (board[i][j]) {
                    placeNum(i, j, board[i][j]);
                }
            }
        }

        file.close();
        return true;
    }

    bool saveBoard(const std::string& filename) {
        std::ofstream file(filename);
        if (!file.is_open()) {
            return false;
        }

        printBoard(file);
        file.close();
        return true;
    }
};


int countRowsInFile(const std::string& filename) {
    std::ifstream file(filename);

    int rowCount = 0;
    std::string line;

    while (std::getline(file, line)) {
        rowCount++;
    }

    return rowCount;
}

std::string generateOutputFileName(const std::string& inputFileName) {
    // Find the last dot in the filename, which typically starts the file extension
    size_t dotPos = inputFileName.rfind('.');

    // If there's no dot, or it's at the beginning, we don't consider it a valid extension
    if (dotPos == std::string::npos || dotPos == 0) {
        return inputFileName + "_output.txt";  // No extension, append "_output.txt"
    }

    // Insert "_output" before the dot (extension)
    return inputFileName.substr(0, dotPos) + "_output" + inputFileName.substr(dotPos);
}


int main() {
    std::cout << "\n================== SUDOKU SOLVER ==================\n\n";
    std::cout << "Enter the input file name:";
    std::string filename;
    filename = 'sudoku_board.txt';

    int size = countRowsInFile(filename);

    if (size == 9) {
        SIZE = 9;
        SQRT_SIZE = 3;
    } else if (size == 16) {
        SIZE = 16;
        SQRT_SIZE = 4;
    } else {
        std::cout << "The puzzle size is either invalid or unrecognized." << std::endl;
    }

    SudokuSolver solver;

    if (!solver.loadBoard("D:\\Git Hub Projects\\Sudoku Solver\\1\\Sample Inputs\\" + filename)) {
        std::cerr << "Failed to load board from file." << std::endl;
        return 1;
    }

    auto start = std::chrono::high_resolution_clock::now();

    bool result = solver.heuristicSolve();

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;

    if (result) {
        std::cout << "Sudoku solved in " << elapsed.count() << " milliseconds.\n" << std::endl;
        std::string output_filename;
        output_filename = generateOutputFileName(filename);
        solver.saveBoard("D:\\Git Hub Projects\\Sudoku Solver\\1\\Sample Solutions & Outputs\\" + output_filename);
        solver.printBoard();
        std::cout << "\n====================================================";
    } else {
        std::cout << "No solution exists." << std::endl;
    }

    return 0;
}
