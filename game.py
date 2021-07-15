import argparse
import subprocess
import numpy as np
import re

def piece_push(piece: int, nd):
    # nd is 1 dimensional array
    assert len(nd.shape) == 1
    # push at 0th position, shuffling down until we find empty slot
    for i in range(len(nd)):
        old = nd[i]
        nd[i] = piece
        if old == 0:
            break
        piece = old
    return nd

class Board:
    def __init__(self, n):
        self.n = n
        self.data = np.zeros([n, n], dtype=np.int8)
        self.moves = 0
    def __repr__(self):
        return "{}\n".format(self.n) + "\n".join(
            [
                "".join([".HF"[self.data[i, j]] for j in range(self.n)])
                for i in range(self.n)
            ]
        ) + '\n'

    def move(self, side, index):
        player = self.moves % 2
        piece = 1 + player
        print("Player {} moves {} {}".format(piece, side, index))
        self.moves += 1
        i = index - 1
        d = self.data
        if side == 'N':
            d[:,i] = piece_push(piece, d[:,i])
        elif side == 'S':
            d[:,i] = np.flip(piece_push(piece, np.flip(d[:,i])))
        elif side == 'E':
            d[i,:] = np.flip(piece_push(piece, np.flip(d[i,:])))
        elif side == 'W':
            d[i,:] = piece_push(piece, d[i,:])

    def check(self):
        # check for conditions that prevent a future move, ie. draw, win
        if self.moves > 2 * (self.n ** 2):
            return "draw (out of time)"
        # TODO: simultanious win is a draw
        for i in range(self.n):
            if np.all(self.data[i,:] == 1):
                return '1 wins'
            if np.all(self.data[i,:] == 2):
                return '2 wins'
            if np.all(self.data[:,i] == 1):
                return '1 wins'
            if np.all(self.data[:,i] == 2):
                return '2 wins'
        return None

def parse_move(stext: str):
    c = stext[0].upper()
    'NSEW'.index(c)
    i = int(stext.strip()[1:])
    return (c, i)


if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('players', type=str, nargs=2, help='player binaries (2)')
    parser.add_argument('-n', action='store', default=4, help='size of board')
    args = parser.parse_args()
    board = Board(args.n)

    print('Players {} vs {}'.format(args.players[0], args.players[1]))

    for i in range(9999999):
        player = i % 2
        procname = args.players[player]
        b = str(board)
        cp = subprocess.run(
            procname, text=True, input=b, capture_output=True, shell=True, timeout=30
        )
        board.move(*parse_move(cp.stdout))
        if board.check():
            print(board.check())
            print(board)
            exit()
    print(board)

