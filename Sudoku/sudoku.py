#!/usr/bin/env python

import struct, string, math, copy
from time import time
#this will be the game object your player will manipulate
class SudokuBoard:

    #the constructor for the SudokuBoard
    def __init__(self, size, board, constraintChecks):
      self.BoardSize = size #the size of the board
      self.CurrentGameboard= board #the current state of the game board
      self.ConstraintChecks = constraintChecks

    #This function will create a new sudoku board object with
    #with the input value placed on the GameBoard row and col are
    #both zero-indexed
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard, self.ConstraintChecks) #return a new board of the same size with the value added
    


# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements witha value of 0 are considered to be empty

def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board


#takes in an array representing a sudoku board and tests to
#see if it has been filled in correctly
def iscomplete( BoardArray ):
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        #check each cell on the board for a 0, or if the value of the cell
        #is present elsewhere within the same row, column, or square
        for row in range(size):
            for col in range(size):

                if BoardArray[row][col]==0:
                    return False
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                           and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                            return False
        return True

# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board, 0)


# check to see if adding a value to a board will still allow for the board to be valid, returns True
# if the board with the new value is valid, otherwise returns false
def checkConstraints(board, newRow, newCol, newEntry):
    size = len(board)
    #get size of smaller squares
    smallsquare = int(math.sqrt(size))

    # check if any other cell in the row, column, or grid of the test cell has the test value
    for i in range(size):
        # check if rows are valid
        if (board[newRow][i] == newEntry):
            return False
        # check if columns are valid
        if (board[i][newCol] == newEntry):
            return False
        # determine which square the cell is in
        currentSquareRow = newRow // smallsquare
        currentSquareCol = newCol // smallsquare
        for x in range(smallsquare):
            for y in range(smallsquare):
                testRow = currentSquareRow*smallsquare + x
                testCol = currentSquareCol*smallsquare + y
                if(board[testRow][testCol] == newEntry):
                    return False

    return True

def getNextCell( sudoku ):
    for row in range(sudoku.BoardSize):
        for col in range(sudoku.BoardSize):
            if ( sudoku.CurrentGameboard[row][col] == 0 ): return row, col
    return -1, -1


def backtracking(sudoku):
    global start_time
    current_time = time()-start_time
    if (current_time) > 30:
        print 'Time Limit Exceeded \n'
        return True
   
    print int(current_time)
    print "\n"
    if((int(current_time)%10 == 0) and (current_time > 0)):
        PrintBoard(sudoku)

    #PrintBoard(sudoku)
    nextrow, nextcol = getNextCell( sudoku )
    if ( nextrow == nextcol == -1 ): return True

    for value in range(1, sudoku.BoardSize+1):
        sudoku.ConstraintChecks += 1
        if checkConstraints(sudoku.CurrentGameboard, nextrow, nextcol, value):
            sudoku.set_value(nextrow, nextcol, value)

            ## if board is full (must be valid due to constraint checks) - then return true
            if (backtracking(sudoku)):
                return True
        ## if value is not valid, leave blank
        sudoku.set_value(nextrow, nextcol, 0)

    ## keep going
    return False

def createEmptyPossibility(sudoku):
    possibilityMatrix = [[range(1,sudoku.BoardSize+1) for row in range(sudoku.BoardSize)] for col in range(sudoku.BoardSize)]
    
    for row in range(sudoku.BoardSize):
        for col in range(sudoku.BoardSize):
            value = sudoku.CurrentGameboard[row][col]

            if (value != 0): 
                possibilityMatrix = updatePossibilityMatrix(sudoku, possibilityMatrix, row, col, value, 'removeFromPossibilityMatrix') 

    return possibilityMatrix


