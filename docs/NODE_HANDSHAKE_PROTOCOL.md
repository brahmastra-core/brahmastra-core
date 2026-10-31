# Brahmastra Mesh Network - Node-to-Node Handshake Specification

## 1. Overview & Objective
To maintain a strict Zero-Trust architecture across untrusted networks, any two nodes establishing a direct P2P link must perform a cryptographically verified, mutual handshake before exchanging any routed traffic.

## 2. Handshake Mechanics
1. **Challenge Issuance**: Initiator broadcasts an ephemeral session request accompanied by a random cryptographic nonce.
2. **Mutual Ed25519 Verification**: Both initiator and responder must sign the challenge nonce using their private identity keys. Connections lacking verifiable signatures are immediately dropped.
3. **Session Key Derivation**: Both nodes derive an ephemeral, forward-secret symmetric key (ChaCha20-Poly1305 / Noise framework) valid only for the lifespan of that specific tunnel.

## 3. Threat Mitigation
- **Anti-Impersonation**: Prevents rogue nodes from spoofing verified Peer IDs.
- **Anti-Replay**: Every handshake requires freshly generated 32-byte nonces.
- **Forward Secrecy**: Node identity compromise does not retroactively expose historical session traffic.
