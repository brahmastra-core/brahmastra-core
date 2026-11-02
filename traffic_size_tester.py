"""
Brahmastra Core: Day 79 - Traffic Size Leakage Architecture & Interface
Verifies:
  1. Sniffing multiple message sizes across mixnet links.
  2. Strict 4096-byte wire frame invariant.
"""

import os
import struct
from typing import List, Tuple
from dataclasses import dataclass

TARGET_PACKET_SIZE = 4096  # 4 KB Constant Wire Invariant

@dataclass
class WirePacketSnapshot:
    packet_id: int
    observed_size: int
    raw_data: bytes

class FixedSizePadder:
    """
    Task 4: Interface and data structures for constant 4096-byte padding/unpadding.
    """
    def __init__(self, target_size: int = TARGET_PACKET_SIZE):
        self.target_size = target_size

    def pad_frame(self, payload: bytes) -> bytes:
        """Pads arbitrary payload to exactly 4096 bytes with random padding."""
        payload_len = len(payload)
        max_payload = self.target_size - 4  # 4 bytes for payload length header
        if payload_len > max_payload:
            raise ValueError(f"Payload size {payload_len} exceeds max allowable {max_payload} bytes")

        header = struct.pack(">I", payload_len)
        padding_needed = self.target_size - 4 - payload_len
        # Cryptographic high-entropy random bytes to prevent entropy differential
        padding = os.urandom(padding_needed)
        return header + payload + padding

    def unpad_frame(self, padded_packet: bytes) -> bytes:
        """Recovers original payload from a 4096-byte packet."""
        if len(padded_packet) != self.target_size:
            raise ValueError(f"Corrupt wire frame size: {len(padded_packet)} != {self.target_size}")
        
        payload_len = struct.unpack(">I", padded_packet[:4])[0]
        return padded_packet[4:4 + payload_len]

class WireSnifferSimulator:
    """
    Task 1: Simulates intermediate network wire sniffing.
    """
    def __init__(self):
        self.captured_packets: List[WirePacketSnapshot] = []

    def sniff(self, raw_packet: bytes) -> WirePacketSnapshot:
        snapshot = WirePacketSnapshot(
            packet_id=len(self.captured_packets) + 1,
            observed_size=len(raw_packet),
            raw_data=raw_packet
        )
        self.captured_packets.append(snapshot)
        return snapshot

def run_day79_architecture_test():
    print("=== Brahmastra Day 79: Traffic Size Leakage Architecture ===")
    
    padder = FixedSizePadder()
    sniffer = WireSnifferSimulator()

    # Task 1: Test messages of varying sizes
    test_messages = [
        b"Hi",                                        # 2 bytes
        b"Brahmastra onion message 2026",             # 30 bytes
        b"Quantum-resistant packet routing frame",    # 39 bytes
        b"Z" * 512,                                   # 512 bytes
        b"X" * 3500                                   # 3500 bytes (Large payload)
    ]

    print(f"[TEST] Injecting {len(test_messages)} varying payload sizes into mixnet...")

    for idx, msg in enumerate(test_messages, 1):
        # Apply strict 4096-byte framing
        framed_packet = padder.pad_frame(msg)
        
        # Sniff packet on intermediate wire
        snapshot = sniffer.sniff(framed_packet)
        print(f"  -> Packet {idx}: Payload = {len(msg)} bytes | Wire Observed = {snapshot.observed_size} bytes")

        # Task 2: Verify strictly 4096 bytes on wire
        assert snapshot.observed_size == TARGET_PACKET_SIZE, f"Size leakage on packet {idx}!"
        
        # Recover and verify integrity
        recovered = padder.unpad_frame(framed_packet)
        assert recovered == msg, f"Integrity error recovering packet {idx}!"

    print("\n[VERIFICATION]")
    # Ensure all captured packets on wire are identical in length
    unique_sizes = {p.observed_size for p in sniffer.captured_packets}
    print(f"  Observed unique sizes across all wire packets: {unique_sizes}")
    assert unique_sizes == {TARGET_PACKET_SIZE}, "Task 2 Failed: Variable wire packet sizes detected!"
    
    print("[PASS] Task 1: Diverse payload sizes successfully routed and sniffed")
    print("[PASS] Task 2: Strictly 4096 bytes invariant verified across all wire traffic")
    print("=== Day 79 Architecture & Interface: READY ===")

if __name__ == "__main__":
    run_day79_architecture_test()
