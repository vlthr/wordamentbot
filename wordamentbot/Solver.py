import queue
import logging
import random
from wordamentbot.utilities import memo, trace
from wordamentbot.datatypes import Word 
def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def get_cached_prefixes(filename):
    import os.path
    if os.path.isfile(filename):
        contents = open(filename).read()
        if len(contents) == 0: raise ValueError("Prefix file is empty.")
        prefixset = set(contents.upper().split())
        return prefixset
    else:
        return None

def write_set_to_file(s, filename):
    f = open(filename, 'w')
    f.write('\n'.join(s))
    f.flush()
    f.close()

def read_word_list(wordfile, use_cache=True):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    contents = wordfile.read()
    if len(contents) == 0: raise ValueError("Word file is empty.")
    wordset = set(contents.upper().split())
    if use_cache:
        prefixfile = wordfile.name + ".prefixes"
        prefixset = get_cached_prefixes(prefixfile)
        if prefixset is None:
            prefixset = set(p for word in wordset for p in prefixes(word))
            write_set_to_file(prefixset, prefixfile)
    else:
        prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

class Solver(object):
    def __init__(self, config, board,wordfile=None,use_cache=True):
        if wordfile is None: wordfile = open('scrabblewordlist.txt')
        self.config = config
        self.board = board
        self.wordset, self.prefixset = read_word_list(wordfile,use_cache=use_cache)
    def next_word(self):
        pass
    @memo
    def wordify(self, path):
        """
        Travels the path and returns the resulting strings.
        
        In case there is only one possibility (no either/or tiles), a list containing one element is returned.
        """
        def expand(word, path):
            """Walks the path as a tree of possible words (branching on either/or tiles) and returns all 
            possible resulting strings"""
            if len(path) == 0:
                return [word]
            tile_val = self.board[path[0]].value
            if tile_val.startswith('-'):
                tile_val = tile_val[1:]
            if tile_val.endswith('-'):
                tile_val = tile_val[:-1]
            if '/' in tile_val:
                first, second = tile_val.split('/')
                result = []
                result.extend(expand(word+first, path[1:]))
                result.extend(expand(word+second, path[1:]))
                return result
            else:
                return expand(word+tile_val, path[1:])
        tile_vals = (self.board[tile].value for tile in path)
        return expand("", path)

    def dead_end(self, path):
        words = self.wordify(path)
        if all(string not in self.prefixset for string in words):
            return True
        else:
            return False

class BlockingSolver(Solver):
    def all_subwords(self, path):
        "Finds all subwords in a given path. Empty list if none found."
        words = []
        for i in range(1,len(path)+1):
            words.extend(self.path_to_words(path[:i]))
        return words

    def path_to_words(self,path):
        "Constructs Words from following the exact path given. Empty list if none found."
        result = []
        words = filter(lambda x: x in self.wordset, self.wordify(path))
        if len(path) >= self.config.min_word_length:
            result.extend([Word(string, path) for string in words])
        return result

    def value_none(self,word):
        return 0
    def value_mix(self,word):
        if random.random() > 0.5:
            score = -sum(self.board[coords].score for coords in word.path)
        else:
            score = sum(self.board[coords].score for coords in word.path)
        if len(word.path) > 7:
            score *= 3
        elif len(word.path) > 5:
            score *= 2
        elif len(word.path) > 3:
            score *= 1.5
        return score

    def value_length(self, word):
        score = -len(word.path)
        if len(word.path) > 7:
            score *= 3
        elif len(word.path) > 5:
            score *= 2
        elif len(word.path) > 3:
            score *= 1.5
        return score
    def value_short(self, word):
        score = sum(self.board[coords].score for coords in word.path)
        if len(word.path) > 7:
            score *= 3
        elif len(word.path) > 5:
            score *= 2
        elif len(word.path) > 3:
            score *= 1.5
        return score
    def value_long(self, word):
        score = -sum(self.board[coords].score for coords in word.path)
        if len(word.path) > 7:
            score *= 3
        elif len(word.path) > 5:
            score *= 2
        elif len(word.path) > 3:
            score *= 1.5
        return score
    @memo
    def expand_word(self, path):
        """
        Moves out recursively in all valid directions from a given path
        """
        def add_suffix(word_path, successor):
            new_path = word_path + (successor,)
            if self.dead_end(new_path):
                return self.all_subwords(new_path)
            else:
                return self.expand_word(new_path)
        successors = self.get_successors(path)
        # logging.debug("successors= %r\n", successors )
        result = []
        for suffix in successors:
            result.extend(add_suffix(path, suffix))
        return result

    def not_beginning_tile(self, coords):
        return not self.board[coords].value.endswith('-')
    @memo
    def get_successors(self, path):
        """
        Returns all adjacent tiles that are eligible as a path
        """
        if self.board[path[-1]].value.startswith('-'): return ()
        traversed = set(path)
        available = set(self.neighbours(path[-1]))
        successors = filter(self.not_beginning_tile, available - traversed)
        return list(successors)

    @memo
    def neighbours(self, currTile):
        """
        Returns all (x,y) neighbours of the current tile as a list
        """
        X = currTile[0]
        Y = currTile[1]
        l = [(x,y) for x in range(X-1, X+2) for y in range(Y-1, Y+2) if 0 <= x < self.config.N if 0 <= y < self.config.N if (x != X or y != Y)]
        return l

    def __init__(self, config, board,wordfile=None, use_cache=True):
        super().__init__(config, board,wordfile=wordfile, use_cache=use_cache)
        self.words = queue.PriorityQueue()
        words = self.solve_all()
        values = map(self.value_long, words)
        seen = set()
        for pair in zip(values,words):
            if pair[1].string in seen:
                continue
            self.words.put(pair)
            seen.add(pair[1].string)
        logging.debug("self.wordset= %r\n", self.wordset )
        logging.debug("self.prefixset= %r\n", self.prefixset )

    def next_word(self,block=True):
        return self.words.get(block)[1]
    
    def solve_all(self):
        """
        Returns a list of Words containing all words on the game board
        """
        tiles = [(x,y) for x in range(0,self.config.N) for y in range(0,self.config.N)]
        result = []
        for tile in tiles:
            result.extend(self.expand_word((tile,)))
        return list(set(result))
