import unittest
from validators import is_prime_miller_rabin, is_blum_prime, validate_seed
from bbs_core import BlumBlumShub
from analysis import monobit_frequency_test

class TestValidators(unittest.TestCase):
    def test_miller_rabin(self):
        # Edge cases and boundaries
        self.assertFalse(is_prime_miller_rabin(-10))
        self.assertFalse(is_prime_miller_rabin(0))
        self.assertFalse(is_prime_miller_rabin(1))
        
        # Known primes
        self.assertTrue(is_prime_miller_rabin(2))
        self.assertTrue(is_prime_miller_rabin(3))
        self.assertTrue(is_prime_miller_rabin(499))
        self.assertTrue(is_prime_miller_rabin(503))
        
        # Known composites
        self.assertFalse(is_prime_miller_rabin(4))
        self.assertFalse(is_prime_miller_rabin(9))
        self.assertFalse(is_prime_miller_rabin(15))
        self.assertFalse(is_prime_miller_rabin(250997)) # 499 * 503

    def test_blum_prime(self):
        # Valid Blum primes (prime and 3 mod 4)
        self.assertTrue(is_blum_prime(3))
        self.assertTrue(is_blum_prime(7))
        self.assertTrue(is_blum_prime(11))
        self.assertTrue(is_blum_prime(499))
        
        # Primes but 1 mod 4
        self.assertFalse(is_blum_prime(5))
        self.assertFalse(is_blum_prime(13))
        self.assertFalse(is_blum_prime(17))
        
        # Composites that happen to be 3 mod 4
        self.assertFalse(is_blum_prime(15))
        self.assertFalse(is_blum_prime(27))

    def test_seed_validation(self):
        n = 15 # Example modulus: p=3, q=5
        
        # Valid seeds (coprime to 15, strictly between 1 and 14)
        self.assertTrue(validate_seed(2, n))
        self.assertTrue(validate_seed(4, n))
        self.assertTrue(validate_seed(13, n))
        
        # Invalid: out of bounds
        self.assertFalse(validate_seed(1, n))
        self.assertFalse(validate_seed(n - 1, n)) # The 1-lock edge case
        self.assertFalse(validate_seed(n, n))
        self.assertFalse(validate_seed(n + 1, n))
        
        # Invalid: shares a factor with n (GCD != 1)
        self.assertFalse(validate_seed(3, n))
        self.assertFalse(validate_seed(5, n))
        self.assertFalse(validate_seed(10, n))

class TestBBSCore(unittest.TestCase):
    def test_bbs_sequence_generation(self):
        # Manual calculation verification
        # p = 11, q = 19, n = 209
        # s = 3 -> x_0 = 9
        # x_1 = 81 -> b_1 = 1
        # x_2 = 6561 mod 209 = 82 -> b_2 = 0
        # x_3 = 6724 mod 209 = 36 -> b_3 = 0
        bbs = BlumBlumShub(11, 19, 3)
        bitstream, states = bbs.generate_sequence(3)
        
        self.assertEqual(bitstream, "100")
        self.assertEqual(states, [81, 82, 36])

class TestAnalysis(unittest.TestCase):
    def test_monobit(self):
        # Empty string rejection
        stats = monobit_frequency_test("")
        self.assertFalse(stats["passed"])
        
        # Perfectly balanced sequence (should pass easily)
        stats = monobit_frequency_test("1010101010101010")
        self.assertTrue(stats["passed"])
        self.assertEqual(stats["ones"], 8)
        self.assertEqual(stats["zeroes"], 8)
        
        # Highly skewed sequence (should fail)
        stats = monobit_frequency_test("11111111111111111111")
        self.assertFalse(stats["passed"])

if __name__ == '__main__':
    unittest.main()
