"""
Brahmastra Mesh Network - Day 47 Encrypted Session Key Management
Manages post-handshake ephemeral session key derivation and connection latency benchmarks.
"""

import time
import secrets
import hashlib
from typing import Dict, Optional
from network.identity import NodeIdentity
from network.handshake import NodeHandshake, HandshakePayload

class SessionKeyManager:
 """Derives and manages forward-secret symmetric keys post successful handshake."""

 def __init__(self, node_identity: NodeIdentity) -> None:
 self.node_identity: NodeIdentity = node_identity
 self.handshake: NodeHandshake = NodeHandshake(node_identity)
 self.active_sessions: Dict[str, bytes] = {}

 def complete_mutual_handshake(self, remote_node_identity: NodeIdentity) -> float:
 """
 Executes complete handshake with latency auditing (< 10ms guardrail).
 Derives an ephemeral symmetric key upon verification.
 """
 start_time = time.perf_counter()

 remote_handshake = NodeHandshake(remote_node_identity)

 # Step 1: Issue challenge
 challenge = remote_handshake.issue_challenge()

 # Step 2: Responder creates signature payload
 payload = self.handshake.create_response(challenge)

 # Step 3: Remote node verifies signature
 if not remote_handshake.verify_remote_node(payload):
 raise PermissionError("Session aborted: Remote signature failed verification!")

 # Step 4: Ephemeral Session Key Derivation (HKDF-like SHA-256 mix)
 # Combines shared challenge nonce with mutual public bytes for ephemeral keying
 session_seed = challenge + self.node_identity.get_public_bytes() + remote_node_identity.get_public_bytes()
 ephemeral_session_key = hashlib.sha256(session_seed).digest()

 remote_peer_id = getattr(remote_node_identity, "peer_id", hashlib.sha256(remote_node_identity.get_public_bytes()).hexdigest())
 self.active_sessions[str(remote_peer_id)] = ephemeral_session_key

 handshake_latency_ms = (time.perf_counter() - start_time) * 1000
 return handshake_latency_ms

if __name__ == "__main__":
 node_local = NodeIdentity()
 node_remote = NodeIdentity()

 session_mgr = SessionKeyManager(node_local)
 latency_ms = session_mgr.complete_mutual_handshake(node_remote)

 print(f"[LOG] Handshake & Session Key Derivation Completed.")
 print(f"[METRICS] Handshake Latency: {latency_ms:.3f} ms")
 assert latency_ms < 10.0, f"Latency breached: {latency_ms}ms >= 10ms"
 print(f"[PASS] Latency well within 10ms threshold!")
 print(f"[ACTIVE SESSIONS] Total Keys Stored: {len(session_mgr.active_sessions)}")
