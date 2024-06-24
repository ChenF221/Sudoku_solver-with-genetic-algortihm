'''
Authors: Chen Yangfeng, Diaz Jimenez Jorge Arif, 5BM1, Escom IPN
26/jun/24  Algoritmos Bioinpirados, Proyecto Final
Sudoku_solver-with-genetic-algortihm
'''

import random
import math

class Sudoku:
    def __init__(self, N, difficulty_level):
        self.N = N
        self.difficulty_level = difficulty_level

        # Compute square root of N
        SRNd = math.sqrt(N)
        self.SRN = int(SRNd)
        self.mat = [[0 for _ in range(N)] for _ in range(N)]

    def fillValues(self):
        # Fill the diagonal of SRN x SRN matrices
        self.fillDiagonal()

        # Fill remaining blocks
        self.fillRemaining(0, self.SRN)

        # Remove Randomly K digits based on the difficulty level to make the game
        self.removeKDigits()

    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)

    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True

    def fillBox(self, row, col):
        num = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.unUsedInBox(row, col, num):
                        break
                self.mat[row + i][col + j] = num

    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)

    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))

    def unUsedInRow(self, i, num):
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True

    def unUsedInCol(self, j, num):
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True

    def fillRemaining(self, i, j):
        # Check if we have reached the end of the matrix
        if i == self.N - 1 and j == self.N:
            return True

        # Move to the next row if we have reached the end of the current row
        if j == self.N:
            i += 1
            j = 0

        # Skip cells that are already filled
        if self.mat[i][j] != 0:
            return self.fillRemaining(i, j + 1)

        # Try filling the current cell with a valid value
        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.mat[i][j] = 0

        # No valid value was found, so backtrack
        return False

    def removeKDigits(self):
        if self.difficulty_level == "Fácil":
            count = 30
        elif self.difficulty_level == "Intermedio":
            count = 37
        elif self.difficulty_level == "Avanzado":
            count = 40
        else:
            raise ValueError("Invalid difficulty level")

        while count != 0:
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if self.mat[i][j] != 0:
                count -= 1
                self.mat[i][j] = 0

        return

    def printSudoku(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.mat[i][j], end=" ")
            print()

# Driver code
if __name__ == "__main__":
    N = 9
    difficulty_level = "Fácil"  # Adjust difficulty level as needed
    sudoku = Sudoku(N, difficulty_level)
    sudoku.fillValues()
    sudoku.printSudoku()
