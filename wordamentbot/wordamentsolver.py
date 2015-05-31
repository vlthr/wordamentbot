import math
import collections

# ------------------------ DECORATORS
def decorator(d):
	" Make function d a decorator: d wraps a function fn."
	import functools
	def _d(fn):
		return functools.update_wrapper(d(fn),fn)
	functools.update_wrapper(_d, d)
	return _d

@decorator
def verbose(f):
	"Wrap a function to print all arguments and the output"
	def _f(*args):
		argstypes = map(type, args)
		print("*** START Function: ",f.__name__,"(", zip(args,argstypes),")")
		result = f(*args)
		resulttype = type(result)
		print("*** END Function:",f.__name__,"--->",result,"<-- of type", resulttype)
		return result
	return _f

@decorator
def memo(f):
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			cache[args] = result = f(*args)
			return result
		except TypeError:
			return f(*args)
	return _f

@decorator
def trace(f):
	indent = '	'
	def _f(*args):
		signature = '%s(%s)' % (f.__name__, ', '.join(map(repr,args)))
		print('%s--> %s' % (trace.level*indent, signature))
		trace.level += 1
		try:
			result = f(*args)
			print('%s<-- %s === %s' % ((trace.level-1)*indent, signature, result))
		finally:
			trace.level -= 1
		return result
	trace.level = 0
	return _f


# ------------------------ END DECORATORS
# BOGGLE / WORDAMENT SOLVER

# -----------------
# User Instructions
# 
# In this problem, you will define a function, boggle_words(), 
# that takes a board as input and returns a set of words that
# can be made from the board according to the rules of Boggle.

@trace
def boggle_words(board, minlength=3):
	"Find all the words on this Boggle board; return as a set of words."
	l = [expandword(index, getsuccessors(index, board), board, minlength) for index in squareindices(board)]
	fl = flatten(l)
	print(fl)
	return set(fl)

#@trace
@memo
def expandword(indexes, successors, board, minlength):
	#@trace
	@memo
	def addsuffix(word, suffix, board, minlength):
		newword = word + suffix
		wordstring = wordify(newword, board)
		if wordstring not in PREFIXES:
			return allwords(wordify(newword, board), minlength)
		else: return expandword(newword, getsuccessors(newword, board), board, minlength)
	result = [addsuffix(indexes, [suffix], board, minlength) for suffix in successors]
	return result

#@trace
def getsuccessors(sequence, board):
	traversed = set(sequence)
	available = set(neighbors(sequence[-1], size(board)))
	available = set([i for i in available if board[i] is not BORDER])
	return list(available - traversed)

def neighbors(i, N):
    return (i-N-1, i-N, i-N+1, i-1, i+1, i+N-1, i+N, i+N+1)

#@trace
def allwords(string, minlength):
	return [string[:i] for i in range(1,len(string)+1) if string[:i] in WORDS if i >= minlength]
    
#@trace
def squareindices(board):
	# returns the index of all valid squares where each index is itself a length 1 list
	boardsize = size(board)
	return [[i] for i in range(boardsize, len(board)-boardsize) if (i%boardsize is not 0) and (i%boardsize is not boardsize-1)]
    

def startnewgame():
	b = Board(raw_input())
	for w in sorted(list(boggle_words(b)), key=len):
		print(w)


def test():
	b = Board('X X X X T E S T X X X X X X X X')
	assert getsuccessors([7], b) == [8, 13, 14]
	assert b == '|||||||XXXX||TEST||XXXX||XXXX|||||||'
	print(display(b))
#	assert boggle_words(b) == set(['SET', 'SEX', 'TEST'])
	assert neighbors(20, 6) == (13, 14, 15, 19, 21, 25, 26, 27)
#	assert len(boggle_words(Board('TPLER ORAIS METND DASEU NOWRB'))) == 317
#	assert boggle_words(Board('PLAY THIS WORD GAME')) == set([
#		'LID', 'SIR', 'OAR', 'LIS', 'RAG', 'SAL', 'RAM', 'RAW', 'SAY', 'RID', 
#		'RIA', 'THO', 'HAY', 'MAR', 'HAS', 'AYS', 'PHI', 'OIL', 'MAW', 'THIS', 
#		'LAY', 'RHO', 'PHT', 'PLAYS', 'ASIDE', 'ROM', 'RIDE', 'ROT', 'ROW', 'MAG', 
#		'THIRD', 'WOT', 'MORE', 'WOG', 'WORE', 'SAID', 'MOR', 'SAIL', 'MOW', 'MOT', 
#		'LAID', 'MOA', 'LAS', 'MOG', 'AGO', 'IDS', 'HAIR', 'GAME', 'REM', 'HOME', 
#		'RED', 'WORD', 'WHA', 'WHO', 'WHOM', 'YID', 'DRAW', 'WAG', 'SRI', 'TOW', 
#		'DRAG', 'YAH', 'WAR', 'MED', 'HIRE', 'TOWARDS', 'ORS', 'ALT', 'ORE', 'SIDE', 
#		'ALP', 'ORA', 'TWA', 'ERS', 'TOR', 'TWO', 'AIS', 'AIR', 'AIL', 'ERA', 'TOM', 
#		'AID', 'TOG', 'DIS', 'HIS', 'GAR', 'GAM', 'HID', 'HOG', 'PLAY', 'GOA', 'HOW', 
#		'HOT', 'WARM', 'GOT', 'IRE', 'GOR', 'ARS', 'ARM', 'ARE', 'TOWARD', 'THROW'])    
	return 'tests pass'


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

    
def Board(text,rowlen=4):
	"""Input is a string of space-separated rows of N letters each;
	result is a string of size (N+2)**2 with borders all around."""
	rows = [''.join(text[i:(i+1)*rowlen].split()) for i in range(rowlen)]
	N = len(rows)
	rows = [BORDER*N] + rows + [BORDER*N]
	return ''.join(BORDER + row + BORDER for row in rows)

#@trace
def size(board): return int(len(board)**0.5)


BORDER = '|'

def display(board):
    "Return a string representation of board, suitable for printing."
    N = size(board)
    return '\n'.join(board[i:i+N] for i in range(0, N**2, N))


#@trace
def wordify(sequence,board):
	result = []
	for i in sequence:
		result.append(board[i])
	return ''.join(result)

# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset



if __name__ == '__main__':
	WORDS, PREFIXES = readwordlist('words4k.txt')
	startnewgame()



