# pdbf.py
# Trevor Pottinger
# Sun Jun 15 10:27:47 PDT 2014

from bloom_filter import bloom_filter

class pdbf():
  def __init__(self, k, m, n):
    self.k = k
    self.m = m
    self.n = n
    self.primes = bloom_filter(k, m, n)
    self.composites = self.primes.deep_copy()

  def long_message(self):
    config = {
      'num_funcs' : self.k,
      'array_len' : self.m,
      'max_num' : self.n
    }
    return """Prime disjoint bloom filter sets
    %(num_funcs)d number of hash functions that are shared for two
    %(array_len)d long bloom filters, where %(max_num)d is the
    maximum of the checked range""" % config

  def __repr__(self):
    return "pdbf(%d funcs, %d bits, %d max)" % ( self.k, self.m, self.n )

def test_pdbf():
  pass

def pdbf_ord(k, m, N):
  """Returns an initialized pdbf where:
  k num hash funcs
  m order of magnitude of the length of the bit hash arrays
  N order of magnitude of max num"""
  return pdbf(k, 2**m, (2**(2**N)) - 1)
