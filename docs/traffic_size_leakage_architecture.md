# Traffic Size Leakage Defense Architecture (Brahmastra Core)

## 1. Overview & Threat Model
In an anonymous mixnet, passive wire sniffers observe packet lengths traversing intermediate links. Variable-length payloads directly reveal traffic characteristics, enabling packet-size correlation attacks.

## 2. 4096-Byte Constant Packet Invariant
- Every onion-routed frame transmitted across any node link is strictly padded to exactly **4096 bytes (4 KB)**.
- Regardless of plaintext size ($0 \le \text{len} \le 4000$ bytes), cryptographic dummy bytes with high entropy fill the frame.
- Frame Format:
  `[Length: 4 bytes big-endian] + [Payload: N bytes] + [High-Entropy Padding: (4092 - N) bytes]`

## 3. Wire Sniffing & Side-Channel Mitigation
- Observers on intermediate relays see only identical 4096-byte blocks.
- Packet length entropy is zero ($H(\text{Size}) = 0$), defeating size-based statistical fingerprinting.
