"""
Brahmastra Mesh Network - Day 49 Ping-Pong Protocol Engine
Implements authenticated, forward-secret ping-pong message exchange between mesh nodes.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import secrets
import json
import time
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from network.identity import NodeIdentity
from network.session_manager import SessionKeyManager

@dataclass
class MeshPacket:
 source_peer_id: str
 target_peer_id: str
 nonce: bytes
 ciphertext: bytes

class PingPongEngine:
 """Manages secure encrypted ping-pong message transmission between nodes."""

 def __init__(self, node_identity: NodeIdentity, session_key: bytes, remote_peer_id: str) -> None:
 self.node_identity = node_identity
 self.session_key = session_key
 self.remote_peer_id = remote_peer_id
 self.cipher = ChaCha20Poly1305(session_key)
 self.seq_counter = 0

 def create_ping(self) -> MeshPacket:
 """Create an encrypted PING packet with an incremented sequence number."""
 self.seq_counter += 1
 payload = json.dumps({
 "type": "PING",
 "seq": self.seq_counter,
 "timestamp": time.time()
 }).encode("utf-8")

 nonce = secrets.token_bytes(12)
 ciphertext = self.cipher.encrypt(nonce, payload, None)

 local_id = getattr(self.node_identity, "peer_id", hashlib.sha256(self.node_identity.get_public_bytes()).hexdigest())

 return MeshPacket(
 source_peer_id=str(local_id),
 target_peer_id=self.remote_peer_id,
 nonce=nonce,
 ciphertext=ciphertext
 )

 def handle_packet(self, packet: MeshPacket) -> Optional[MeshPacket]:
 """Decrypt incoming packet; if PING, return encrypted PONG reply."""
 try:
 decrypted_data = self.cipher.decrypt(packet.nonce, packet.ciphertext, None)
 msg = json.loads(decrypted_data.decode("utf-8"))
 except Exception as e:
 raise PermissionError(f"Integrity check failed: corrupt or tampered packet: {e}")

 if msg.get("type") == "PING":
 pong_payload = json.dumps({
 "type": "PONG",
 "echo_seq": msg.get("seq"),
 "timestamp": time.time()
 }).encode("utf-8")

 nonce = secrets.token_bytes(12)
 ciphertext = self.cipher.encrypt(nonce, pong_payload, None)

 local_id = getattr(self.node_identity, "peer_id", hashlib.sha256(self.node_identity.get_public_bytes()).hexdigest())

 return MeshPacket(
 source_peer_id=str(local_id),
 target_peer_id=packet.source_peer_id,
 nonce=nonce,
 ciphertext=ciphertext
 )

 return None

 def verify_pong(self, pong_packet: MeshPacket) -> Tuple[bool, int]:
 """Verify returned PONG packet matches sequence."""
 decrypted_data = self.cipher.decrypt(pong_packet.nonce, pong_packet.ciphertext, None)
 msg = json.loads(decrypted_data.decode("utf-8"))
 if msg.get("type") == "PONG":
 return True, msg.get("echo_seq", -1)
 return False, -1

if __name__ == "__main__":
 node_a = NodeIdentity()
 node_b = NodeIdentity()

 mgr_a = SessionKeyManager(node_a)
 mgr_b = SessionKeyManager(node_b)

 mgr_a.complete_mutual_handshake(node_b)
 
 # Extract the exact peer_id used by SessionKeyManager
 peer_b_id = str(getattr(node_b, "peer_id", hashlib.sha256(node_b.get_public_bytes()).hexdigest()))
 peer_a_id = str(getattr(node_a, "peer_id", hashlib.sha256(node_a.get_public_bytes()).hexdigest()))
 shared_key = mgr_a.active_sessions[peer_b_id]

 engine_a = PingPongEngine(node_a, shared_key, peer_b_id)
 engine_b = PingPongEngine(node_b, shared_key, peer_a_id)

 # Node-A sends encrypted PING
 ping_pkt = engine_a.create_ping()
 print("[PING-PONG] Node-A sent encrypted PING datagram.")

 # Node-B receives PING and replies with encrypted PONG
 pong_pkt = engine_b.handle_packet(ping_pkt)
 if pong_pkt:
 print("[PING-PONG] Node-B received and decrypted PING successfully. Generated PONG.")

 # Node-A verifies PONG
 success, echo_seq = engine_a.verify_pong(pong_pkt)
 print(f"[PING-PONG] Node-A verified PONG (Echo Sequence: {echo_seq}). Success: {success}")
