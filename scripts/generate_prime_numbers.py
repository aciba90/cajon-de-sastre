from sympy import prime
from string import ascii_lowercase, ascii_uppercase

primes_lookup = dict()
for i, (letter_up, letter_down) in enumerate(zip(ascii_uppercase, ascii_lowercase)):
    prime_ = prime(i + 1)
    primes_lookup.update(
        {
            letter_up: prime_,
            letter_down: prime_,
        }
    )

print(primes_lookup)