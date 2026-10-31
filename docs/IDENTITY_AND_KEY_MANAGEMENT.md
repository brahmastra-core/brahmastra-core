# Brahmastra Mesh Network - Peer Identity & Key Management
**Phase 3: Day 43 Architecture Specification**

## Overview
Brahmastra utilizes a zero-trust cryptographic identity layer where node identity is deterministically bound to asymmetric cryptography keys.

## Cryptographic Standards
- **Key Algorithm:** Ed25519 (RFC 8032)
  - Public Key: 32 bytes (raw)
  - Private Key: 32 bytes (raw seed) / 64 bytes
  - Signatures: 64 bytes
- **Peer ID Derivation:** SHA-256 (FIPS 180-4)
  - Formula: `Node_ID = SHA-256(Raw_Ed25519_PublicKey).hexdigest()`
  - Length: 64 hexadecimal characters

## Security Policies
1. Private keys must remain strictly within local memory / secure storage with non-root ownership (UID 10001).
2. Public keys are exchanged over the mesh network to verify packet integrity and origin authenticity.
3. Every payload transmitted across nodes must carry an Ed25519 digital signature.
