# bloom_filter.py
# Trevor Pottinger
# Sun Jun 15 10:27:29 PDT 2014

import random

__primes = [2, 3, 5, 7, 11, 13]

def random_prime():
  global __primes
  if len(__primes) == 6:
    last_prime = __primes[-1]
    # not actually random...
    for n in range(last_prime+1, 100000):
      is_prime = True
      for i in range(len(__primes)):
        if n % __primes[i] == 0:
          is_prime = False
          break
      if is_prime:
        __primes.append(n)
  # end if
  return random.choice(__primes)

class bloom_filter():
  """A naive implementation of bloom filters. Specifically targetting the use
  of two filters, such that they are disjoint subsets of one larger set. The
  result of this is that a bitwise OR of the two results in the bloom filter
  as though the sets were joined"""

  # INITIALIZERS

  def __init__(self, k, m, maxNum, to_build=True):
    self.k = k
    self.m = m
    self.maxNum = maxNum 
    if to_build:
      self.__build()

  def deep_copy(self):
    copy = bloom_filter(self.k, self.m, self.maxNum, False)
    copy.funcs = self.funcs
    copy.array = self.array # number assignment is by value
    copy.arrayMask = self.arrayMask
    return copy

  def __build(self):
    """Generate the necessary hash functions for this bloom filter. A
    hash function takes a number less than maxNum and returns a number
    in the range [0,m]"""
    print "Building %d hash functions..." % self.k
    def helper():
      m = random_prime()
      b = random_prime()
      print m, "* n +", b
      def hash_func(n):
        return (n*m + b) % (self.m)
      return hash_func
    self.funcs = [ helper() for _ in range(self.k) ]
    print "Building an array of length %d..." % self.m
    self.array = 2 ** long(self.m) # when AND'd with arrayMask
    self.arrayMask = (2 ** long(self.m)) - 1
    print "Done."

  def load(funcs_str, arr_str, maxNum):
    bf_set = bloom_filter(len(funcs_str.split(":")), len(arr_str) / 2, maxNum, False)
    bf_set.funcs = [[]] * bf_set.k # TODO
    bf_set.array = int(arr_str, 16)

  # SETTERS

  def add(self, n):
    # map hashes on n, results in list of indicies
    hashes = map(lambda f: f(n), self.funcs)
    # map indicies to integer with that bit set
    nums = map(lambda i: 1 << i, hashes)
    final_hash = reduce(lambda a, num: a | num, nums, 0)
    self.array |= final_hash
    return self

  def setArray(self, array):
    self.array = array
    return self

  # GETTERS

  def contains(self, n):
    return n  == (self.array & n)

  def getArrayVal(self):
    return self.array & self.arrayMask

  def getArrayRepr(self):
    s = hex(self.getArrayVal()).lstrip('0x').rstrip('L')
    expected_len = self.m / 4 # expected string length
    if len(s) < expected_len:
      return '0' * (expected_len - len(s)) + s
    elif len(s) > expected_len:
      raise Exception("Array longer than expected")
    else:
      return s

  def getFunctionRepr(self):
    return "<function_repr>"

  # end bloom_filter

def test_bf():
  tests = {}

  tests[0] = bloom_filter(3, 128, 255)
  tests[0].add(2**7 + 2**5)
  tests[0].add(2**5 + 2**3)
  print tests[0].getArrayRepr()

  print tests[0].contains(2**3)
  print tests[0].contains(2**5)
  print tests[0].contains(2**4)
