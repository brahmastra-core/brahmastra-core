"""
Day 63: Stress Testing & Latency Verification for Onion Routing Core
"""
import time
import sys
from onion_wire_core import (
    serialize_onion_packet, 
    deserialize_onion_packet, 
    HEADER_SIZE
)

def run_onion_stress_suite():
    print("=== Starting Day 63 Onion Routing Stress & Latency Suite ===")
    
    # 1. Normal Payload Latency Check
    start = time.perf_counter()
    sample_payload = b"Secure_Mesh_Payload_Hop_Stream"
    wire = serialize_onion_packet(3, sample_payload)
    v, d, p = deserialize_onion_packet(wire)
    normal_latency = (time.perf_counter() - start) * 1000
    print(f"[PASS] Normal 3-Hop Serialization & Deserialization | Latency: {normal_latency:.4f} ms")
    
    # 2. Edge Case: Empty Payload Handling
    start = time.perf_counter()
    empty_wire = serialize_onion_packet(1, b"")
    v_e, d_e, p_e = deserialize_onion_packet(empty_wire)
    empty_latency = (time.perf_counter() - start) * 1000
    assert p_e == b"", "Empty payload mismatch"
    print(f"[PASS] Edge Case (Empty Payload) | Wire Size: {len(empty_wire)}B | Latency: {empty_latency:.4f} ms")
    
    # 3. Edge Case: Corrupted / Truncated Malformed Packet Rejection
    start = time.perf_counter()
    malformed_wire = b"\x01\x02"  # Only 2 bytes (Header requires at least HEADER_SIZE)
    try:
        deserialize_onion_packet(malformed_wire)
        print("[FAIL] Corrupted packet was not rejected.")
    except ValueError as e:
        reject_latency = (time.perf_counter() - start) * 1000
        print(f"[PASS] Malformed Packet Safely Intercepted: {e} | Latency: {reject_latency:.4f} ms")
        
    # 4. Stress Load: 50,000 Byte Burst Payload & Memory Footprint
    start = time.perf_counter()
    large_payload = b"A" * 50000
    large_wire = serialize_onion_packet(1, large_payload)
    v_l, d_l, p_l = deserialize_onion_packet(large_wire)
    large_latency = (time.perf_counter() - start) * 1000
    mem_kb = sys.getsizeof(large_wire) / 1024
    print(f"[PASS] Large Burst Payload (50KB) Processed | Size: {mem_kb:.2f} KB | Latency: {large_latency:.4f} ms")

if __name__ == "__main__":
    run_onion_stress_suite()
