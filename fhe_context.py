# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

def create_fhe_context():
 # 1. Initializing BFV Scheme Context
 context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=8192,
 plain_modulus=1032193
 )
 
 # 2. Generating Homomorphic Multiplication & Rotation Keys
 context.generate_relin_keys()
 context.generate_galois_keys()
 
 print("[SUCCESS] FHE Context, Relin Keys and Galois Keys successfully generated !")
 print(f"- Relin Keys Status: {context.has_relin_keys()}")
 print(f"- Galois Keys Status: {context.has_galois_keys()}")
 print(f"- Secret Key Status: {context.has_secret_key()}")
 
 return context

if __name__ == "__main__":
 create_fhe_context()
