import math
from typing import Dict, Any

def monobit_frequency_test(bitstring: str) -> Dict[str, Any]:
    """
    Performs the Monobit (Frequency) Test.
    Evaluates whether the number of 1s and 0s in a sequence are approximately equal.
    """
    n = len(bitstring)
    if n == 0:
        return {"passed": False, "p_value": 0.0, "ones_ratio": 0.0}

    ones = bitstring.count('1')
    zeroes = bitstring.count('0')

    # Calculate test statistic S_obs
    s_obs = abs(ones - zeroes) / math.sqrt(n)

    # Compute complementary error function for p-value estimation
    p_value = math.erfc(s_obs / math.sqrt(2))

    # Threshold for NIST SP 800-22 Monobit test is p-value >= 0.01
    passed = p_value >= 0.01

    return {
        "total_bits": n,
        "zeroes": zeroes,
        "ones": ones,
        "ones_ratio": round(ones / n, 4),
        "s_obs": round(s_obs, 4),
        "p_value": round(p_value, 4),
        "passed": passed
    }
