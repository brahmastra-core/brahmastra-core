# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts
import sys

def run_simd_batching():
    # 1. Initialize BFV Context with SIMD Batching support
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    context.generate_relin_keys()

    # Task 1: Generate batch vectors containing 1,000 integers each
    batch_size = 1000
    vector_a = [i for i in range(1, batch_size + 1)]        # [1, 2, ..., 1000]
    vector_b = [i * 2 for i in range(1, batch_size + 1)]    # [2, 4, ..., 2000]

    # Task 2: Encrypt entire 1,000-integer vectors into single ciphertexts
    print(f"[STATUS] Encrypting {batch_size} elements into SIMD Ciphertext...")
    enc_vector_a = ts.bfv_vector(context, vector_a)
    enc_vector_b = ts.bfv_vector(context, vector_b)

    # Task 3: Perform single parallel homomorphic addition on all 1,000 slots simultaneously
    print("[COMPUTE] Performing parallel SIMD addition (1 operation for 1,000 numbers)...")
    enc_result = enc_vector_a + enc_vector_b

    # Decrypt and verify accuracy
    decrypted_result = enc_result.decrypt()
    expected_result = [a + b for a, b in zip(vector_a, vector_b)]
    assert decrypted_result == expected_result, "SIMD parallel addition verification failed!"
    print(f"[VERIFIED] SIMD parallel addition verified for all {batch_size} elements.")
    print(f"- Sample Slot [0]: {vector_a[0]} + {vector_b[0]} = {decrypted_result[0]}")
    print(f"- Sample Slot [999]: {vector_a[999]} + {vector_b[999]} = {decrypted_result[999]}")

    # Task 4: Memory efficiency analysis (Single Ciphertext vs Naive Individual Encryption)
    single_ciphertext_size = len(enc_vector_a.serialize())
    estimated_naive_size = single_ciphertext_size * batch_size
    memory_savings_ratio = estimated_naive_size / single_ciphertext_size

    print("\n--- [TASK 4: MEMORY SAVINGS ANALYSIS] ---")
    print(f"- SIMD Batched Ciphertext Size: {single_ciphertext_size / 1024:.2f} KB")
    print(f"- Estimated Naive Size (1000 individual ciphertexts): {estimated_naive_size / (1024 * 1024):.2f} MB")
    print(f"- Memory Reduction Factor: ~{memory_savings_ratio:.0f}x efficiency gain")
    print("\033[92m[SUCCESS] Day 12 Tasks (SIMD Batching & Vector Packing) Completed Successfully!\033[0m")

if __name__ == "__main__":
    run_simd_batching()
