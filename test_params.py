# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# BFV స్కీమ్ పారామీటర్ల సెటప్
poly_mod_degree = 8192
plain_mod = 1032193

context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=poly_mod_degree,
    plain_modulus=plain_mod
)

print("[SUCCESS] BFV స్కీమ్ పారామీటర్లు ఖచ్చితంగా సెట్ అయ్యాయి!")
print(f"Polynomial Modulus Degree: {poly_mod_degree}")
print(f"Plain Modulus: {plain_mod}")
print(f"Is Context Public? {context.is_public()}")
