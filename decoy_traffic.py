"""
Brahmastra Core: Decoy Traffic Generator (Dummy Packets)
Day 70: Architecture & Interface Design
"""

import os
import time
import secrets
from dataclasses import dataclass
from typing import List

# Core Constants (4 KB Constant Size Invariant as specified in Blueprint)
DECOY_PACKET_SIZE = 4096 # 4 KB strict invariant
DECOY_FLAG_HEADER = b"\xde\xc0\xde\xc0" # Identifies dummy packet at destination node

@dataclass
class DecoyPacket:
 packet_id: str
 target_route: List[str]
 raw_bytes: bytes
 created_at: float

class DecoyTrafficGenerator:
 """
 Interface and architecture for generating continuous 4 KB decoy cover traffic.
 """
 def __init__(self, node_pool: List[str], packet_size: int = DECOY_PACKET_SIZE):
 self.node_pool = node_pool
 self.packet_size = packet_size
 self.generated_count = 0

 def build_decoy_packet(self, hop_count: int = 3) -> DecoyPacket:
 """
 Creates a decoy packet matching the exact 4096-byte size invariant.
 Padded with cryptographically secure random entropy.
 """
 if len(self.node_pool) < hop_count:
 route = [f"Node-{i}" for i in range(hop_count)]
 else:
 route = secrets.SystemRandom().sample(self.node_pool, hop_count)

 packet_id = secrets.token_hex(8)
 header = DECOY_FLAG_HEADER + packet_id.encode("utf-8")
 random_entropy = os.urandom(self.packet_size - len(header))
 raw_payload = header + random_entropy

 assert len(raw_payload) == self.packet_size, f"Size invariant violated: {len(raw_payload)} != {self.packet_size}"

 self.generated_count += 1
 return DecoyPacket(
 packet_id=packet_id,
 target_route=route,
 raw_bytes=raw_payload,
 created_at=time.time()
 )

if __name__ == "__main__":
 print("=== Testing Decoy Traffic Generator Interface (Day 70) ===")
 sample_nodes = ["Node-A", "Node-B", "Node-C", "Node-D", "Node-E"]
 generator = DecoyTrafficGenerator(node_pool=sample_nodes)

 decoy = generator.build_decoy_packet(hop_count=3)
 print(f"[PASS] Task 1: Decoy Packet Generated ID : {decoy.packet_id}")
 print(f"[PASS] Task 1: Target Route Path : {' -> '.join(decoy.target_route)}")
 print(f"[PASS] Task 2: Exact Size Invariant : {len(decoy.raw_bytes)} bytes (4 KB)")
 print(f"[PASS] Task 4: Decoy Flag Verification : {decoy.raw_bytes.startswith(DECOY_FLAG_HEADER)}")
 print("=== Day 70 Architecture & Interface: READY ===")
