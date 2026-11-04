"""
Brahmastra Mesh Network - Node Cryptographic Identity Layer
Handles Ed25519 key generation, signing, verification, and SHA-256 Peer-ID derivation.
"""

import hashlib
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class NodeIdentity:
 """Represents a cryptographic identity for a zero-trust mesh node."""

 def __init__(self, private_key: Optional[ed25519.Ed25519PrivateKey] = None) -> None:
 if private_key is None:
 self._private_key = ed25519.Ed25519PrivateKey.generate()
 else:
 self._private_key = private_key
 
 self._public_key = self._private_key.public_key()
 self._public_bytes = self._public_key.public_bytes(
 encoding=serialization.Encoding.Raw,
 format=serialization.PublicFormat.Raw
 )
 self.node_id = self._derive_node_id()

 def _derive_node_id(self) -> str:
 """Derive canonical 64-char hex Node ID via SHA-256 hashing of raw public key."""
 return hashlib.sha256(self._public_bytes).hexdigest()

 def get_public_bytes(self) -> bytes:
 """Return 32-byte raw public key."""
 return self._public_bytes

 def sign(self, message: bytes) -> bytes:
 """Cryptographically sign an arbitrary byte payload using Ed25519."""
 return self._private_key.sign(message)

 @staticmethod
 def verify(public_bytes: bytes, message: bytes, signature: bytes) -> bool:
 """Verify an Ed25519 signature against raw public key bytes."""
 try:
 public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
 public_key.verify(signature, message)
 return True
 except Exception:
 return False

 def export_identity(self) -> Dict[str, Any]:
 """Export public metadata for peer advertisement."""
 return {
 "node_id": self.node_id,
 "public_key_hex": self._public_bytes.hex(),
 "algorithm": "Ed25519",
 "hash_algorithm": "SHA-256"
 }

if __name__ == "__main__":
 identity = NodeIdentity()
 metadata = identity.export_identity()
 print("[INIT] Node Identity Generated Successfully")
 print(f"Node ID (SHA-256): {metadata['node_id']}")
 print(f"Public Key (Hex): {metadata['public_key_hex']}")
 
 test_data = b"BRAHMASTRA_ZERO_TRUST_PACKET"
 sig = identity.sign(test_data)
 valid = NodeIdentity.verify(identity.get_public_bytes(), test_data, sig)
 print(f"Cryptographic Signature Valid: {valid}")
