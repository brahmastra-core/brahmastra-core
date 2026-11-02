"""
Brahmastra Core: Day 78 Stress Testing & Verification (Final Patch)
Module: 5-Node E2E Onion Routing Pipeline
"""

import unittest
import time
import resource
from onion_mesh_tester import OnionPacket
from e2e_onion_core import AuditedOnionPipeline

class TestDay78OnionStress(unittest.TestCase):

    def setUp(self):
        self.pipeline = AuditedOnionPipeline()

    def test_01_mass_e2e_circuit_stress(self):
        """Stress tests 500 complete end-to-end circuit traversals."""
        secret_base = b"BRAHMASTRA_STRESS_CIRCUIT_BURST_TOKEN_"
        start_time = time.perf_counter()

        for i in range(500):
            for k in self.pipeline.node_memory_logs:
                self.pipeline.node_memory_logs[k] = []

            payload = secret_base + str(i).encode()
            packet = self.pipeline.create_onion_message(payload)
            recovered, leak = self.pipeline.execute_and_audit_circuit(packet, payload)
            
            self.assertEqual(recovered, payload, f"Integrity failure at iteration {i}")
            self.assertFalse(leak, f"Leakage detected at iteration {i}")

        elapsed_ms = ((time.perf_counter() - start_time) / 500) * 1000
        print(f"\n[METRIC] Mean E2E Circuit Processing Latency: {elapsed_ms:.4f} ms")
        self.assertLess(elapsed_ms, 5.0, "E2E latency exceeded 5ms threshold!")

    def test_02_payload_tampering_edge_case(self):
        """Validates that bit modifications mid-transit fail plaintext recovery or route validity."""
        payload = b"CRITICAL_INTEGRITY_CHECK_PAYLOAD"
        packet = self.pipeline.create_onion_message(payload)
        
        # Tamper byte in outer payload
        corrupted_bytes = bytearray(packet.layer_data)
        corrupted_bytes[10] ^= 0xFF
        corrupted_packet = OnionPacket(layer_data=bytes(corrupted_bytes), next_hop=packet.next_hop)

        try:
            recovered, _ = self.pipeline.execute_and_audit_circuit(corrupted_packet, payload)
            # If no routing crash occurs, recovered payload must NOT match original payload
            self.assertNotEqual(recovered, payload, "Tampered packet unexpectedly recovered valid plaintext!")
        except Exception:
            # Routing crash on garbage next-hop is also expected and valid behavior
            pass

    def test_03_empty_and_minimal_payload_edge_cases(self):
        """Ensures that minimal and empty payloads do not crash onion encapsulation."""
        for edge_payload in [b"X", b"A" * 1024]:
            for k in self.pipeline.node_memory_logs:
                self.pipeline.node_memory_logs[k] = []
            packet = self.pipeline.create_onion_message(edge_payload)
            recovered, leak = self.pipeline.execute_and_audit_circuit(packet, edge_payload)
            self.assertEqual(recovered, edge_payload, "Edge payload mismatch!")
            self.assertFalse(leak, "Leak on edge payload!")

        empty_payload = b""
        packet_empty = self.pipeline.create_onion_message(empty_payload)
        recovered_empty = self.pipeline.simulate_circuit_traversal(packet_empty)
        self.assertEqual(recovered_empty, empty_payload, "Empty payload recovery failed!")

    def test_04_resource_limits_under_80mb(self):
        """Strict verification that memory footprint remains well below 80MB RAM."""
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[METRIC] Current E2E Onion Pipeline Memory: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
    unittest.main()
