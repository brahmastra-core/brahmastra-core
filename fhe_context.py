# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

def create_fhe_context():
    # 1. BFV స్కీమ్ కాంటెక్స్ట్ ప్రారంభం
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    
    # 2. హోమోమార్ఫిక్ మల్టిప్లికేషన్ & రొటేషన్ కీల తయారీ
    context.generate_relin_keys()
    context.generate_galois_keys()
    
    print("[SUCCESS] FHE కాంటెక్స్ట్, Relin Keys మరియు Galois Keys విజయవంతంగా తయారయ్యాయి!")
    print(f"- Relin Keys Status: {context.has_relin_keys()}")
    print(f"- Galois Keys Status: {context.has_galois_keys()}")
    print(f"- Secret Key Status: {context.has_secret_key()}")
    
    return context

if __name__ == "__main__":
    create_fhe_context()
