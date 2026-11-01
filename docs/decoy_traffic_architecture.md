# Decoy Traffic Generator Architecture (Dummy Packets)

## 1. Overview
In a zero-trust mixnet, an adversary observing quiescent periods can correlate transmission bursts with real user activities. Decoy (dummy) background traffic guarantees constant flow density, rendering packet volume analysis and presence detection mathematically infeasible.

## 2. Invariant & Obfuscation Properties
- **Uniform Packet Size:** Decoy packets strictly adhere to the constant 4096-byte (4 KB) packet invariant using cryptographically secure random entropy.
- **Indistinguishability:** To an outside observer or intermediary relay, decoy packets are bitwise indistinguishable from genuine Sphinx packets.
- **Silent Drop Protocol:** Encapsulated drop flags designate the payload as decoy, commanding destination relay nodes to discard the packet silently upon final decryption.

## 3. Data Structures & Engine Interface
- `DecoyPacket`: Holds routing hop metadata, unique packet identifier, creation timestamp, and padded byte sequence.
- `DecoyTrafficGenerator`: Thread-safe, non-blocking interface responsible for background traffic generation and injection.
