# Brahmastra Core - ZKP Library Architecture Analysis (Day 18)

## 1. zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge)
- **Proof Size**: Extremely small (~200 - 300 bytes), ultra-succinct on the wire.
- **Verification Complexity**: Constant time O(1), highly optimal for low-latency peer validation.
- **Trade-off**: Requires a Structured Reference String (SRS) / Trusted Setup ceremony.
- **Suitability**: High-throughput distributed ledger transactions where proof verification must take <1ms.

## 2. Bulletproofs
- **Proof Size**: Logarithmic size O(log N), larger than SNARKs (~1 KB to 2 KB).
- **Verification Complexity**: Linear with circuit size O(N), higher verification overhead.
- **Advantage**: Transparent setup. Zero trusted setup ceremonies or toxic waste parameters.
- **Suitability**: Confidential transactions and Range Proofs (e.g., balance > 0, age >= 18) without central trust assumptions.

## Architectural Decision for Brahmastra Core
Brahmastra adopts a hybrid model:
1. **Bulletproof-style transparent circuits** for decentralized identity validation (identity anonymity without trusted parties).
2. **Succinct verifiable circuits** for inter-node state transitions and cryptographic routing.
