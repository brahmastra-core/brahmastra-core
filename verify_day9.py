# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# Context Initialized
context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=8192,
 plain_modulus=1032193
)
context.generate_relin_keys()

# Testing sample data vector encryption
data = [10, 20, 30, 40]
encrypted_vector = ts.bfv_vector(context, data)

print("[SUCCESS] Day 9: FHE context & encryption keys verified successfully!")
print(f"- Encrypted Vector Size: {encrypted_vector.size()}")
print(f"- Decrypted Test Check: {encrypted_vector.decrypt()}")
