import tenseal as ts

# Brahmastra (SIMD ‌)
context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=4096,
 plain_modulus=1032193
)

# Vector Data Lists
data_batch_1 = [10, 20, 30, 40, 50]
data_batch_2 = [5, 15, 25, 35, 45]

print("Raw Data Batch 1:", data_batch_1)
print("Raw Data Batch 2:", data_batch_2)

# Packing vector batches into single ciphertext via SIMD
enc_batch_1 = ts.bfv_vector(context, data_batch_1)
enc_batch_2 = ts.bfv_vector(context, data_batch_2)

print("\nVector batches locked inside lattice ciphertext.")

# Homomorphic SIMD Evaluation: Evaluating parallel additions simultaneously
enc_result = enc_batch_1 + enc_batch_2

print("Blind addition executed across all values without decryption.")

# Decryption verification with private key
decrypted_batch = enc_result.decrypt()
print("\nBrahmastra Decrypted Result (All Sums):", decrypted_batch)