import struct, string

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def PrintBoard(self):
        print(self.board[0][0] + "|" + self.board[1][0] + "|" + self.board[2][0])
        
        print(self.board[0][1] + "|" + self.board[1][1] + "|" + self.board[2][1])
        
        print(self.board[0][2] + "|" + self.board[1][2] + "|" + self.board[2][2])
        
    def play_square(self, col, row, val):
        self.board[col][row] = val

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]
        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] and self.board[0][0]==self.board[2][2] ):
            return self.board[0][0]
        if(self.board[2][0]!='N' and self.board[2][0] == self.board[1][1] and self.board[2][0]==self.board[0][2]):
            return self.board[2][0]
        return 'N'

    # return a list of all the possible moves
    def possible_moves(self):
        possible_moves = []

        for i in range(3):
            for j in range(3):
                if(self.get_square(i,j) == 'N'):
                    possible_moves.append((i,j))

        return possible_moves

# recursive minimax algorithm with alpha beta pruning
def alphabetapruning(board, turn, alpha=float("-Inf"), beta=float("Inf")):
    bestMove = (-1,-1)
    oppositePlayer = {'ai': 'human', 'human': 'ai'}
    playerSymbol = {'ai': 'X', 'human': 'O'}

    if board.winner() == 'X': 
        # computer wins, return 1
        return 1, bestMove
    elif board.winner() == 'O': 
        # human wins, return -1
        return -1, bestMove
    elif board.full_board(): 
        # draw, return 0
        return 0, bestMove

    # loop through all possible moves
    for move in board.possible_moves():
        # play the square, then calculate score, before then resetting the square to empty
        board.play_square(move[0],move[1], playerSymbol[turn])
        currentScore, (bestMove_i, bestMove_j) = alphabetapruning(board, oppositePlayer[turn], alpha, beta)
        board.play_square(move[0], move[1],'N')

        # if maximizing turn (AI's turn)
        if(turn == 'ai'):
            if currentScore > alpha:
                alpha = currentScore
                bestMove = (move[0],move[1])
        # if minimizing turn (human's turn)
        else:
            if currentScore < beta:
                beta = currentScore
                bestMove = (move[0],move[1])
        # branch unnecessary - prune it
        if beta <= alpha: 
            break

    # if no more possible moves to test, return the currently known best move
    if(turn == 'ai'): 
        return alpha, bestMove
    return beta, bestMove


def make_intelligent_cpu_move(Board, cpuval):
    # get best move/score
    bestValue, bestMove = alphabetapruning(Board, 'ai')
    Board.play_square(bestMove[0], bestMove[1], cpuval) 


def play():
    Board = TicTacToeBoard()
    humanval =  'O'
    cpuval = 'X'
    Board.PrintBoard()
    
    while( Board.full_board()==False and Board.winner() == 'N'):
        print("your move, pick a row (0-2)")
        row = int(input())
        print("your move, pick a col (0-2)")
        col = int(input())

        if(Board.get_square(col,row)!='N'):
            print("square already taken!")
            continue
        else:
            Board.play_square(col,row,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                print("CPU Move")
                make_intelligent_cpu_move(Board, cpuval)
                Board.PrintBoard()

    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("\nCat game")
    elif(Board.winner()==humanval):
        print("\nYou Win!")
    elif(Board.winner()==cpuval):
        print("\nCPU Wins!")

def main():
    play()

main()
            
