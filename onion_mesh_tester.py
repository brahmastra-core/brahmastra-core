"""
Brahmastra Core: End-to-End Onion Routing Architecture & Interface
Day 76: 3-Hop Layering & Peeling Blueprint
"""

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

def xor_crypt(key: bytes, data: bytes) -> bytes:
 """Deterministic stream cipher simulation for onion layer demonstration."""
 keystream = bytearray()
 counter = 0
 while len(keystream) < len(data):
 keystream.extend(hashlib.sha256(key + counter.to_bytes(4, 'big')).digest())
 counter += 1
 return bytes(a ^ b for a, b in zip(data, keystream[:len(data)]))

@dataclass
class OnionPacket:
 layer_data: bytes
 next_hop: str

class MeshRelayNode:
 """
 Task 4: Data structures and interface for Mesh Relay Nodes.
 Peels one layer of the onion and identifies the downstream relay.
 """
 def __init__(self, node_id: str):
 self.node_id = node_id
 self.private_key = hashlib.sha256(f"priv_{node_id}".encode()).digest()
 self.public_key = hashlib.sha256(self.private_key).digest()

 def peel_layer(self, encrypted_payload: bytes) -> Tuple[str, bytes]:
 """
 Decrypts outermost layer using node's private key.
 Format: [NextHop: 16 bytes UTF-8 padded] + [Remaining Onion Payload]
 """
 decrypted = xor_crypt(self.private_key, encrypted_payload)
 next_hop = decrypted[:16].decode('utf-8', errors='ignore').strip()
 remaining_payload = decrypted[16:]
 return next_hop, remaining_payload

class EndToEndOnionPipeline:
 """
 Task 1 & Task 2: Architecture for building and relaying nested onion messages.
 """
 def __init__(self):
 self.nodes: Dict[str, MeshRelayNode] = {
 "Node-A": MeshRelayNode("Node-A"), # Sender
 "Node-B": MeshRelayNode("Node-B"), # Ingress
 "Node-D": MeshRelayNode("Node-D"), # Mix
 "Node-E": MeshRelayNode("Node-E") # Egress
 }

 def create_onion_message(self, plaintext: bytes) -> OnionPacket:
 """
 Task 1: Locks payload into 3 layers in reverse order:
 Layer 3 (Node-E) -> Layer 2 (Node-D) -> Layer 1 (Node-B).
 """
 # Inner Layer for Node-E (Terminal hop: "EXIT")
 header_e = "EXIT".ljust(16).encode('utf-8')
 layer_e = xor_crypt(self.nodes["Node-E"].private_key, header_e + plaintext)

 # Middle Layer for Node-D (Directs to Node-E)
 header_d = "Node-E".ljust(16).encode('utf-8')
 layer_d = xor_crypt(self.nodes["Node-D"].private_key, header_d + layer_e)

 # Outer Layer for Node-B (Directs to Node-D)
 header_b = "Node-D".ljust(16).encode('utf-8')
 layer_b = xor_crypt(self.nodes["Node-B"].private_key, header_b + layer_d)

 return OnionPacket(layer_data=layer_b, next_hop="Node-B")

 def simulate_circuit_traversal(self, packet: OnionPacket) -> bytes:
 """
 Task 2: Traces traversal: Node-A -> Node-B -> Node-D -> Node-E.
 """
 print(f"[PATH] Initiating from Node-A -> Forwarding to {packet.next_hop}")
 
 # Hop 1: Node-B (Ingress)
 hop1_node = self.nodes[packet.next_hop]
 next_hop1, payload1 = hop1_node.peel_layer(packet.layer_data)
 print(f"[HOP 1 - {hop1_node.node_id}] Layer 1 Peeled. Next Directive -> {next_hop1}")

 # Hop 2: Node-D (Mix)
 hop2_node = self.nodes[next_hop1]
 next_hop2, payload2 = hop2_node.peel_layer(payload1)
 print(f"[HOP 2 - {hop2_node.node_id}] Layer 2 Peeled & Mixed. Next Directive -> {next_hop2}")

 # Hop 3: Node-E (Egress)
 hop3_node = self.nodes[next_hop2]
 terminal_status, recovered_plaintext = hop3_node.peel_layer(payload2)
 print(f"[HOP 3 - {hop3_node.node_id}] Layer 3 Peeled. Status -> {terminal_status}")

 return recovered_plaintext

if __name__ == "__main__":
 print("=== Testing 5-Node Mesh E2E Onion Routing (Day 76) ===")
 pipeline = EndToEndOnionPipeline()
 
 secret_message = b"BRAHMASTRA_ZERO_KNOWLEDGE_PAYLOAD_v1.0"
 print(f"[INPUT] Original Secret at Node-A: {secret_message.decode()}")

 # Task 1: Generate Onion
 onion = pipeline.create_onion_message(secret_message)
 print(f"[PASS] Task 1: 3-Layer Nested Onion Packet Constructed")

 # Task 2: Traverse Circuit
 result = pipeline.simulate_circuit_traversal(onion)
 print(f"[OUTPUT] Recovered Payload at Node-E: {result.decode()}")

 assert result == secret_message, "End-to-End Plaintext Mismatch!"
 print(f"[PASS] Task 2: Verified 3-Hop Peeling Sequence (A -> B -> D -> E)")
 print("=== Day 76 Architecture & Interface: READY ===")
