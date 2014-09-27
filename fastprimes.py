# fastprimes.py
# Trevor Pottinger
# Sun Sep 14 22:55:00 PDT 2014

import sys

from bloom_filter import BloomFilter

def n_primes(n):
  "Returns the first n primes"
  assert n < (1 << 35), 'Less than 2^35 primes please'
  assert n > 2, 'Less than 2 primes isnt interesting'
  primes = [2, 3]
  print "Starting the generation of primes with seed %s" % str(primes)
  while len(primes) < n:
    possible_prime = primes[-1]
    while True:
      possible_prime += 2
      is_possible = True
      for p in primes:
        if (possible_prime % p) == 0:
          is_possible = False
          break
      if is_possible:
        primes.append(possible_prime)
        break
  print "Finished, generated a total of %d primes" % len(primes)
  return primes

def evaluate(primes, bloomf):
  """Tests every number between the first and last primes, including the
  numbers not in primes. We use the primes array as the source of truth."""
  false_positives, false_negatives = (0, 0)
  min_false_positive = primes[-1] + 1 # not true, but helps logic
  for i in range(primes[0], primes[-1]):
    true_prime = i in primes
    bf_prime = bloomf.contains(i)
    if true_prime and not bf_prime:
      false_negatives += 1
    elif not true_prime and bf_prime:
      false_positives += 1
      if i < min_false_positive:
        min_false_positive = i
  return (false_positives, false_negatives, min_false_positive)

if __name__ == '__main__':
  if len(sys.argv) == 5:
    num_funcs = int(sys.argv[1])
    num_bits = 1 << int(sys.argv[2])
    num_primes = int(sys.argv[3])
    num_iterations = int(sys.argv[4])
  else:
    num_funcs = 2
    num_bits = 1 << 16 # 64K
    num_primes = 10000
    num_iterations = 10
  primes = n_primes(num_primes)
  for _ in range(num_iterations):
    bloom_filter = BloomFilter(num_funcs, num_bits)
    for p in primes[:-1]:
      bloom_filter.add(p)
    (fps, fns, min_fp) = evaluate(primes, bloom_filter)
    print 'False positives %d, negatives %d, min false pos %d' % (fps, fns, min_fp)
