# pdbf.py
# Trevor Pottinger
# Sun Jun 15 10:27:47 PDT 2014

import random

from bloom_filter import bloom_filter

def randD():
  """Returns a random number between 0 and 1"""
  return random.random()

def randB():
  return randD() < 0.5

def randSort():
  r = randD()
  if r < 0.5: return 1
  elif r > 0.5: return -1
  else: return 0

class pdbf():
  def __init__(self, k, m, maxNum, to_build=True):
    self.k = k
    self.m = m
    self.maxNum = maxNum
    self.primes = bloom_filter(k, m, maxNum)
    self.composites = self.primes.deep_copy()
    self.built = False
    if to_build:
      self.__build(showProgress=True)

  def __build(self, showProgress=False):
    ns = ( n for n in range(self.maxNum+1) ) # inclusive range
    if showProgress:
      from tqdm import tqdm
      ns = tqdm(ns, desc='Building disjoint sets', total=self.maxNum)
    for n in ns:
      #print "testing", n,
      if self.isPrime(n):
        #print "prime",
        self.primes.add(n)
      else:
        #print "composite",
        self.composites.add(n)
      #print self.primes.getArrayVal(), self.composites.getArrayVal()
    self.built = True

  def isPrime(self, n):
    return randB()

  def long_message(self):
    config = {
      'num_funcs' : self.k,
      'array_len' : self.m,
      'max_num' : self.maxNum
    }
    return """Prime disjoint bloom filter sets
    %(num_funcs)d number of hash functions that are shared for two
    %(array_len)d long bloom filters, where %(max_num)d is the
    maximum of the checked range""" % config

  def __repr__(self):
    return "pdbf(%d funcs, %d bits, %d max)" % ( self.k, self.m, self.maxNum )

def test_pdbf():
  pass

def pdbf_ord(k, m, N):
  """Returns an initialized pdbf where:
  k num hash funcs
  m order of magnitude of the length of the bit hash arrays
  N order of magnitude of max num"""
  return pdbf(k, 2**m, (2**(2**N)) - 1)
