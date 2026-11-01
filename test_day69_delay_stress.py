"""
Brahmastra Core: Day 69 Stress Testing & Resource Verification
Module: Sphinx Packet Poisson Delay Engine
"""

import unittest
import time
import os
import resource
from sphinx_delay_core import SphinxDelayCore, compute_poisson_delay, MAX_DELAY_CAP_SEC, MIN_DELAY_FLOOR_SEC

class TestDay69SphinxDelayStress(unittest.TestCase):

    def test_01_poisson_boundary_clamps(self):
        """Edge-case boundary testing on mathematical sampling."""
        delays = [compute_poisson_delay(rate_lambda=20.0) for _ in range(1000)]
        for d in delays:
            self.assertGreaterEqual(d, MIN_DELAY_FLOOR_SEC, "Delay violated minimum floor clamp!")
            self.assertLessEqual(d, MAX_DELAY_CAP_SEC, "Delay violated 200ms maximum clamp!")

    def test_02_stress_high_throughput_queue(self):
        """Stress testing with 500 packets entering the engine simultaneously."""
        engine = SphinxDelayCore(rate_lambda=20.0, max_cap=MAX_DELAY_CAP_SEC)
        total = 500
        start_enqueue = time.perf_counter()
        for i in range(total):
            pkt = os.urandom(1024)
            engine.enqueue(packet_id=i, raw_packet=pkt, next_hop=f"Node-{i%5}")
        enqueue_duration = time.perf_counter() - start_enqueue

        avg_latency_ms = (enqueue_duration / total) * 1000
        print(f"\n[METRIC] Enqueue Throughput Latency per Packet: {avg_latency_ms:.4f} ms")
        self.assertLess(avg_latency_ms, 1.0, "Latency exceeded strict 1ms boundary!")
        self.assertEqual(engine.pending_count(), total)

    def test_03_memory_ceiling_under_80mb(self):
        """Strict verification of 80MB RAM resource footprint constraint."""
        # ru_maxrss returns kilobytes on Linux
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[METRIC] Current Process Memory: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

    def test_04_draining_integrity_and_no_loss(self):
        """Ensure all buffered packets are released without data loss or corruption."""
        engine = SphinxDelayCore(rate_lambda=50.0, max_cap=0.050)
        packet_payload = b"\xde\xad\xbe\xef" * 256
        engine.enqueue(packet_id=999, raw_packet=packet_payload, next_hop="Node-Omega")
        
        # Advance time simulation to drain
        ready = engine.drain_ready(time.time() + 0.100)
        self.assertEqual(len(ready), 1)
        self.assertEqual(ready[0].packet_id, 999)
        self.assertEqual(ready[0].raw_packet, packet_payload)
        self.assertEqual(engine.pending_count(), 0)

if __name__ == "__main__":
    unittest.main()
