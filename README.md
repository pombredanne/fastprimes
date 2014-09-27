fastprimes
==========

Constant time checks if a small number is a prime or composite

Example Output
==============

    $ python fastprimes.py 2 16 10000 1
    Starting the generation of primes with seed [2, 3]
    Finished, generated a total of 10000 primes
    Building 2 hash functions...
    Building an array of length 65536...
    Done.
    False positives 9711, negatives 0, min false pos 4

    $ python fastprimes.py 2 18 10000 2
    Starting the generation of primes with seed [2, 3]
    Finished, generated a total of 10000 primes
    Building 2 hash functions...
    Building an array of length 262144...
    Done.
    False positives 253, negatives 0, min false pos 1023
    Building 2 hash functions...
    Building an array of length 262144...
    Done.
    False positives 227, negatives 0, min false pos 51

    $ python fastprimes.py 3 18 10000 2
    Starting the generation of primes with seed [2, 3]
    Finished, generated a total of 10000 primes
    Building 3 hash functions...
    Building an array of length 262144...
    Done.
    False positives 129, negatives 0, min false pos 125
    Building 3 hash functions...
    Building an array of length 262144...
    Done.
    False positives 106, negatives 0, min false pos 1295
