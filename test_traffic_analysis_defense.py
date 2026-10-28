# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import time
import secrets
from crypto_dummy_padding import create_padded_packet, extract_authentic_data, PACKET_SIZE

def run_day17_traffic_analysis_suite():
    print("=" * 72)
    print(" DAY 17: TRAFFIC ANALYSIS RESISTANCE & PERFORMANCE BENCHMARK")
    print("=" * 72)

    total_runs = 50
    observed_sizes = []
    padding_times = []
    unpadding_times = []

    print(f"[*] Task 1: Generating and testing {total_runs} payloads across random sizes (1 to 3800 bytes)...")

    for i in range(1, total_runs + 1):
        # Vary payload sizes randomly between 1 byte and 3800 bytes
        payload_size = secrets.randbelow(3800) + 1
        raw_payload = secrets.token_bytes(payload_size)

        # Measure padding latency (Task 4)
        t_start = time.perf_counter()
        padded_packet = create_padded_packet(raw_payload)
        t_pad = (time.perf_counter() - t_start) * 1000.0
        padding_times.append(t_pad)

        # Record packet size for network capture emulation (Task 2 & 3)
        observed_sizes.append(len(padded_packet))

        # Measure unpadding latency and verify integrity
        t_unpad_start = time.perf_counter()
        extracted = extract_authentic_data(padded_packet)
        t_unpad = (time.perf_counter() - t_unpad_start) * 1000.0
        unpadding_times.append(t_unpad)

        assert extracted == raw_payload, f"Data corruption in run #{i}"

    # Task 2 Verification: Exactly 4096 bytes check
    min_size = min(observed_sizes)
    max_size = max(observed_sizes)
    all_identical = all(sz == PACKET_SIZE for sz in observed_sizes)
    assert all_identical, "Packet size invariant failed!"

    # Task 3 Verification: Wireshark/Network capture zero-variance check
    variance = max_size - min_size

    # Task 4 Verification: Processing overhead metrics in milliseconds
    avg_pad_time = sum(padding_times) / total_runs
    max_pad_time = max(padding_times)
    avg_unpad_time = sum(unpadding_times) / total_runs

    print("\n" + "-" * 72)
    print(" [WIRESHARK / NETWORK CAPTURE SIMULATION RESULTS]")
    print(f"  - Total Captured Packets   : {total_runs}")
    print(f"  - Minimum Observed Size   : {min_size} bytes")
    print(f"  - Maximum Observed Size   : {max_size} bytes")
    print(f"  - Network Size Variance   : {variance} bytes (ZERO VARIANCE)")
    print(f"  - Wire Invariant Status   : CONSTANT 4096 BYTES (VERIFIED)")
    print("-" * 72)
    print(" [LATENCY & OVERHEAD BENCHMARK (Task 4)]")
    print(f"  - Avg Padding Overhead    : {avg_pad_time:.4f} ms")
    print(f"  - Max Padding Latency     : {max_pad_time:.4f} ms")
    print(f"  - Avg Extraction Latency  : {avg_unpad_time:.4f} ms")
    print("-" * 72)

    print("\033[92m[SUCCESS] Day 17: All 50 packets strictly verified at 4096 bytes. Zero traffic leakage.\033[0m")

if __name__ == "__main__":
    run_day17_traffic_analysis_suite()
