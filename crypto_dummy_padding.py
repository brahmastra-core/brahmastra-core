# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import struct
import secrets

PACKET_SIZE = 4096
HEADER_MAGIC = b"BDUM"  # Brahmastra Dummy Padded Frame

def generate_secure_dummy_bytes(length: int) -> bytes:
    """Task 1: Generate cryptographically secure pseudorandom dummy bytes."""
    return secrets.token_bytes(length)

def create_padded_packet(authentic_data: bytes) -> bytes:
    """
    Task 2 & 3: Encapsulate payload with cryptographic dummy bytes into exactly 4096 bytes.
    Frame: [Magic Header (4B)] + [Payload Length (4B)] + [Authentic Data (N bytes)] + [Dummy Bytes (Pad)]
    """
    data_length = len(authentic_data)
    max_payload = PACKET_SIZE - len(HEADER_MAGIC) - 4
    if data_length > max_payload:
        raise ValueError(f"Payload size ({data_length}) exceeds maximum limit ({max_payload})")

    dummy_needed = PACKET_SIZE - len(HEADER_MAGIC) - 4 - data_length
    dummy_padding = generate_secure_dummy_bytes(dummy_needed)
    
    packet = HEADER_MAGIC + struct.pack(">I", data_length) + authentic_data + dummy_padding
    assert len(packet) == PACKET_SIZE, f"Length invariant violated: {len(packet)} != 4096"
    return packet

def extract_authentic_data(packet: bytes) -> bytes:
    """
    Task 4: Strip cryptographically secure dummy bytes and safely extract authentic payload.
    """
    if len(packet) != PACKET_SIZE:
        raise ValueError(f"Integrity check failed: Expected {PACKET_SIZE} bytes, received {len(packet)}")
    
    magic = packet[:4]
    if magic != HEADER_MAGIC:
        raise ValueError("Invalid frame header signature")
    
    data_length = struct.unpack(">I", packet[4:8])[0]
    payload = packet[8:8 + data_length]
    return payload

def run_day16_test_suite():
    print("=" * 68)
    print(" DAY 16: CRYPTOGRAPHIC DUMMY PADDING ALGORITHM VERIFICATION")
    print("=" * 68)

    # Task 3 Test Scenarios: 1 Byte vs 3000 Bytes payloads
    test_payload_1byte = b"X"
    test_payload_3000bytes = secrets.token_bytes(3000)
    intermediate_payload = b"Brahmastra Lattice Cryptographic Node Heartbeat"

    scenarios = [
        ("Single Byte Edge Case", test_payload_1byte),
        ("Realistic Node Payload", intermediate_payload),
        ("Heavy Load (3000 Bytes)", test_payload_3000bytes)
    ]

    for label, payload in scenarios:
        packet = create_padded_packet(payload)
        extracted = extract_authentic_data(packet)
        
        # Invariant Assertions
        assert len(packet) == 4096, f"Failed constant size invariant for {label}"
        assert extracted == payload, f"Failed integrity unpadding for {label}"
        
        print(f"[{label}]")
        print(f"  - Authentic Payload Size : {len(payload):<5} bytes")
        print(f"  - Padded Frame Size     : {len(packet)} bytes (Exact 4 KB)")
        print(f"  - Unpadding Verification: PASSED\n")

    print("\033[92m[SUCCESS] Day 16 Tasks (Cryptographic Dummy Padding) Passed All Tests!\033[0m")

if __name__ == "__main__":
    run_day16_test_suite()
