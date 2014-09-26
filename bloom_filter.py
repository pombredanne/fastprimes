# bloom_filter.py
# Trevor Pottinger
# Sun Jun 15 10:27:29 PDT 2014

import random
from random import shuffle as rand_shuffle
from random import randint as rand_num
from fractions import gcd

__primes = [2, 3, 5, 7, 11, 13]

def _is_coprime(a, b):
  return gcd(a, b) == 1

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
    assert num_bits != 0 and ((num_bits & (num_bits - 1)) == 0), 'Only powers of two for now please'
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

  @staticmethod
  def __hash_builder(num_bits):
    "Returns a linear congruence function"
    assert num_bits > 0, 'Cant make an LCG for 0 modulus'
    c = rand_num(0, num_bits-1)
    while not _is_coprime(c, num_bits):
      c = rand_num(0, num_bits-1)
    a = rand_num(1, num_bits-1)
    # second and third requirements of Hull-Dobell Theorem, respectively
    # see http://en.wikipedia.org/wiki/Linear_congruential_generator
    # the first requirement is this easy because num_bits must be a power of 2
    #while (a - 1 % 2 != 0) or (a - 1 % 4 != 0):
    while (a - 1 % 4 == 0):
      a = rand_num(1, num_bits-1)
    def __chunks(n):
      "Breaks n up into smaller ints, so each one is smaller than num_bits"
      ns = []
      while n != 0:
        ns.append(n % num_bits)
        n = n / num_bits
      return ns
    print a, c, num_bits
    def __hash(n):
      ns = __chunks(n)
      x = (a * ns[0] + c) % num_bits
      for i in range(1, len(ns)):
        # this doesnt quite smell right, b/c x is reused
        x = (x + a * ns[i] + c) % num_bits
      return x
    return __hash

  def __build(self):
    """Generate the necessary hash functions for this bloom filter. A
    hash function takes a number and returns a number in the range 
    [0,num_bits]"""
    assert BloomFilter.primes_inited, 'Primes not initialized'
    print "Building %d hash functions..." % self.num_funcs
    small_enough = lambda prime: prime < self.num_bits
    some_primes = filter(small_enough, BloomFilter.primes)
    rand_shuffle(some_primes) # side effects :(
    self.funcs = [ BloomFilter.__hash_builder(self.num_bits) for _ in range(self.num_funcs) ]
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
