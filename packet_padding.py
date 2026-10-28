# Copyright 2026 Brahmastra Core Contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# Official Audit Baseline: Clean-Room FHE Core Implementation.

import struct
import secrets

BUFFER_SIZE = 4096
MAGIC_HEADER = b"BFPD"  # Brahmastra Fixed Packet Data

def pad_packet(payload: bytes) -> bytes:
    """
    Task 1, 2 & 4: Encapsulate variable-length payload into a constant 4096-byte packet.
    """
    payload_len = len(payload)
    max_payload = BUFFER_SIZE - len(MAGIC_HEADER) - 4  # 4 bytes for length prefix
    
    if payload_len > max_payload:
        raise ValueError(f"Payload size ({payload_len} bytes) exceeds maximum capacity ({max_payload} bytes)")

    # Construct packet: [Magic (4B)] + [Payload Length (4B)] + [Payload (NB)] + [Padding]
    header = MAGIC_HEADER + struct.pack(">I", payload_len)
    padding_needed = BUFFER_SIZE - len(header) - payload_len
    padding_bytes = secrets.token_bytes(padding_needed)
    
    padded_packet = header + payload + padding_bytes
    return padded_packet

def unpad_packet(packet: bytes) -> bytes:
    """
    Strip padding and extract authentic payload verifying header constraints.
    """
    if len(packet) != BUFFER_SIZE:
        raise ValueError(f"Packet corrupted: Expected {BUFFER_SIZE} bytes, got {len(packet)} bytes")
        
    magic = packet[:4]
    if magic != MAGIC_HEADER:
        raise ValueError("Invalid packet header signature")
        
    payload_len = struct.unpack(">I", packet[4:8])[0]
    payload = packet[8:8 + payload_len]
    return payload

def run_padding_verification():
    print("=" * 68)
    print(" DAY 15: CONSTANT PACKET PADDING DESIGN (4 KB BUFFER)")
    print("=" * 68)
    
    # Test payloads of varying sizes
    test_cases = [
        b"Small heartbeat ping",
        b"Medium transaction message: Dharma consensus validation block #1042",
        secrets.token_bytes(1500)
    ]
    
    for idx, payload in enumerate(test_cases, 1):
        padded = pad_packet(payload)
        unpadded = unpad_packet(padded)
        
        # Verify constant packet size
        assert len(padded) == BUFFER_SIZE, f"Buffer invariant failed: {len(padded)} != 4096"
        assert unpadded == payload, "Unpadded payload does not match authentic data!"
        
        print(f"[TEST {idx}] Input Size: {len(payload):<4} bytes | Padded Size: {len(padded)} bytes | Verified: OK")
        
    print(f"\n[STATUS] Constant 4096-byte buffer invariant successfully enforced.")
    print("\033[92m[SUCCESS] Day 15 Tasks (Constant Packet Padding & Documentation) Completed!\033[0m")

if __name__ == "__main__":
    run_padding_verification()
