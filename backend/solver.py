import numpy as np

def allowedValues(board, row, col, n):
    numbersList = list()

    for number in range(1, n + 1):

        found = False
        # Check if all row elements include this number
        for j in range(n):
            if board[row][j] == number:
                found = True
                break
        # Check if all column elements include this number
        if found:
            continue
        else:
            for i in range(n):
                if board[i][col] == number:
                    found = True
                    break

        # Check if the number is already included in the block
        if found:
            continue
        else:
            rowBlockStart = (row // int(n**0.5)) * int(n**0.5)
            colBlockStart = (col // int(n**0.5)) * int(n**0.5)

            rowBlockEnd = rowBlockStart + int(n**0.5)
            colBlockEnd = colBlockStart + int(n**0.5)
            for i in range(rowBlockStart, rowBlockEnd):
                for j in range(colBlockStart, colBlockEnd):
                    if board[i][j] == number:
                        found = True
                        break
        if not found:
            numbersList.append(number)
    return numbersList

def findEmpty(board, n):
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:
                return row, col
    return None

def cacheValidValues(board, n):
    cache = dict()
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                cache[(i, j)] = allowedValues(board, i, j, n)
    return cache

def isValid(board, num, pos, n):
    row, col = pos
    # Check if all row elements include this number
    for j in range(n):
        if board[row][j] == num:
            return False

    # Check if all column elements include this number
    for i in range(n):
        if board[i][col] == num:
            return False

    # Check if the number is already included in the block
    rowBlockStart = (row // int(n**0.5)) * int(n**0.5)
    colBlockStart = (col // int(n**0.5)) * int(n**0.5)

    rowBlockEnd = rowBlockStart + int(n**0.5)
    colBlockEnd = colBlockStart + int(n**0.5)
    for i in range(rowBlockStart, rowBlockEnd):
        for j in range(colBlockStart, colBlockEnd):
            if board[i][j] == num:
                return False

    return True

def orderedValidValues(board, cache, n):
    cachePriority = dict()
    countAppearanceRow = [dict() for i in range(n)]
    countAppearanceCol = [dict() for i in range(n)]
    countAppearanceBlock = [dict() for i in range(n)]
    valuesFound = False

    for row in range(n):
        tempList = list()

        for col in range(n):
            if (row, col) in cache.keys():
                for value in cache[(row, col)]:
                    tempList.append(value)
        tempSet = set(tempList)
        for number in tempSet:
            countAppearanceRow[row][number] = tempList.count(number)

    for col in range(n):
        tempList = list()

        for row in range(n):
            if (row, col) in cache.keys():
                for value in cache[(row, col)]:
                    tempList.append(value)
        tempSet = set(tempList)
        for number in tempSet:
            countAppearanceCol[col][number] = tempList.count(number)

    rowBlockStart = 0
    colBlockStart = 0
    blockNumber = 0
    while True:
        rowBlockEnd = rowBlockStart + int(n**0.5)
        colBlockEnd = colBlockStart + int(n**0.5)
        tempList = list()
        for row in range(rowBlockStart, rowBlockEnd):
            for col in range(colBlockStart, colBlockEnd):
                if (row, col) in cache.keys():
                    for value in cache[(row, col)]:
                        tempList.append(value)
        tempSet = set(tempList)
        for number in tempSet:
            countAppearanceBlock[blockNumber][number] = tempList.count(number)
        if rowBlockStart == n - int(n**0.5) and colBlockStart == n - int(n**0.5):
            break
        elif colBlockStart == n - int(n**0.5):
            rowBlockStart += int(n**0.5)
            colBlockStart = 0
        else:
            colBlockStart += int(n**0.5)
        blockNumber += 1

    for row in range(n):
        for col in range(n):
            tempList = list()
            blockNumber = (row // int(n**0.5)) * int(n**0.5) + col // int(n**0.5)
            if (row, col) in cache.keys():
                for value in cache[(row, col)]:
                    freq = countAppearanceRow[row][value] + countAppearanceCol[col][value] + countAppearanceBlock[blockNumber][value]
                    tempList.append(freq)
                cachePriority[(row, col)] = tempList

    for row in range(n):
        for col in range(n):
            if (row, col) in cache.keys():
                cache[(row, col)] = [i for _, i in sorted(zip(cachePriority[(row, col)], cache[(row, col)]))]

                # Check if the current cell has a single valid value
                if len(cache[(row, col)]) == 1:
                    board[row][col] = cache[(row, col)][0]
                    valuesFound = True

    return valuesFound, cache

def scanBoardMultipleTimes(board, n):
    valuesFound = True

    while valuesFound:
        cacheValid = cacheValidValues(board, n)
        valuesFound, orderedCache = orderedValidValues(board, cacheValid, n)

    return orderedCache

def read_puzzle(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sudoku_board = [[int(num) for num in line.split()] for line in lines]
    return sudoku_board

def solveWithCache(board, cache):
    blank = findEmpty(board, len(board))
    if not blank:
        return True
    else:
        row, col = blank

    for value in cache[(row, col)]:
        if isValid(board, value, (row, col), len(board)):
            board[row][col] = value

            if solveWithCache(board, cache):
                return True

            board[row][col] = 0
    return False

def solve(sudoku_board):
    # Example Sudoku board

    # Determine the size of the puzzle (assuming it's either 9x9 or 16x16)
    n = len(sudoku_board)
    print(np.matrix(sudoku_board))
    print(n)

    orderedVal = scanBoardMultipleTimes(sudoku_board, n)
    solveWithCache(sudoku_board, orderedVal)
    return sudoku_board
