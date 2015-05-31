import unittest
from nose.tools import assert_equals, assert_in, assert_regexp_matches, assert_true, assert_false, istest, nottest
from nose.plugins.attrib import attr
import time
import logging 

from wordamentbot.datatypes import Board

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.values = range(0,4*4)
        self.scores = [i%4 for i in range(0,4*4)]
        self.board = Board(self.values,self.scores,4)

    def test_iteration(self):
        for index, tile in enumerate(self.board):
            assert_equals(tile.value,self.values[index])
            assert_equals(tile.score,self.scores[index])
    def test_container_get(self):
        import itertools
        for pair in itertools.combinations_with_replacement(range(0,4),2):
            self.assertEqual(self.board[pair].value,self.values[pair[0] + pair[1]*4])
