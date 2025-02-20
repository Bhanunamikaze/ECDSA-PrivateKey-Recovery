# ECDSA-PrivateKey-Recovery
## Recovering ECDSA Private Key from JWT Signatures

This repository demonstrates a method to recover an ECDSA private key when the same ephemeral key (`k`) is reused in multiple JWT signatures. This script extracts the necessary parameters from two JWTs, performs the cryptographic calculations as explained below, and derives the private key.

##  Explanation
ECDSA signatures rely on a random nonce (`k`). If `k` is reused across different messages, it becomes possible to derive the private key using basic algebraic manipulation of the signature equation.

An ECDSA signature consists of two values `(r, s)`, computed as:
```math
r = (kG).x \mod q
```

```math
s = k^{-1} (H(m) + d \cdot r) \mod q
```

If the same `k` is reused for two different messages (`m1` and `m2`), we get:
```math
s1 = k^{-1} (H(m1) + d \cdot r) \mod q
```

```math
s2 = k^{-1} (H(m2) + d \cdot r) \mod q
```

By subtracting these equations and solving for `d`, we recover the private key:
```math
d = \frac{s2 H(m1) - s1 H(m2)}{r (s1 - s2)} \mod q
```

The script automates this process by:
1. Parsing two JWTs to extract the signature values (`r`, `s1`, and `s2`).
2. Computing the message hashes (`H(m1)` and `H(m2)`).
3. Performing modular arithmetic to recover `d`.

### Steps Involved:
1. Extract the signatures from two JWTs signed using the same `k`.
2. Compute the SHA-256 hash of each JWT's header and payload.
3. Solve for the private key (`d`) using modular arithmetic.
4. Output the recovered private key.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Bhanunamikaze/ECDSA-PrivateKey-Recovery.git
   cd ECDSA-PrivateKey-Recovery
   ```

2. Install dependencies:
   ```bash
   pip install ecdsa pycryptodome libnum
   ```

3. Run the script:
   ```bash
   #Update JWT keys in teh code and run the below command to Recover Private Key
   python ECDSA-PrivateKey-Recovery.py
   
   Expected Output: Recovered private key (d): 1234567890123456789037412598746321544155
   
   ```

## Disclaimer

This project is for educational and research purposes only. Unauthorized use of cryptographic exploits may violate applicable laws and regulations.

## License

This project is licensed under the MIT License.
