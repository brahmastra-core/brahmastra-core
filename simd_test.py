import tenseal as ts

# బ్రహ్మాస్త్రం కోర్ కాంటెక్స్ట్ (SIMD సపోర్ట్‌తో)
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=4096,
    plain_modulus=1032193
)

# సంఖ్యల శ్రేణి (డేటా లిస్ట్‌లు)
data_batch_1 = [10, 20, 30, 40, 50]
data_batch_2 = [5,  15, 25, 35, 45]

print("అసలు డేటా బ్యాచ్ 1:", data_batch_1)
print("అసలు డేటా బ్యాచ్ 2:", data_batch_2)

# SIMD పద్ధతిలో డేటాను ఒకే సైఫర్‌టెక్స్ట్‌గా లాక్ చేయడం
enc_batch_1 = ts.bfv_vector(context, data_batch_1)
enc_batch_2 = ts.bfv_vector(context, data_batch_2)

print("\nడేటా బ్యాచ్‌లు బ్రహ్మాస్త్రం గణిత కవచంలోకి వెళ్లాయి.")

# హోమోమార్ఫిక్ SIMD కూడిక: అన్ని సంఖ్యలు ఒకేసారి కలుస్తాయి
enc_result = enc_batch_1 + enc_batch_2

print("తాళం తీయకుండానే అన్ని విలువలపై ఒకేసారి గణిత ప్రక్రియ పూర్తయింది.")

# సీక్రెట్ కీతో ధ్రువీకరణ
decrypted_batch = enc_result.decrypt()
print("\nబ్రహ్మాస్త్రం సీక్రెట్ ఫలితం (All Sums):", decrypted_batch)