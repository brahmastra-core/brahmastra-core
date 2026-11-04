import unittest
from onion_wire_core import (
 serialize_onion_packet, 
 deserialize_onion_packet, 
 HEADER_SIZE, 
 PROTOCOL_VERSION
)

class TestOnionWireStress(unittest.TestCase):
 def test_01_standard_packet(self):
 payload = b"Hop-Layer-Verification"
 wire = serialize_onion_packet(3, payload)
 ver, depth, recovered = deserialize_onion_packet(wire)
 self.assertEqual(ver, PROTOCOL_VERSION)
 self.assertEqual(depth, 3)
 self.assertEqual(recovered, payload)

 def test_02_empty_payload(self):
 wire = serialize_onion_packet(1, b"")
 ver, depth, recovered = deserialize_onion_packet(wire)
 self.assertEqual(depth, 1)
 self.assertEqual(recovered, b"")

 def test_03_malformed_truncated_packet(self):
 truncated_wire = b"\x01\x02" # Smaller than HEADER_SIZE
 with self.assertRaises(ValueError):
 deserialize_onion_packet(truncated_wire)

 def test_04_large_payload_integrity(self):
 burst_data = b"X" * 60000
 wire = serialize_onion_packet(2, burst_data)
 _, depth, recovered = deserialize_onion_packet(wire)
 self.assertEqual(depth, 2)
 self.assertEqual(recovered, burst_data)

if __name__ == "__main__":
 unittest.main()
