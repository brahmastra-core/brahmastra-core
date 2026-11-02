"""
Brahmastra Core: Day 81 Stress Testing & Edge Cases
Module: Traffic Size Leakage Defense (4096-byte Invariant)
"""

import unittest
import time
import resource
import os
from traffic_size_tester import FixedSizePadder, WireSnifferSimulator, TARGET_PACKET_SIZE
from traffic_size_core import StatisticalTrafficAuditor

class TestDay81SizeLeakStress(unittest.TestCase):

    def setUp(self):
        self.padder = FixedSizePadder()
        self.sniffer = WireSnifferSimulator()

    def test_01_mass_padding_burst_stress(self):
        """Stress tests 1,000 rapid padding and unpadding cycles across pseudo-random sizes."""
        start_time = time.perf_counter()
        
        for i in range(1000):
            # Dynamic pseudo-random sizes from 0 to 3000 bytes
            payload_len = (i * 37) % 3000
            payload = os.urandom(payload_len)
            
            framed = self.padder.pad_frame(payload)
            self.sniffer.sniff(framed)
            
            recovered = self.padder.unpad_frame(framed)
            self.assertEqual(recovered, payload, f"Integrity failure at index {i}")

        elapsed_ms = ((time.perf_counter() - start_time) / 1000) * 1000
        print(f"\n[METRIC] Mean Frame Padding & Audit Latency: {elapsed_ms:.4f} ms")
        self.assertLess(elapsed_ms, 1.0, "Latency exceeded 1.0 ms threshold!")

        # Verify zero standard deviation across all 1,000 packets
        observed_sizes = [p.observed_size for p in self.sniffer.captured_packets]
        auditor = StatisticalTrafficAuditor(observed_sizes)
        self.assertEqual(auditor.compute_standard_deviation(), 0.0, "Statistical leakage detected!")
        self.assertEqual(auditor.compute_size_entropy(), 0.0, "Entropy of packet lengths is non-zero!")

    def test_02_boundary_and_oversize_edge_cases(self):
        """Validates exact payload upper boundaries (4092 bytes) and rejects oversized payloads."""
        # 1. Exact boundary payload: 4092 bytes + 4 bytes header = 4096 bytes
        max_valid_payload = b"B" * 4092
        framed_max = self.padder.pad_frame(max_valid_payload)
        self.assertEqual(len(framed_max), TARGET_PACKET_SIZE)
        self.assertEqual(self.padder.unpad_frame(framed_max), max_valid_payload)

        # 2. Oversized payload: 4093 bytes (Must raise ValueError)
        oversized_payload = b"B" * 4093
        with self.assertRaises(ValueError):
            self.padder.pad_frame(oversized_payload)

    def test_03_truncated_wire_frame_rejection(self):
        """Validates that incomplete packets arriving on the wire are rejected immediately."""
        # Frame of 4095 bytes (1 byte short)
        short_packet = b"X" * 4095
        with self.assertRaises(ValueError):
            self.padder.unpad_frame(short_packet)

        # Frame of 4097 bytes (1 byte extra)
        long_packet = b"X" * 4097
        with self.assertRaises(ValueError):
            self.padder.unpad_frame(long_packet)

    def test_04_resource_limits_under_80mb(self):
        """Strict verification that memory footprint remains well below 80MB RAM."""
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[METRIC] Current Traffic Size Pipeline Memory: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
    unittest.main()
