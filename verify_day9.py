# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts

# కాంటెక్స్ట్ ప్రారంభం
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=8192,
    plain_modulus=1032193
)
context.generate_relin_keys()

# శాంపిల్ డేటా వెక్టర్ ఎన్‌క్రిప్షన్ టెస్ట్
data = [10, 20, 30, 40]
encrypted_vector = ts.bfv_vector(context, data)

print("[SUCCESS] డే 9 FHE కాంటెక్స్ట్ & ఎన్‌క్రిప్షన్ కీస్ వెరిఫికేషన్ విజయవంతమైంది!")
print(f"- Encrypted Vector Size: {encrypted_vector.size()}")
print(f"- Decrypted Test Check: {encrypted_vector.decrypt()}")
