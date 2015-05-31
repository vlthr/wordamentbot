import unittest
from nose.tools import assert_equals, assert_in, assert_regexp_matches, assert_true, assert_false, istest, nottest
from nose.plugins.attrib import attr
import time
import logging

from wordamentbot.testdefaults import *

from wordamentbot.Solver import BlockingSolver

board = make_one_word_board()

class SolverTest(unittest.TestCase):
    def setUp(self):
        f = make_one_word_wordfile()
        self.solver = BlockingSolver(default_config, board, wordfile=f, use_cache=False)
    def test_wordify(self):
        path = list(zip(range(0,4), [0]*4))
        self.assertEqual(['TEST'],self.solver.wordify(path))
    def test_get_successors(self):
        expected = [(0,1), (1,0), (1,1)]
        self.assertEqual(expected,self.solver.get_successors(((0,0),)))
    def test_get_successors_traversed(self):
        expected = [(0,1), (1,1)]
        self.assertEqual(expected,self.solver.get_successors(((1,0),(0,0))))
    def test_expand_word(self):
        result = self.solver.expand_word(((0,0),))
        self.assertEqual(1,len(result)) # only one word on board
        self.assertEqual("TEST",result[0].string)
    def test_next_word(self):
        self.assertEqual("TEST",self.solver.next_word(block=False).string)
    def test_prefix(self):
        "The first three tiles should be recognized as the prefix to TEST"
        full_path = tuple(zip(range(0,4), [0]*4))
        prefixes = [full_path[:i] for i in range(0,3)]
        for p in prefixes:
            self.assertFalse(self.solver.dead_end(p))
    def test_negative_prefix(self):
        "The full word itself should count as a dead end"
        full_path = tuple(zip(range(0,4), [0]*4))
        self.assertTrue(self.solver.dead_end(full_path))
    def test_path_to_words(self):
        full_path = tuple(zip(range(0,4), [0]*4))
        wordstrings = [word.string for word in self.solver.path_to_words(full_path)]
        self.assertEqual(["TEST"],wordstrings)
    def test_all_subwords(self):
        full_path = tuple(zip(range(0,4), [0]*4))
        wordstrings = [word.string for word in self.solver.all_subwords(full_path)]
        self.assertEqual(["TEST"],wordstrings)

class SolverBoardTestCase(object):
    def init(self):
        """Subclasses set up variables:
            self.wordlist
            self.values
            self.scores
            Then calls base class init() on itself
        """
        import wordamentbot.datatypes
        f = make_wordfile(self.wordlist)
        board = wordamentbot.datatypes.Board(self.values,self.scores,default_config.N)
        self.solver = BlockingSolver(default_config, board,wordfile=f,use_cache=False)
    def find_words(self):
        found = set()
        running = True
        while running:
            try:
                logging.debug("found = %r\n", found  )
                found.add(self.solver.next_word(block=False))
            except:
                running = False
        return found

    def test_finds_words(self):
        found = set([word.string for word in self.find_words()])
        self.assertEqual(set(self.expected),found)
         
class SolverDoublesTest(unittest.TestCase, SolverBoardTestCase):
    def setUp(self):
        self.expected = ["CHINA", "RICH"]
        self.wordlist = self.expected
        self.values = "g d y t i a o a e p n r s r i ch".upper().split()
        self.scores = [int(x) for x in "4 3 5 2 2 2 2 2 1 4 2 2 2 2 2 9".split()]
        SolverBoardTestCase.init(self)

    def test_doesnt_split_double(self):
        "Should not find words including only one of the double chars"
        found = set([word.string for word in self.find_words()])
        self.assertTrue("ARC" not in found)

class SolverEitherTest(unittest.TestCase, SolverBoardTestCase):
    def setUp(self):
        self.expected = ["LIP", "TRUE"]
        self.wordlist = self.expected
        self.values = "e m t d u/l r e w i p d e p o e m".upper().split()
        self.scores = [int(x) for x in "1 4 2 3 20 2 1 6 2 4 3 1 4 2 1 4".split()]
        SolverBoardTestCase.init(self)

    def test_wordify_either(self):
        path = ((2,0), (1,1), (0,1), (0,0))
        wordstrings = self.solver.wordify(path)
        self.assertEqual(wordstrings,["TRUE", "TRLE"])


class SolverEndingTest(unittest.TestCase, SolverBoardTestCase):
    def setUp(self):
        self.expected = ["SPIC", "TONIC"]
        self.wordlist = self.expected + ["ARC"]
        self.values = "o n n e e -ic t o s s p a t e s t".upper().split()
        self.scores = [int(x) for x in "2 2 2 1 1 12 2 2 2 2 4 2 2 1 2 2".split()]
        SolverBoardTestCase.init(self)

    def test_no_ending_successor(self):
        path = ((1,1),)
        self.assertEqual((),self.solver.get_successors(path))

class SolverBeginningTest(unittest.TestCase, SolverBoardTestCase):
    def setUp(self):
        self.expected = ["OVERLY"]
        self.wordlist = self.expected + ["LAYOVER"]
        self.values = "s d r c c e p l e l over- a t s y r".upper().split()
        self.scores = [int(x) for x in "2 3 2 3 3 1 4 3 1 3 12 2 2 2 5 2".split()]
        SolverBoardTestCase.init(self)

    def test_not_beginning_tile(self):
        self.assertTrue(self.solver.not_beginning_tile((0,0)))
        self.assertFalse(self.solver.not_beginning_tile((2,2)))

    def test_no_beginning_successor(self):
        "Tiles with 'beginning' values should not be successors"
        path = ((1,2),)
        self.assertTrue((2,2) not in self.solver.get_successors(path))
    def test_doesnt_append_beginning(self):
        "Should not find words ending with the 'beginning' tile"
        found = set([word.string for word in self.find_words()])
        self.assertTrue("LAYOVER" not in found)
