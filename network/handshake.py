"""
Brahmastra Mesh Network - Node-to-Node Secure Handshake Protocol
Establishes mutual cryptographic proof and session integrity between two nodes.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
import secrets
import hashlib
from network.identity import NodeIdentity

class HandshakeState(Enum):
    INITIATED = "INITIATED"
    CHALLENGE_ISSUED = "CHALLENGE_ISSUED"
    AUTHENTICATED = "AUTHENTICATED"
    REJECTED = "REJECTED"

@dataclass
class HandshakePayload:
    initiator_peer_id: str
    initiator_public_bytes: bytes
    nonce: bytes
    signature: bytes

class NodeHandshake:
    """Manages secure mutual verification and session handshake between nodes."""

    def __init__(self, node_identity: NodeIdentity) -> None:
        self.node_identity: NodeIdentity = node_identity
        self.state: HandshakeState = HandshakeState.INITIATED

    def issue_challenge(self) -> bytes:
        """Issue a fresh, cryptographically secure 32-byte nonce."""
        self.state = HandshakeState.CHALLENGE_ISSUED
        return secrets.token_bytes(32)

    def create_response(self, challenge_nonce: bytes) -> HandshakePayload:
        """Sign the incoming challenge nonce with this node's private key."""
        pub_bytes = self.node_identity.get_public_bytes()
        # Derive SHA-256 Peer ID safely from public bytes
        derived_peer_id = getattr(self.node_identity, "peer_id", hashlib.sha256(pub_bytes).hexdigest())
        signature = self.node_identity.sign(challenge_nonce)
        
        return HandshakePayload(
            initiator_peer_id=str(derived_peer_id),
            initiator_public_bytes=pub_bytes,
            nonce=challenge_nonce,
            signature=signature
        )

    def verify_remote_node(self, payload: HandshakePayload) -> bool:
        """Strictly verify remote node's signature to prevent rogue nodes or impersonation."""
        is_valid = NodeIdentity.verify(
            payload.initiator_public_bytes,
            payload.nonce,
            payload.signature
        )

        if not is_valid:
            self.state = HandshakeState.REJECTED
            raise PermissionError("Handshake Failed: Cryptographic signature mismatch! Rogue node detected.")

        self.state = HandshakeState.AUTHENTICATED
        return True

if __name__ == "__main__":
    node_a = NodeIdentity()
    node_b = NodeIdentity()

    handshake_a = NodeHandshake(node_a)
    handshake_b = NodeHandshake(node_b)

    # 1. Node B issues challenge to Node A
    challenge = handshake_b.issue_challenge()

    # 2. Node A signs challenge and generates payload
    response_payload = handshake_a.create_response(challenge)

    # 3. Node B verifies Node A
    if handshake_b.verify_remote_node(response_payload):
        print("[HANDSHAKE] Node A identity authenticated successfully by Node B.")
        print(f"[HANDSHAKE] State: {handshake_b.state.value}")
