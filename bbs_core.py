from typing import List, Tuple

class BlumBlumShub:
    def __init__(self, p: int, q: int, seed: int):
        self.p = p
        self.q = q
        self.n = p * q
        self.seed = seed
        # x_0 = s^2 mod n
        self.current_state = pow(seed, 2, self.n)

    def next_bit(self) -> Tuple[int, int]:
        """
        Advances the state machine by one step.
        Returns a tuple: (extracted_bit, new_state)
        """
        self.current_state = pow(self.current_state, 2, self.n)
        bit = self.current_state % 2  # Extract LSB
        return bit, self.current_state

    def generate_sequence(self, num_bits: int) -> Tuple[str, List[int]]:
        """
        Generates a sequence of pseudorandom bits of length `num_bits`.
        Returns the bitstring and the list of internal states.
        """
        bits = []
        states = []
        for _ in range(num_bits):
            bit, state = self.next_bit()
            bits.append(str(bit))
            states.append(state)
        return "".join(bits), states
