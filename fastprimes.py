# fastprimes.py
# Trevor Pottinger
# Sun Sep 14 22:55:00 PDT 2014

from bloom_filter import BloomFilter

def n_primes(n):
  "Returns the first n primes"
  assert n < (1 << 35), 'Less than 2^35 primes please'
  assert n > 2, 'Less than 2 primes isnt interesting'
  primes = [2, 3]
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
  return primes

if __name__ == '__main__':
  primes = n_primes(4000) # len(n_primes(n)) == n
  BloomFilter.setPrimes(primes)
  num_bits = 1 << 16 # 64K
  num_funcs = 3
  bloom_filter = BloomFilter(num_funcs, num_bits)
  for p in primes[:-1]:
    bloom_filter.add(p)
  print bloom_filter
