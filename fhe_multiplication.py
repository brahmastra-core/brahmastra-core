# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

def run_homomorphic_multiplication():
    # 1. Initialize BFV Context
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )

    # Task 3: Attach Relinearization keys to context to manage noise and degree expansion
    context.generate_relin_keys()
    print("[INIT] Context initialized with Relinearization keys enabled.")
    print(f"- Has Relin Keys: {context.has_relin_keys()}")

    # Task 1: Encrypt sample numbers A = 5, B = 10
    a = 5
    b = 10
    enc_a = ts.bfv_vector(context, [a])
    enc_b = ts.bfv_vector(context, [b])
    print(f"[STATUS] Initial Ciphertexts created for A={a} and B={b}")

    # Task 2: Perform Homomorphic Multiplication and track noise expansion handling
    # Multiplying two ciphertexts expands degree from 2 to 3; relinearization restores it back.
    print("[COMPUTE] Performing Homomorphic Multiplication (enc_a * enc_b)...")
    enc_mul = enc_a * enc_b

    # Task 4: Verify decryption within noise budget (Expected: 50)
    result = enc_mul.decrypt()
    print(f"[STATUS] Decrypted Multiplication Result: {result[0]}")

    # Assertion check for accuracy
    assert result[0] == 50, f"Multiplication failed! Expected 50, got {result[0]}"
    print("\033[92m[SUCCESS] Day 11 Verification Passed: Result is 50 within valid noise budget!\033[0m")

if __name__ == "__main__":
    run_homomorphic_multiplication()
