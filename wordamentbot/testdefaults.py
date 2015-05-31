from wordamentbot.datatypes import Board, Config

default_config=Config(4, 2)

def make_wordfile(words):
    import tempfile
    f = tempfile.TemporaryFile(mode='r+')
    f.write('\n'.join(words))
    f.flush()
    f.seek(0)
    return f
def make_one_word_wordfile():
    return make_wordfile(['TEST'])
def make_one_word_board():
    values = 'T E S T _ _ _ _ _ _ _ _ _ _ _ _'.upper().split()
    scores = [i%4 for i in range(0,4*4)]
    board = Board(values,scores,4)
    return board
