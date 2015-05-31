def tassert(fn, expanswer, *args, **kwargs):
	"Replacement for an assert statement"
	result = fn(*args, **kwargs)
	if result != expanswer:
		print('-'*20)
		print('		Returned: ', result)
		print('		Expected: ', expanswer)
		raw_input('Press any button to continue...')
	return result

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
	def _f(*args, **kwargs):
		argstypes = map(type, args, kwargs)
		print("*** START Function: ",f.__name__,"(", zip(args,argstypes),")")
		result = f(*args, **kwargs)
		resulttype = type(result)
		print("*** END Function:",f.__name__,"--->",result,"<-- of type", resulttype)
		return result
	return _f

@decorator
def memo(f):
	cache = {}
	def _f(*args, **kwargs):
		try:
			return cache[args]
		except KeyError:
			cache[args] = result = f(*args, **kwargs)
			return result
		except TypeError:
			return f(*args, **kwargs)
	return _f

@decorator
def trace(f):
	indent = '	'
	def _f(*args, **kwargs):
		signature = '%s(%s)' % (f.__name__, ', '.join(map(repr,args)))
		print('%s--> %s' % (trace.level*indent, signature))
		trace.level += 1
		try:
			result = f(*args, **kwargs)
			print('%s<-- %s === %s' % ((trace.level-1)*indent, signature, result))
		finally:
			trace.level -= 1
		return result
	trace.level = 0
	return _f

class countcalls(object):
   "Decorator that keeps track of the number of times a function is called. Use normal decorator notation to apply, then access logs with countcalls.counts()"
   __instances = {}

   def __init__(self, f):
      self.__f = f
      self.__numcalls = 0
      countcalls.__instances[f] = self

   def __call__(self, *args, **kwargs):
      self.__numcalls += 1
      return self.__f(*args, **kwargs)

   @staticmethod
   def count(f):
      "Return the number of times the function f was called."
      return countcalls.__instances[f].__numcalls

   @staticmethod
   def counts():
      "Return a dict of {function: # of calls} for all registered functions."
      return dict([(f, countcalls.count(f)) for f in countcalls.__instances])




