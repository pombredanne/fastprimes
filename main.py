# main.py
# Trevor Pottinger
# Sun Jun 15 10:26:02 PDT 2014

from bloom_filter import bloom_filter, test_bf
from pdbf import pdbf, pdbf_ord, test_pdbf

def main():
  primes = pdbf_ord(3, 7, 3)
  print primes

if __name__ == '__main__':
  main()
  test_bf()
