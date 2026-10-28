# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# 1. ప్రైవేట్ కాంటెక్స్ట్ తయారీ
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=8192,
    plain_modulus=1032193
)
context.generate_relin_keys()
context.generate_galois_keys()

# 2. ప్రైవేట్ సీరియలైజ్డ్ డేటా (క్లయింట్ దగ్గరే భద్రంగా ఉంటుంది)
secret_context = context.serialize(save_secret_key=True)

# 3. సర్వర్ కోసం పబ్లిక్ కాంటెక్స్ట్‌ను వేరుచేయడం (Zero-Trust)
context.make_context_public()
public_context = context.serialize()

print("[SUCCESS] పబ్లిక్ & ప్రైవేట్ కాంటెక్స్ట్‌ల విభజన పూర్తయింది!")
print(f"- Server Public Context has Secret Key? {context.has_secret_key()}")
print(f"- Public Context Size: {len(public_context)} bytes")
print(f"- Secret Context Size: {len(secret_context)} bytes")
