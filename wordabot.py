import sys
import logging
import time
from wordamentbot.utilities import trace, memo, tassert
from wordamentbot.Scout import Scout
from wordamentbot.Interpreter import Interpreter, PytesserInterpreter
from wordamentbot.Solver import BlockingSolver
from wordamentbot.Mover import Mover


## Globals
# --------------
from wordamentbot.datatypes import Config 
WORKDIR = './'
N = 4
ROWLEN = 4
MINLENGTH = 2
BOARD = []
B_TO_V = {}
PREFIXES = []
WORDS = []
CONFIG = Config(N, 2)

def botloop():
    word_cap = 200
    while True:
        scout = Scout(CONFIG)
        print("Starting board interpreter...")
        interpreter = PytesserInterpreter(scout, CONFIG)
        print("Finished interpreting board. Starting solver...")
        board = interpreter.get_board()
        solver = BlockingSolver(CONFIG, board)
        mover = Mover(scout, CONFIG)
        time_left = interpreter.get_time()
        start_time = time.clock()
        end_time = start_time + time_left - 10
        print("Bot session starting. Continuing until %s",  end_time)
        n = 0
        # logging.warn("solver.words = %r\n", solver.solve_all()  )
        while (time.clock() < end_time):
            word = solver.next_word()
            print("Moving %s" % word.string)
            mover.move(word.path)
            n+=1
            if n == word_cap:
                break
        time.sleep(max([end_time-time.clock(),0]) + 55)

if __name__ == '__main__':
    botloop()
