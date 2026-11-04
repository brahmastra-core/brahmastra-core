import hashlib
import time
import random

print("=== Brahmastra: Decentralized P2P Node Network Engine ===\n")

class BrahmastraNode:
 def __init__(self, node_id, location):
 self.node_id = node_id
 self.location = location
 self.peers = []

 def connect_peer(self, peer_node):
 if peer_node not in self.peers:
 self.peers.append(peer_node)
 peer_node.peers.append(self)

 def relay_packet(self, sender_id, encrypted_payload, hops=3):
 if hops == 0:
 print(f"[{self.node_id} ({self.location})]: Packet reached destination! .")
 return

 print(f"[{self.node_id} ({self.location})]: ‌ ‌ ... ( : {hops})")
 time.sleep(0.4)

 # Forwarding to an available peer
 eligible_peers = [p for p in self.peers if p.node_id != sender_id]
 if eligible_peers:
 next_hop = random.choice(eligible_peers)
 next_hop.relay_packet(self.node_id, encrypted_payload, hops - 1)

# 1. Creating 4 virtual nodes globally
node_in = BrahmastraNode("Node_IND_01", "Hyderabad, India")
node_ch = BrahmastraNode("Node_CHE_01", ", ")
node_de = BrahmastraNode("Node_DEU_01", "Frankfurt, Germany")
node_sg = BrahmastraNode("Node_SGP_01", "Singapore")

# 2. Establishing decentralized mesh topology across nodes
node_in.connect_peer(node_sg)
node_sg.connect_peer(node_ch)
node_ch.connect_peer(node_de)
node_de.connect_peer(node_in)

print(f"[Network Status]: 4 Global nodes interconnected in mesh network.\n")

# 3. ‌ 
mock_encrypted_payload = hashlib.sha256(b"Brahmastra_Encrypted_Tx_500Credits").hexdigest()
print(f"[Initiation]: Transaction routing started from Node_IND_01...")
print(f"[‌ ]: {mock_encrypted_payload[:16]}...\n")

# Routing packet across 3 hops
node_in.relay_packet("CLIENT_USER", mock_encrypted_payload, hops=3)

print("\n" + "=" * 45)
print("P2P ‌ verified: !")
print("=" * 45)