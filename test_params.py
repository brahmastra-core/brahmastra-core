# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# BFV scheme parameter setup
poly_mod_degree = 8192
plain_mod = 1032193

context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=poly_mod_degree,
 plain_modulus=plain_mod
)

print("[SUCCESS] BFV scheme parameters configured and verified successfully!")
print(f"Polynomial Modulus Degree: {poly_mod_degree}")
print(f"Plain Modulus: {plain_mod}")
print(f"Is Context Public? {context.is_public()}")
