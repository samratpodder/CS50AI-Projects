"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countO=0
    countX=0

    for pos in board:
        for items in pos:
            if items==X:
                countX+=1
            if items==O:
                countO+=1
    if countO == countX:
        return X
    if countX>countO:
        return O
    if countO==4 and countX==5:
        return -1

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions=[]
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.append((i,j))
    return actions
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardcopy = copy.deepcopy(board)
    if boardcopy[action[0]][action[1]] != EMPTY:
        raise Exception("not a valid move")
    else:
        boardcopy[action[0]][action[1]] = player(boardcopy)
    return boardcopy

    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    xcount=0
    ocount=0
    # [------->]
    # [------->]
    # [------->]
    
    for i in range(3):
        xcount=0
        ocount=0
        for j in range(3):
            if board[i][j] == X:
                xcount+=1
            if board[i][j] == O:
                ocount+=1
        if xcount==3:
            return X
        if ocount == 3:
            return O
    # [^^^^^^^]
    # [|||||||]
    # [|||||||]
    # [|||||||]
    for j in range(3):
        xcount=0
        ocount=0
        for i in range(3):
            if board[i][j] == X:
                xcount+=1
            if board[i][j] == O:
                ocount+=1
        if xcount==3:
            return X
        if ocount == 3:
            return O
    #Diagonals
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    #Tie
    return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0:
        return True
    if winner(board) is not None:
        return True
    return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    # raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    k=0
    best_move=()
    if player(board)==X:
        v= -math.inf
        for action in actions(board):
            k=MIN_VALUE(result(board,action))
            if k>v:
                v=k
                best_move=action
    if player(board)==O:
        v=math.inf
        for action in actions(board):
            k=MAX_VALUE(result(board,action))
            if k<v:
                v=k
                best_move=action
    return best_move


    # raise NotImplementedError
def MIN_VALUE(board):
    if terminal(board):
        return utility(board)
    v=math.inf
    for action in actions(board):
        v=min(v,MAX_VALUE(result(board,action)))
        return v
def MAX_VALUE(board):
    if terminal(board):
        return utility(board)
    v=-math.inf
    for action in actions(board):
        v=max(v,MIN_VALUE(result(board,action)))
        return v

if  __name__ == "__main__":
    state = [[O, EMPTY, X],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    won = winner(state)
    print(won)
    # print("change main at line 190")