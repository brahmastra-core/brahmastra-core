# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

def run_homomorphic_arithmetic():
    # 1. Initialize BFV Context
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    context.generate_relin_keys()

    # 2. Define sample raw datasets
    vector_a = [150, 300, 450, 600]
    vector_b = [50, 100, 150, 200]

    # 3. Encrypt vectors client-side
    enc_a = ts.bfv_vector(context, vector_a)
    enc_b = ts.bfv_vector(context, vector_b)

    # 4. Perform Homomorphic Operations without decryption
    enc_add = enc_a + enc_b
    enc_sub = enc_a - enc_b

    # 5. Verify results by decrypting locally
    dec_add = enc_add.decrypt()
    dec_sub = enc_sub.decrypt()

    print("[STATUS] Homomorphic Arithmetic Execution Complete.")
    print(f"Original A: {vector_a}")
    print(f"Original B: {vector_b}")
    print(f"Homomorphic Addition Result (A + B): {dec_add}")
    print(f"Homomorphic Subtraction Result (A - B): {dec_sub}")

    # Automated verification checks
    assert dec_add == [200, 400, 600, 800], "Addition verification failed!"
    assert dec_sub == [100, 200, 300, 400], "Subtraction verification failed!"
    print("[VERIFIED] All cryptographic assertions passed successfully.")

if __name__ == "__main__":
    run_homomorphic_arithmetic()
