import collections
BoardUnit = collections.namedtuple("BoardUnit", "value score")
Config = collections.namedtuple("Config", "N min_word_length")
Word = collections.namedtuple("Word", "string path")
AbsolutePos = collections.namedtuple("AbsolutePos", 'x y')
RelativePos = collections.namedtuple("RelativePos", 'x y')
TileCoords = collections.namedtuple("TileCoords", 'x y')
Box = collections.namedtuple("Box", 'xMin yMin xMax yMax')

class Board(object):
    def __init__(self,values,scores, N):
        self.tiles = [BoardUnit(pair[0], pair[1]) for pair in zip(values, scores)]
        self.N = N

    def __len__():
        return self.N*self.N

    def __iter__(self):
        return iter(self.tiles)

    def __getitem__(self, coords):
        return self.tiles[coords[0] + coords[1] * self.N]
