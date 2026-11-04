import tenseal as ts

<<<<<<< HEAD
# 1. Cryptographic Shield (Lattice Encryption Context Setup)
=======
# 1. (Lattice Encryption Context) 
>>>>>>> 86db1ed (Standardize all codebase comments, docs, and prints to professional English)
context = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=4096,
 plain_modulus=1032193
)

<<<<<<< HEAD
# 2. Secret Raw Data Values
num1 = [15]
num2 = [25]

# 3. Encrypting Data into Lattice Ciphertext
enc1 = ts.bfv_vector(context, num1)
enc2 = ts.bfv_vector(context, num2)

print("Data successfully encrypted into lattice ciphertext.")

# 4. Homomorphic Computation: Blind Addition Without Decryption
enc_sum = enc1 + enc2

print("Blind computation (Addition) completed without decryption.")

# 5. Result Verification with Private Key
result = enc_sum.decrypt()
print("Secret Result (Decrypted Sum):", result[0])
=======
# 2. 
num1 = [15]
num2 = [25]

# 3. ‌ (Ciphertext)
enc1 = ts.bfv_vector(context, num1)
enc2 = ts.bfv_vector(context, num2)

print(" ‌ .")

# 4. : 
enc_sum = enc1 + enc2

print(" (Addition) .")

# 5. verified
result = enc_sum.decrypt()
print("Secret Result ( ):", result[0])
>>>>>>> 86db1ed (Standardize all codebase comments, docs, and prints to professional English)
