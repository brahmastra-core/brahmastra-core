import unittest
from sphinx_core import (
 TOTAL_SPHINX_SIZE,
 ALPHA_SIZE,
 BETA_SIZE,
 GAMMA_SIZE,
 DELTA_SIZE,
 SphinxReplayCache,
 build_sphinx_wire_packet,
 process_sphinx_packet_with_replay_guard
)

class TestSphinxStressSuite(unittest.TestCase):
 def setUp(self):
 self.cache = SphinxReplayCache()
 self.valid_packet = build_sphinx_wire_packet(
 b"\x01" * ALPHA_SIZE,
 b"\x02" * BETA_SIZE,
 b"\x03" * GAMMA_SIZE,
 b"\x04" * DELTA_SIZE
 )

 def test_01_valid_packet_transformation(self):
 next_hop, transformed = process_sphinx_packet_with_replay_guard(self.valid_packet, self.cache)
 self.assertEqual(len(transformed), TOTAL_SPHINX_SIZE)
 self.assertEqual(next_hop, "Node-Relay-Next")

 def test_02_replay_attack_prevention(self):
 # First processing succeeds
 process_sphinx_packet_with_replay_guard(self.valid_packet, self.cache)
 # Second processing with identical packet must raise ValueError
 with self.assertRaises(ValueError):
 process_sphinx_packet_with_replay_guard(self.valid_packet, self.cache)

 def test_03_boundary_sizes_rejected(self):
 with self.assertRaises(ValueError):
 process_sphinx_packet_with_replay_guard(b"\x00" * 1023, self.cache)
 with self.assertRaises(ValueError):
 process_sphinx_packet_with_replay_guard(b"\x00" * 1025, self.cache)

 def test_04_batch_unique_packets(self):
 for i in range(50):
 unique_alpha = i.to_bytes(4, "big").ljust(ALPHA_SIZE, b"\x00")
 pkt = build_sphinx_wire_packet(
 unique_alpha,
 b"\x02" * BETA_SIZE,
 b"\x03" * GAMMA_SIZE,
 b"\x04" * DELTA_SIZE
 )
 _, out = process_sphinx_packet_with_replay_guard(pkt, self.cache)
 self.assertEqual(len(out), TOTAL_SPHINX_SIZE)

if __name__ == "__main__":
 unittest.main()
