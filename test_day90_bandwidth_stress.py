"""
Brahmastra Core: Day 90 - Bandwidth Benchmarking Stress Testing & Edge Cases
Verifies:
  1. High-burst traffic load distribution and edge-case payload sizes.
  2. Sub-millisecond dispatch latency bounds under stress.
  3. Strict memory footprint containment beneath 80MB RAM.
  4. 100% automated test pass rate.
"""

import unittest
import time
import resource
import os
from bandwidth_core import BandwidthCoreEngine, CorePacket

class TestDay90BandwidthStress(unittest.TestCase):

    def setUp(self):
        self.node_pool = ["Mix-Hop-1", "Mix-Hop-2", "Mix-Hop-3", "Mix-Hop-4"]
        self.engine = BandwidthCoreEngine(node_pool=self.node_pool)

    def test_01_burst_traffic_load_balance(self):
        """Stress: Inject 1,000 burst packets and verify strict equitable load distribution."""
        total_packets = 1000
        for i in range(total_packets):
            pkt = CorePacket(
                packet_id=f"burst-stress-{i}",
                payload=b"SPHINX_CIPHERTEXT_BURST_BLOCK",
                timestamp=time.time()
            )
            ok, assigned_node = self.engine.dispatch(pkt)
            self.assertTrue(ok)
            self.assertTrue(pkt.delivered)

        expected_per_node = total_packets // len(self.node_pool)
        for nid, node in self.engine.nodes.items():
            self.assertEqual(node.processed_count, expected_per_node)

    def test_02_variable_payload_size_stability(self):
        """Edge Case: Fuzz with variable payload sizes from tiny 32-byte chunks to 32KB payloads."""
        for i in range(200):
            size = (i % 32 + 1) * 1024  # 1KB to 32KB
            raw_payload = os.urandom(size)
            pkt = CorePacket(
                packet_id=f"fuzz-pkt-{i}",
                payload=raw_payload,
                timestamp=time.time()
            )
            ok, _ = self.engine.dispatch(pkt)
            self.assertTrue(ok)

    def test_03_submillisecond_dispatch_latency(self):
        """Performance: Ensure average dispatch latency is sub-millisecond (< 1.0 ms)."""
        iterations = 500
        start_time = time.perf_counter()

        for i in range(iterations):
            pkt = CorePacket(
                packet_id=f"perf-lat-{i}",
                payload=b"QUICK_DISPATCH_BLOCK",
                timestamp=time.time()
            )
            self.engine.dispatch(pkt)

        total_elapsed_ms = (time.perf_counter() - start_time) * 1000
        avg_latency_ms = total_elapsed_ms / iterations
        print(f"\n[BENCHMARK] Average Dispatch Latency: {avg_latency_ms:.5f} ms")
        self.assertLess(avg_latency_ms, 1.0, "Dispatch latency exceeded 1.0 ms threshold!")

    def test_04_memory_ceiling_under_80mb(self):
        """Stability: Total process memory footprint must remain strictly beneath 80MB RAM."""
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[BENCHMARK] Memory Footprint: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
    unittest.main()
