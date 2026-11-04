# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# 1. Generating Private Context
context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=8192,
 plain_modulus=1032193
)
context.generate_relin_keys()
context.generate_galois_keys()

# 2. Private Serialized Data (Retained strictly on client device)
secret_context = context.serialize(save_secret_key=True)

# 3. Extracting Public Context for Server (Zero-Trust)
context.make_context_public()
public_context = context.serialize()

print("[SUCCESS] Public & Private Context Separation Complete!")
print(f"- Server Public Context has Secret Key? {context.has_secret_key()}")
print(f"- Public Context Size: {len(public_context)} bytes")
print(f"- Secret Context Size: {len(secret_context)} bytes")
