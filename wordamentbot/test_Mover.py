import unittest
from nose.tools import assert_equals, assert_in, assert_regexp_matches, assert_true, assert_false, istest, nottest
from unittest.mock import MagicMock
from nose.plugins.attrib import attr
import time
import logging 
from wordamentbot.testdefaults import default_config
from wordamentbot.Mover import Mover
from wordamentbot.Scout import Scout

def make_mock_scout():
    def identity(arg):
        return arg
    scout = MagicMock()
    scout.coords_to_pos = MagicMock(side_effect=identity)
    return scout

def make_mock_api():
    api = MagicMock()
    api.set_mouse = MagicMock()
    api.left_down = MagicMock()
    api.left_up = MagicMock()
    return api

class MoverTest(unittest.TestCase):
    def setUp(self):
        self.scout = make_mock_scout()
        self.api = make_mock_api()
        self.mover = Mover(self.scout, default_config, api=self.api)
    def test_button(self):
        path = zip(range(0,4), [0]*4)
        self.mover.move(path)
        self.api.left_down.assert_called_once_with()
        self.api.left_up.assert_called_once_with()
    def test_row(self):
        path = zip(range(0,4), [0]*4)
        self.mover.move(path)
        calls = [nose.call(coords) for coords in path]
        self.api.set_mouse.assert_has_calls(calls)
