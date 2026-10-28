# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

def run_brahmastra_poc():
    # 1. Initialize BFV Context
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )

    # Task 1: Client encrypts A = 5, B = 10 into lattice ciphertexts
    a = 5
    b = 10
    enc_a = ts.bfv_vector(context, [a])
    enc_b = ts.bfv_vector(context, [b])

    # Task 2: Server performs blind addition without decryption
    enc_result = enc_a + enc_b

    # Task 3: Client decrypts result using private key
    result = enc_result.decrypt()

    print("[STATUS] Brahmastra POC Execution:")
    print(f"- Input A: {a}")
    print(f"- Input B: {b}")
    print(f"- Decrypted Result: {result[0]}")

    # Task 4: Assert verification check (5 + 10 == 15)
    assert result[0] == 15, "Verification failed: Result does not match 15!"
    print("\033[92m[SUCCESS] Task 4 Passed: assert result[0] == 15 verified successfully!\033[0m")

if __name__ == "__main__":
    run_brahmastra_poc()
