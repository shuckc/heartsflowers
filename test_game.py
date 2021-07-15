import pytest
from game import Board, parse_move, piece_push
import numpy as np


def test_parser():
    assert parse_move('N6\n') == ('N', 6)
    assert parse_move('W1') == ('W', 1)
    assert parse_move('N16') == ('N', 16)
    with pytest.raises(ValueError):
        parse_move('A4')

def test_push():
    d = np.zeros([5], dtype=np.int8)
    assert str(d) == '[0 0 0 0 0]'
    d = piece_push(1, d)
    assert str(d) == '[1 0 0 0 0]'
    d = piece_push(2, d)
    assert str(d) == '[2 1 0 0 0]'

    d = np.zeros([5], dtype=np.int8)
    d[2] = 2
    d[4] = 2
    d = piece_push(1, d)
    assert str(d) == '[1 0 2 0 2]'
    d = piece_push(1, d)
    assert str(d) == '[1 1 2 0 2]'
    d = piece_push(1, d)
    assert str(d) == '[1 1 1 2 2]'
    d = piece_push(1, d)
    assert str(d) == '[1 1 1 1 2]'
    d = piece_push(2, d)
    assert str(d) == '[2 1 1 1 1]'

def test_board():
    b = Board(1)
    assert str(b) == '1\n.\n'
    assert b.check() == 0

    b.move('N', 1)
    assert str(b) == '1\nH\n'
    assert b.check() == '1 wins'

    b = Board(2)
    assert str(b) == '2\n..\n..\n'
    assert b.check() == 0

    b.move('N', 1)
    assert str(b) == '2\nH.\n..\n'
    assert str(b.data) == '[[1 0]\n [0 0]]' # verify orientation of numpy grid

    b.move('N', 2)
    assert str(b) == '2\nHF\n..\n'
    assert str(b.data) == '[[1 2]\n [0 0]]'
    assert b.check() == 0

    b.move('W', 1)
    assert str(b) == '2\nHH\n..\n'
    assert str(b.data) == '[[1 1]\n [0 0]]'
    assert b.check() == '1 wins'

def test_big_board():
    b = Board(4)
    b.move('W', 1) # H
    b.move('N', 3) # F
    b.move('W', 2) # H
    b.move('N', 3) # F
    b.move('S', 2) # H
    b.move('S', 3) # F
    assert str(b) == '4\nH.F.\nH.F.\n....\n.HF.\n'
    assert b.check() == None

