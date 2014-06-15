# bloom_filter.py
# Trevor Pottinger
# Sun Jun 15 10:27:29 PDT 2014

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
    self.array = 2 ** long(m) # when OR'd with maxNum, it equals 0
    if to_build:
      self.__build()

  def deep_copy(self):
    copy = bloom_filter(self.k, self.m, self.maxNum, False)
    copy.funcs = self.funcs
    return copy

  def __build(self):
    """Generate the necessary hash functions for this bloom filter"""
    print "Building %d hash functions..." % self.k
    self.funcs = [ lambda x: x ] * self.k
    print "Done."

  # SETTERS

  def add(self, n):
    self.array |= n

  def contains(self, n):
    return n  == (self.array & n)

  # GETTERS

  def getArrayVal(self):
    return self.array & self.maxNum

  def getArrayRepr(self):
    return hex(self.getArrayVal()).lstrip('0x').rstrip('L')

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