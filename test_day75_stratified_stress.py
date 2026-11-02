"""
Brahmastra Core: Day 75 Stress Testing & Resource Verification
Module: Stratified Topology Engine & Config Loader
"""

import unittest
import time
import os
import resource
from stratified_topology import LayerType, StratumNode, StratifiedTopologyEngine
from stratified_topology_core import ConfigurableStratifiedEngine

class TestDay75StratifiedStress(unittest.TestCase):

    def setUp(self):
        self.engine = ConfigurableStratifiedEngine()
        self.engine.load_from_config("config/topology_strata.json")

    def test_01_mass_path_invariance_stress(self):
        """Stress tests generation of 1000 paths to guarantee strict L1 -> L2 -> L3 invariant."""
        for _ in range(1000):
            path = self.engine.build_stratified_path()
            self.assertEqual(len(path), 3, "Circuit path length must be strictly 3 hops!")
            self.assertEqual(path[0].layer, LayerType.INGRESS, "Hop 0 is not Ingress!")
            self.assertEqual(path[1].layer, LayerType.MIX, "Hop 1 is not Mix!")
            self.assertEqual(path[2].layer, LayerType.EGRESS, "Hop 2 is not Egress!")

    def test_02_empty_stratum_edge_case(self):
        """Validates that incomplete topologies with missing layers are securely rejected."""
        broken_engine = StratifiedTopologyEngine()
        broken_engine.register_node(StratumNode("Only-Ingress", LayerType.INGRESS, "10.0.1.1:9001"))
        
        with self.assertRaises(ValueError):
            broken_engine.build_stratified_path()

    def test_03_path_generation_latency(self):
        """Measures path generation latency under rapid sequential requests."""
        total_runs = 500
        start_time = time.perf_counter()
        for _ in range(total_runs):
            self.engine.build_stratified_path()
        duration = time.perf_counter() - start_time

        avg_latency_ms = (duration / total_runs) * 1000
        print(f"\n[METRIC] Stratified Path Generation Latency: {avg_latency_ms:.4f} ms")
        self.assertLess(avg_latency_ms, 1.0, "Path building latency exceeded 1ms threshold!")

    def test_04_memory_ceiling_under_80mb(self):
        """Strict verification that memory footprint remains well below 80MB RAM."""
        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mem_mb = usage_kb / 1024.0
        print(f"[METRIC] Current Process Memory: {mem_mb:.2f} MB")
        self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
    unittest.main()
