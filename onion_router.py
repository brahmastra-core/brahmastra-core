"""
Day 61: 3-Hop Onion Routing Architecture Data Structures & Interfaces
Mathematical Model: Reverse layer encapsulation and single-hop unwrapping.
"""
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any

@dataclass
class OnionHop:
 """Represents a single hop node in the 3-hop routing circuit."""
 node_id: str
 public_key: str
 next_node_id: Optional[str] = None

@dataclass
class OnionPacket:
 """Layered Onion Packet Data Structure."""
 ephemeral_key: str
 payload: bytes
 layer_depth: int = 3

def build_onion_packet(
 payload: bytes, 
 hops: list[OnionHop]
) -> OnionPacket:
 """
 Constructs a 3-layer onion packet using reverse encapsulation:
 Layer 3 (Exit) -> Layer 2 (Relay) -> Layer 1 (Entry).
 """
 current_payload = payload
 for hop in reversed(hops):
 # Simulated multi-layer encryption encapsulation
 layer_header = f"ADDR:{hop.next_node_id}|KEY:{hop.public_key}|".encode()
 current_payload = layer_header + current_payload

 return OnionPacket(
 ephemeral_key="ephemeral_curve25519_stub",
 payload=current_payload,
 layer_depth=len(hops)
 )

def peel_onion_layer(
 packet: OnionPacket, 
 private_key: str
) -> Tuple[Optional[str], OnionPacket]:
 """
 Peels exactly one outer layer using the current node's private key.
 Returns:
 (next_hop_address, remaining_inner_packet)
 """
 if packet.layer_depth <= 0 or not packet.payload:
 raise ValueError("Invalid packet depth or empty payload.")

 # Parsing the peeled outer layer
 data = packet.payload
 if b"|" in data:
 header_part, remaining_payload = data.split(b"|", 1)
 next_hop = header_part.replace(b"ADDR:", b"").decode(errors="ignore")
 if next_hop == "None":
 next_hop = None
 else:
 next_hop = None
 remaining_payload = data

 peeled_packet = OnionPacket(
 ephemeral_key=packet.ephemeral_key,
 payload=remaining_payload,
 layer_depth=packet.layer_depth - 1
 )
 return next_hop, peeled_packet

if __name__ == "__main__":
 # Test Interface Initialization
 h3 = OnionHop("Node-3", "pk_node3", None)
 h2 = OnionHop("Node-2", "pk_node2", "Node-3")
 h1 = OnionHop("Node-1", "pk_node1", "Node-2")

 onion = build_onion_packet(b"TOP_SECRET_PAYLOAD", [h1, h2, h3])
 print(f"[Initialized] Layer Depth: {onion.layer_depth}")
 
 # Peel Layer 1 at Entry Node
 next_hop, inner = peel_onion_layer(onion, "sk_node1")
 print(f"[Peel Hop 1] Next Hop: {next_hop} | Remaining Depth: {inner.layer_depth}")
