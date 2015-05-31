import unittest
from nose.tools import assert_equals, assert_in, assert_regexp_matches, assert_true, assert_false, istest, nottest
from nose.plugins.attrib import attr
import time
import logging 
from wordamentbot.testdefaults import default_config
from wordamentbot.Interpreter import PytesserInterpreter
from wordamentbot.Scout import Scout
from wordamentbot.Solver import BlockingSolver

def make_mock_grabber(image):
    def mock_grabber(box):
        return image.crop(box)
    return mock_grabber

# class MockScout(object):
#     def __init__(self, image_path):
#         self.valueimgs = create_load_pickled_images(image_path+".values")
#         self.scoreimgs = create_load_pickled_images(image_path+".scores")
#         self.timeimg = create_load_pickled_image(image_path+".scores")


# def create_load_pickled_images(path):
#     import cpickle
#     picklepath = "dpickles/" + path
#     if os.path.isfile(picklepath):
#         img_list = cpickle.load(open(picklepath))
#     else:



@attr('slow')
class ScoutInterpreterTest(unittest.TestCase):
    def setUp(self):
        # TODO NEXT: create mock scout to test interpreter 
        from PIL import Image
        self.grabber = make_mock_grabber(Image.open("images/1920x1080.png"))
        self.values = ["R", 'S', 'A', 'L', 'T', 'R', 'S', 'H', 'O', 'O', 'A', 'U', 'H', 'S', 'RE', 'C']
        self.scores = [int(x) for x in "2 2 2 3 2 2 2 4 2 2 2 4 4 2 7 3".split()]
        self.scout = Scout(default_config, grabber=self.grabber)
        self.interpreter = PytesserInterpreter(self.scout, default_config)
    def test_values(self):
        self.assertEqual(self.interpreter.get_values(), self.values)
    def test_scores(self):
        self.assertEqual(self.interpreter.get_scores(), self.scores)
    def test_board(self):
        self.assertEqual([unit.value for unit in self.interpreter.get_board()],self.values)
    def test_get_time(self):
        self.assertEqual(42,self.interpreter.get_time())
@attr('slow')
class ScoutInterpreterPlainTest(unittest.TestCase):
    def setUp(self):
        # TODO NEXT: create mock scout to test interpreter 
        from PIL import Image
        self.grabber = make_mock_grabber(Image.open("images/1920x1080_plain.png"))
        self.values = "i o p f v a l n e e y i n i r s".upper().split()
        self.scores = [int(x) for x in "2 2 4 5 6 2 3 2 1 1 5 2 2 2 2 2".split()]
        self.scout = Scout(default_config, grabber=self.grabber)
        self.interpreter = PytesserInterpreter(self.scout, default_config)
    def test_values(self):
        self.assertEqual(self.interpreter.get_values(), self.values)
    def test_scores(self):
        self.assertEqual(self.interpreter.get_scores(), self.scores)
    def test_board(self):
        self.assertEqual([unit.value for unit in self.interpreter.get_board()],self.values)
    def test_get_time(self):
        self.assertEqual(116,self.interpreter.get_time())
@attr('slow')
class ScoutInterpreterDoublesTest(unittest.TestCase):
    def setUp(self):
        # TODO NEXT: create mock scout to test interpreter 
        from PIL import Image
        self.grabber = make_mock_grabber(Image.open("images/1920x1080_double.png"))
        self.values = "g d y t i a o a e p n r s r i ch".upper().split()
        self.scores = [int(x) for x in "4 3 5 2 2 2 2 2 1 4 2 2 2 2 2 9".split()]
        self.scout = Scout(default_config, grabber=self.grabber)
        self.interpreter = PytesserInterpreter(self.scout, default_config)
    def test_values(self):
        self.assertEqual(self.interpreter.get_values(), self.values)
    def test_scores(self):
        self.assertEqual(self.interpreter.get_scores(), self.scores)
    def test_board(self):
        self.assertEqual([unit.value for unit in self.interpreter.get_board()],self.values)
@attr('slow')
class ScoutInterpreterWordEndingTest(unittest.TestCase):
    def setUp(self):
        # TODO NEXT: create mock scout to test interpreter 
        from PIL import Image
        self.grabber = make_mock_grabber(Image.open("images/1920x1080_word_ending.png"))
        self.values = "o n n e e -ic t o s s p a t e s t".upper().split()
        self.scores = [int(x) for x in "2 2 2 1 1 12 2 2 2 2 4 2 2 1 2 2".split()]
        self.scout = Scout(default_config, grabber=self.grabber)
        self.interpreter = PytesserInterpreter(self.scout, default_config)
    def test_values(self):
        self.assertEqual(self.interpreter.get_values(), self.values)
    def test_scores(self):
        self.assertEqual(self.interpreter.get_scores(), self.scores)
    def test_board(self):
        self.assertEqual([unit.value for unit in self.interpreter.get_board()],self.values)
