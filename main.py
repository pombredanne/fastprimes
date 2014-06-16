# main.py
# Trevor Pottinger
# Sun Jun 15 10:26:02 PDT 2014

from bloom_filter import bloom_filter, test_bf
from pdbf import pdbf, pdbf_ord, test_pdbf

def main():
  # Makes two, disjoint bloom filters. They share three hash functions
  # and have 2^7 or 128 bits. Lastly, the max number is 2^2^3 or 256
  primes = pdbf_ord(3, 7, 3)
  print primes
  print "primes", primes.primes.getArrayRepr()
  print "composites", primes.composites.getArrayRepr()

if __name__ == '__main__':
  main()
  #test_bf()
