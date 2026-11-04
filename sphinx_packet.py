"""
Day 64: Sphinx Packet Architecture Data Structures & Interfaces
Strict 1024-byte constant size anonymous routing model.
"""
from dataclasses import dataclass
from typing import Tuple, Optional
import os

ALPHA_SIZE = 32 # Ephemeral public key size
BETA_SIZE = 160 # Routing information size
GAMMA_SIZE = 16 # HMAC authentication tag size
DELTA_SIZE = 816 # Encrypted payload size
TOTAL_SPHINX_SIZE = ALPHA_SIZE + BETA_SIZE + GAMMA_SIZE + DELTA_SIZE # 1024 Bytes

@dataclass(frozen=True)
class SphinxPacket:
 """Represents a Sphinx packet with strict byte size constraints."""
 alpha: bytes
 beta: bytes
 gamma: bytes
 delta: bytes

 def __post_init__(self):
 if len(self.alpha) != ALPHA_SIZE:
 raise ValueError(f"Alpha must be {ALPHA_SIZE} bytes.")
 if len(self.beta) != BETA_SIZE:
 raise ValueError(f"Beta must be {BETA_SIZE} bytes.")
 if len(self.gamma) != GAMMA_SIZE:
 raise ValueError(f"Gamma must be {GAMMA_SIZE} bytes.")
 if len(self.delta) != DELTA_SIZE:
 raise ValueError(f"Delta must be {DELTA_SIZE} bytes.")

 def to_bytes(self) -> bytes:
 """Serializes the Sphinx packet into 1024 continuous bytes."""
 return self.alpha + self.beta + self.gamma + self.delta

 @classmethod
 def from_bytes(cls, raw_bytes: bytes) -> "SphinxPacket":
 """Deserializes 1024 raw bytes into a SphinxPacket structure."""
 if len(raw_bytes) != TOTAL_SPHINX_SIZE:
 raise ValueError(f"Sphinx packet must be exactly {TOTAL_SPHINX_SIZE} bytes, got {len(raw_bytes)}")
 
 idx1 = ALPHA_SIZE
 idx2 = idx1 + BETA_SIZE
 idx3 = idx2 + GAMMA_SIZE
 
 return cls(
 alpha=raw_bytes[:idx1],
 beta=raw_bytes[idx1:idx2],
 gamma=raw_bytes[idx2:idx3],
 delta=raw_bytes[idx3:]
 )

def create_mock_sphinx_packet() -> SphinxPacket:
 """Constructs a valid mock Sphinx packet of exactly 1024 bytes."""
 return SphinxPacket(
 alpha=b"\xaa" * ALPHA_SIZE,
 beta=b"\xbb" * BETA_SIZE,
 gamma=b"\xcc" * GAMMA_SIZE,
 delta=b"\xdd" * DELTA_SIZE
 )

def process_sphinx_hop(packet: SphinxPacket, node_private_key: bytes) -> Tuple[str, SphinxPacket]:
 """
 Simulates peeling a layer and applying deterministic padding to 
 maintain strict 1024-byte invariant.
 """
 next_hop = "Node-Relay-2"
 
 # Simulate transformation and padding invariant
 peeled_beta = packet.beta[32:] + b"\x00" * 32
 new_alpha = b"\xee" * ALPHA_SIZE
 
 transformed_packet = SphinxPacket(
 alpha=new_alpha,
 beta=peeled_beta,
 gamma=packet.gamma,
 delta=packet.delta
 )
 return next_hop, transformed_packet

if __name__ == "__main__":
 pkt = create_mock_sphinx_packet()
 raw = pkt.to_bytes()
 print(f"[Initialized Sphinx Packet] Size: {len(raw)} Bytes")
 
 # Process Hop
 next_node, out_pkt = process_sphinx_hop(pkt, b"mock_key_32bytes_long___________")
 out_raw = out_pkt.to_bytes()
 print(f"[Hop Processed] Next Hop: {next_node} | Outgoing Packet Size: {len(out_raw)} Bytes")
 assert len(out_raw) == TOTAL_SPHINX_SIZE, "Size invariant violated!"
 print("[Verification] 1024-Byte Constant Size Invariant Strictly Preserved!")
