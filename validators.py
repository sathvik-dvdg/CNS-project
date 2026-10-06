import math
import random

def is_prime_miller_rabin(n: int, k: int = 40) -> bool:
    """
    Tests primality using the Miller-Rabin probabilistic algorithm.
    k=40 reduces the probability of a false prime to 4^-40, sufficient for this project.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2) if n > 3 else 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def is_blum_prime(p: int) -> bool:
    """
    Verifies that p is prime and satisfies p ≡ 3 (mod 4).
    """
    return is_prime_miller_rabin(p) and (p % 4 == 3)

def validate_seed(s: int, n: int) -> bool:
    """
    Validates that the seed s satisfies 1 < s < n - 1 and gcd(s, n) == 1.
    Strictly bounding below n - 1 prevents the x_0 = 1 infinite sequence flaw.
    """
    return 1 < s < n - 1 and math.gcd(s, n) == 1
