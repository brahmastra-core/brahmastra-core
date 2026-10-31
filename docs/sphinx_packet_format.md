# Sphinx Packet Format Specification (Constant Size Anonymous Routing)

## 1. Overview
The Sphinx packet format provides provable anonymity and cryptographically enforces constant packet size across all hops in the mesh network. This completely mitigates packet-size fingerprinting and traffic analysis attacks.

## 2. Packet Layout & Fixed Byte Budget
Every Sphinx packet is padded to a strictly constant size of **1024 Bytes**:
- **Alpha ($\alpha$) [32 Bytes]:** Ephemeral public key (Curve25519) used for Diffie-Hellman shared secret derivation at each hop.
- **Beta ($\beta$) [160 Bytes]:** Encrypted routing information token containing the next hop address and per-hop routing commands.
- **Gamma ($\gamma$) [16 Bytes]:** HMAC-SHA256 authentication tag to detect any unauthorized packet tampering.
- **Delta ($\delta$) [816 Bytes]:** Encrypted payload padded to maintain uniform byte length.

$$\text{Total Packet Size} = 32 + 160 + 16 + 816 = 1024 \text{ Bytes (Constant)}$$

## 3. Constant-Size Hop Transformation (Padding Invariant)
When Node $i$ processes packet $P_i$:
1. Uses private key $SK_i$ and packet $\alpha$ to derive shared secret $s_i$.
2. Verifies integrity tag $\gamma$. If invalid, drops packet immediately.
3. Decrypts routing instructions from $\beta$, discovering the next hop address $\text{Addr}_{i+1}$.
4. Shifts $\beta$ to reveal the inner layer and appends deterministic pseudo-random padding $\rho_i$ generated from $s_i$ to ensure $|\beta|$ never shrinks.
5. Blinds public key $\alpha \rightarrow \alpha'$ for the next hop.
6. The resulting packet $P_{i+1}$ transmitted to the next hop remains **strictly 1024 Bytes**.

## 4. Resource Constraints Compliance
- Operations utilize pre-allocated fixed memory buffers adhering strictly to the <80MB RAM and <1ms latency ceilings.
