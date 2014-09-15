# bloom_filter.py
# Trevor Pottinger
# Sun Jun 15 10:27:29 PDT 2014

import random
from random import shuffle as rand_shuffle

__primes = [2, 3, 5, 7, 11, 13]

def random_prime(maxN):
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
  return random.choice(filter(lambda n: n < maxN, __primes))

class BloomFilter(object):
  """A naive implementation of bloom filters. Specifically targetting the use
  of two filters, such that they are disjoint subsets of one larger set. The
  result of this is that a bitwise OR of the two results in the bloom filter
  as though the sets were joined"""

  primes = [2]
  primes_inited = False

  # INITIALIZERS

  def __init__(self, num_funcs, num_bits, to_build=True):
    assert num_bits > 64, 'Only more than 64 bits please'
    self.num_funcs = num_funcs
    self.num_bits = num_bits
    # begin needs building
    self.funcs = []
    self.array = 0
    self.array_mask = 0
    self.built = False
    # end needs building
    if to_build:
      self.__build()

  def deep_copy(self):
    copy = BloomFilter(self.num_funcs, self.num_bits, False)
    copy.funcs = list(self.funcs) # is this really a deep copy?
    copy.array = self.array # number assignment is by value
    copy.array_mask = self.array_mask
    return copy

  def __build(self):
    """Generate the necessary hash functions for this bloom filter. A
    hash function takes a number and returns a number in the range 
    [0,num_bits]"""
    assert BloomFilter.primes_inited, 'Primes not initialized'
    print "Building %d hash functions..." % self.num_funcs
    small_enough = lambda prime: prime < self.num_bits
    some_primes = filter(small_enough, BloomFilter.primes)
    rand_shuffle(some_primes) # side effects :(
    def helper(index, primes, num_bits):
      m = primes[2*index]
      b = primes[2*index+1]
      return lambda n: (n*m + b) % self.num_bits
    self.funcs = [ helper(i, some_primes, self.num_bits) for i in range(self.num_funcs) ]
    print "Building an array of length %d..." % self.num_bits
    self.array = 1 << self.num_bits
    self.array_mask = (1 << self.num_bits) - 1
    print "Done."
    self.built = True

  def load(funcs_str, arr_str):
    bf_set = BloomFilter(len(funcs_str.split(":")), len(arr_str) / 2, False)
    bf_set.funcs = [[]] * bf_set.num_funcs # TODO
    bf_set.array = int(arr_str, 16)

  # SETTERS

  @staticmethod
  def setPrimes(primes):
    BloomFilter.primes = primes
    BloomFilter.primes_inited = True

  def add(self, n):
    self.array |= self.get_hash(n)
    return self

  def setArray(self, array):
    self.array = array
    return self

  # GETTERS

  def get_hash(self, n):
    # map hashes on n, results in list of indicies
    hashes = map(lambda f: f(n), self.funcs)
    # map indicies to integer with that bit set
    nums = map(lambda i: 1 << i, hashes)
    return reduce(lambda a, num: a | num, nums, 0)

  def contains(self, n):
    h = self.get_hash(n)
    return h  == (self.array & h)

  def getArrayVal(self):
    return self.array & self.array_mask

  def getArrayRepr(self):
    s = hex(self.getArrayVal()).lstrip('0x').rstrip('L')
    expected_len = self.num_bits / 4 # expected string length
    if len(s) < expected_len:
      return '0' * (expected_len - len(s)) + s
    elif len(s) > expected_len:
      raise Exception("Array longer than expected")
    else:
      return s

  def getFunctionRepr(self):
    return "<function_repr>"

  def __str__(self):
    return hex(self.getArrayVal())[2:-1]

  # end BloomFilter

def test_bf():
  tests = {}

  tests[0] = BloomFilter(3, 128, 255)
  tests[0].add(2**7 + 2**5)
  tests[0].add(2**5 + 2**3)
  print tests[0].getArrayRepr()

  print tests[0].contains(2**7 + 2**5)
  print tests[0].contains(2**5 + 2**3)
  print tests[0].contains(2**5)
