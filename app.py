import streamlit as st

from validators import is_blum_prime, validate_seed
from bbs_core import BlumBlumShub
from analysis import monobit_frequency_test

st.set_page_config(page_title="BBS Generator", layout="wide")

st.title("Blum Blum Shub (BBS) Pseudorandom Bit Generator")
st.markdown("""
This application demonstrates the **Blum Blum Shub (BBS)** Cryptographic Pseudorandom Bit Generator.
Security rests on the computational hardness of the **Quadratic Residuosity Problem** modulo $n = p \\times q$.
""")

st.sidebar.header("Input Parameters")

p_input = st.sidebar.text_input("Prime p", value="499")
q_input = st.sidebar.text_input("Prime q", value="503")
seed_input = st.sidebar.text_input("Initial Seed (s)", value="17")
num_bits = st.sidebar.number_input("Number of Bits to Generate", min_value=1, max_value=10000, value=100)

if st.sidebar.button("Generate Bitstream"):
    try:
        # Sanitize inputs by removing commas and accidental whitespace
        p = int(p_input.replace(",", "").strip())
        q = int(q_input.replace(",", "").strip())
        s = int(seed_input.replace(",", "").strip())
    except ValueError:
        st.error("Inputs p, q, and seed must be valid integers. Letters or symbols are not allowed.")
        st.stop()

    # Validation Phase
    p_valid = is_blum_prime(p)
    q_valid = is_blum_prime(q)

    if not p_valid:
        st.error(f"Invalid p ({p}): Must be a prime number congruent to 3 mod 4.")
    if not q_valid:
        st.error(f"Invalid q ({q}): Must be a prime number congruent to 3 mod 4.")
    if p == q:
        st.error("Primes p and q must be distinct.")

    if not (p_valid and q_valid and p != q):
        st.stop()

    n = p * q
    if not validate_seed(s, n):
        st.error(f"Invalid Seed ({s}): Must satisfy 1 < s < {n - 1} and gcd(s, {n}) == 1.")
        st.stop()

    st.success("All mathematical prerequisites verified successfully.")

    # Execution Phase
    generator = BlumBlumShub(p, q, s)
    bitstream, states = generator.generate_sequence(num_bits)

    col1, col2, col3 = st.columns(3)
    col1.metric("Modulus (n = p × q)", str(n))
    col2.metric("Initial State (x₀ = s² mod n)", str(pow(s, 2, n)))
    col3.metric("Generated Bits", str(len(bitstream)))

    # Manual Calculation Walkthrough
    st.subheader("Manual Calculation (Iteration 1)")
    st.markdown("Demonstrating the exact mathematical steps for the first extracted bit:")
    
    x0 = pow(s, 2, n)
    x1 = pow(x0, 2, n)
    b1 = x1 % 2
    
    st.latex(rf"n = p \times q = {p} \times {q} = {n}")
    st.latex(rf"x_0 = s^2 \bmod n = {s}^2 \bmod {n} = {x0}")
    st.latex(rf"x_1 = x_0^2 \bmod n = {x0}^2 \bmod {n} = {x1}")
    st.latex(rf"b_1 = x_1 \bmod 2 = {x1} \bmod 2 = {b1}")

    st.subheader("Generated Bit Sequence")
    st.code(bitstream, language="text")

    # Statistical Evaluation
    st.subheader("Statistical Randomness Evaluation (Monobit Test)")
    stats = monobit_frequency_test(bitstream)

    st.write(f"Zeroes: {stats['zeroes']} | Ones: {stats['ones']} | Proportion of 1s: {stats['ones_ratio']}")
    st.write(f"Test Statistic (S_obs): {stats['s_obs']} | p-value: {stats['p_value']}")

    if stats["passed"]:
        st.success("Passed Monobit Test (p-value >= 0.01): Bit distribution is statistically uniform.")
    else:
        st.warning("Failed Monobit Test (p-value < 0.01): Non-uniform bit distribution.")

    # State Trace Expander
    with st.expander("View Internal State Trajectory"):
        st.write("State steps $x_i = x_{i-1}^2 \\bmod n$ and extracted LSBs:")
        state_log = [f"Step {i+1}: State = {st_val}, Bit = {st_val % 2}" for i, st_val in enumerate(states)]
        st.text("\n".join(state_log[:100]))
        if len(states) > 100:
            st.caption("Truncated display to first 100 states.")
