"""
Brahmastra Core: Day 84 Stress Testing & Edge Cases
Module: Domain Fronting & Traffic Obfuscation
"""

import unittest
import time
import resource
import os
from fronting_obfuscation_tester import DomainFrontingManager, MockDPISurveillanceEngine
from fronting_obfuscation_core import ChromeTLSProfiler, LocalObfuscationProxy, WireEnvelope

class TestDay84FrontingStress(unittest.TestCase):

    def setUp(self):
        self.manager = DomainFrontingManager()
        self.dpi = MockDPISurveillanceEngine()
        self.profiler = ChromeTLSProfiler()
        self.target_node = "brahmastra-guard-alpha.internal"
        self.proxy = LocalObfuscationProxy(target_host=self.target_node)

    def test_01_mass_domain_fronting_stress(self):
        """Stress tests 1,000 rapid domain fronting encapsulations and proxy routes."""
        start_time = time.perf_counter()

        for i in range(1000):
            # Dynamic random payloads
            payload = os.urandom((i * 13) % 2048)
            packet = self.manager.encapsulate_request(
                payload,
                front_sni="ajax.googleapis.com",
                target_host=self.target_node,
                mimicry_type="youtube"
            )
            # Route through DPI mock engine
            allowed, classification = self.dpi.inspect_stream(packet)
            self.assertTrue(allowed)
            self.assertIn("YOUTUBE", classification)

            # Route through local proxy
            envelope = WireEnvelope(
                sni=packet.outer_sni,
                headers=packet.headers,
                payload=packet.obfuscated_payload
            )
            delivered = self.proxy.handle_ingress(envelope)
            self.assertTrue(delivered)

        elapsed_ms = ((time.perf_counter() - start_time) / 1000) * 1000
        print(f"\n[METRIC] Mean Fronting & Camouflage Latency: {elapsed_ms:.4f} ms")
        self.assertLess(elapsed_ms, 1.0, "Latency exceeded 1.0 ms threshold!")
        self.assertEqual(len(self.proxy.intercepted_envelopes), 1000)

    def test_02_invalid_sni_and_mismatched_host_edges(self):
        """Edge case validation: DPI blocking suspicious SNIs and proxy rejecting host mismatches."""
        # 1. Direct mixnet keyword in SNI must be blocked by DPI
        suspicious_packet = self.manager.encapsulate_request(
            b"test_data",
            front_sni="brahmastra-node.net",
            target_host=self.target_node
        )
        allowed, reason = self.dpi.inspect_stream(suspicious_packet)
        self.assertFalse(allowed)
        self.assertIn("CENSORSHIP_ALERT", reason)

        # 2. Mismatched Host Header at proxy must be rejected safely
        mismatched_envelope = WireEnvelope(
            sni="ajax.googleapis.com",
            headers={"Host": "malicious-unknown-destination.internal"},
            payload=b"dummy"
        )
        delivered = self.proxy.handle_ingress(mismatched_envelope)
        self.assertFalse(delivered)

    def test_03_tls_profiler_consistency(self):
        """Verifies TLS camouflage invariants against signature detection."""
        profile = self.profiler.get_chrome_profile(front_sni="ajax.googleapis.com")
        self.assertEqual(profile.sni_server_name, "ajax.googleapis.com")
        self.assertIn("h2", profile.alpn)
        self.assertGreater(len(profile.ciphers), 4)

    def test_04_memory_and_resource_bounds(self):
        """Ensures memory footprint stays strictly below 80MB RAM."""
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[METRIC] Current Obfuscation Pipeline Memory: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
    unittest.main()
