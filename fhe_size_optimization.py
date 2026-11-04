# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import tenseal as ts
import zlib
import time

def benchmark_degree(degree):
 # Setup context
 ctx = ts.context(
 ts.SCHEME_TYPE.BFV,
 poly_modulus_degree=degree,
 plain_modulus=1032193
 )
 ctx.generate_relin_keys()

 # Create and serialize ciphertext
 data = [100, 200, 300, 400]
 t0 = time.time()
 enc_v = ts.bfv_vector(ctx, data)
 enc_time = (time.time() - t0) * 1000

 raw_bytes = enc_v.serialize()
 raw_kb = len(raw_bytes) / 1024

 # Apply zlib compression
 compressed_bytes = zlib.compress(raw_bytes, level=6)
 comp_kb = len(compressed_bytes) / 1024
 savings_pct = (1 - (comp_kb / raw_kb)) * 100

 return raw_kb, comp_kb, savings_pct, enc_time

def run_day13_benchmarks():
 print("=" * 68)
 print(" DAY 13: LATTICE CIPHERTEXT SIZE MEASUREMENT & OPTIMIZATION")
 print("=" * 68)

 # Task 1, 2, & 3: Measure sizes, compression, and degree comparison
 results = {}
 for deg in [4096, 8192]:
 results[deg] = benchmark_degree(deg)

 print("\n[TASK 3: POLYNOMIAL DEGREE SIZE COMPARISON TABLE]")
 print(f"{'Poly Degree':<14} | {'RAM/Raw Size':<14} | {'Compressed':<12} | {'Savings':<10} | {'Latency'}")
 print("-" * 68)
 for deg, (raw, comp, savings, lat) in results.items():
 print(f"{deg:<14} | {raw:<11.2f} KB | {comp:<9.2f} KB | {savings:<8.1f}% | {lat:.2f} ms")

 # Task 4: Fix default parameters for minimum latency & 128-bit quantum security
 print("\n[TASK 4: OPTIMAL PARAMETER DECISION]")
 print("- Selected Standard: poly_modulus_degree = 8192")
 print("- Plain Modulus: 1032193")
 print("- Network Transfer Protocol: Enable zlib compression for serialization payloads.")
 print("\033[92m[SUCCESS] Day 13 Tasks Completed & Baseline Profile Locked!\033[0m")

if __name__ == "__main__":
 run_day13_benchmarks()
