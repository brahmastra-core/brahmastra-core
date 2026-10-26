import tenseal as ts

# 1. గణిత కవచం (Lattice Encryption Context) ఏర్పాటు
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=4096,
    plain_modulus=1032193
)

# 2. రెండు రహస్య సంఖ్యలు
num1 = [15]
num2 = [25]

# 3. లాటిస్ ఎన్‌క్రిప్షన్ ద్వారా లాక్ చేయడం (Ciphertext)
enc1 = ts.bfv_vector(context, num1)
enc2 = ts.bfv_vector(context, num2)

print("డేటా పూర్తిగా లాటిస్ ఎన్‌క్రిప్ట్ అయ్యింది.")

# 4. హోమోమార్ఫిక్ కంప్యూటేషన్: డేటాను తెరవకుండానే కూడిక చేయడం
enc_sum = enc1 + enc2

print("తాళం తీయకుండానే చీకట్లోనే లెక్క (Addition) పూర్తయింది.")

# 5. వ్యక్తిగత కీతో ఫలితాన్ని ధ్రువీకరించడం
result = enc_sum.decrypt()
print("Secret Result (సరైన మొత్తం):", result[0])