def updatePossibilityMatrix(sudoku, possibilityMatrix, currentRow, currentCol, value, action):
    size = len(possibilityMatrix)

    # if the value is in the same row/column, remove value
    for i in range(size):
        if action == 'removeFromPossibilityMatrix':
            if (value in possibilityMatrix[currentRow][i]):
                possibilityMatrix[currentRow][i].remove(value)
            if (value in possibilityMatrix[i][currentCol]): 
                possibilityMatrix[i][currentCol].remove(value)

        elif action == 'addFromPossibilityMatrix':
            if (checkConstraints(sudoku.CurrentGameboard, currentRow, i, value) and (value not in possibilityMatrix[currentRow][i])):
                possibilityMatrix[currentRow][i].append(value)
            if (checkConstraints(sudoku.CurrentGameboard, i, currentCol, value) and (value not in possibilityMatrix[i][currentCol])):
                possibilityMatrix[i][currentCol].append(value)
            
    # calculate the subsquare
    subsquare = int(math.sqrt(size))
    SquareRow = currentRow // subsquare
    SquareCol = currentCol // subsquare

    for i in range(subsquare):
        for j in range(subsquare):
            row, col = SquareRow * subsquare + i, SquareCol * subsquare + j

            if(value in possibilityMatrix[row][col] and action == 'removeFromPossibilityMatrix'):
                possibilityMatrix[row][col].remove(value)
            elif (action == 'addFromPossibilityMatrix' and (value not in possibilityMatrix[row][col]) and checkConstraints(sudoku.CurrentGameboard, row, col, value)): 
                possibilityMatrix[row][col].append(value)

    return possibilityMatrix


# forward checking algorithm
def forwardChecking(sudoku, possibilityMatrix):
    global start_time
    if ( time() - start_time ) > 10:
        print 'Time Limit Exceeded \n'
        return True
    if((time()-start_time)%10 == 0):
        PrintBoard(sudoku)

    nextrow, nextcol = getNextCell(sudoku)

    #if board is full (and thereby valid), finish
    if ( nextrow == nextcol == -1 ):
        return True

    # create a copy of the new possibilityMatrix, but use deepcopy because there are objects that need to be copied
    newPossibilityMatrix = copy.deepcopy(possibilityMatrix[nextrow][nextcol])

    for value in newPossibilityMatrix:
        sudoku.ConstraintChecks += 1
        
        if checkConstraints(sudoku.CurrentGameboard, nextrow, nextcol, value):
            sudoku.set_value(nextrow, nextcol, value)
            updatePossibilityMatrix(sudoku, possibilityMatrix, nextrow, nextcol, value, 'removeFromPossibilityMatrix')
            
            if (forwardChecking(sudoku, possibilityMatrix)): 
                return True

        sudoku.set_value(nextrow, nextcol, 0)
        updatePossibilityMatrix(sudoku, possibilityMatrix, nextrow, nextcol, value, 'addFromPossibilityMatrix')
                    
    return False


def PrintBoard(sudokuboard):
    board = sudokuboard.CurrentGameboard
    size = len(board)

    for i in range(size):
        for j in range(size):
            print board[i][j], "\t",
            if(j == size-1):
                print ""
    print ""

x = input("Please input the size of the sudoku board (4,9,16): ")


if (x == 4 or x == 9 or x == 16 or x == 25):
    puzzle_path = "%s_%s.sudoku" % (x, x)
else: 
    print "Please enter a valid size \n"

print "Testing backtracking \n"
backtrackBoard = init_board(puzzle_path)

start_time = time()
final = backtracking(backtrackBoard)
passed_time = time() - start_time
print 'Length of Time: %.2f' % passed_time
print 'Number of checks: %d' % backtrackBoard.ConstraintChecks

PrintBoard(backtrackBoard)

print 'Testing forward checking\n'
forwardCheckBoard = init_board(puzzle_path)

start_time = time()
possibilityMatrix = createEmptyPossibility(forwardCheckBoard)
final = forwardChecking(forwardCheckBoard, possibilityMatrix)
passed_time = time() - start_time

print 'Length of Time: %.2f' % passed_time
print 'Number of checks: %d' % forwardCheckBoard.ConstraintChecks


PrintBoard(forwardCheckBoard)


