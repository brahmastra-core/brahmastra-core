# Engineering Architecture: Mixnet & Sphinx Packet Routing Core

## 1. Constant Packet Padding (4 KB) Mathematical Formulation
In Brahmastra anonymous overlay network, packet size indistinguishability is enforced across all mix hops to eliminate packet length side-channel metadata:
$$|M_i| = 4096 \text{ Bytes (Constant)}, \quad \forall i \in [1, \kappa]$$

### 1.1 Invariant Length Mechanics
Each Sphinx packet maintains a fixed header $H$ and encrypted payload $P$:
- Fixed Header: $|H| = 192 \text{ Bytes}$
- Fixed Payload: $|P| = 3904 \text{ Bytes}$
- Strict Total: $|H| + |P| = 4096 \text{ Bytes}$

Upon each hop transition $k$, the routing node strips its ephemeral header, unmasks the payload, and regenerates deterministic pseudo-random trailing bytes:
$$P_{k+1} = \text{Trunc}_{3904}(D_{k}(P_k) \parallel \text{PRG}(s_k))$$
This guarantees invariant length conservation where no passive adversary can correlate ingress and egress packet size.

## 2. Poisson Delay Distribution & Traffic Analysis Hardness
To counter global timing correlation and traffic confirmation attacks, mix nodes decouple packet arrival from transmission using an independent memoryless Poisson process.

### 2.1 Exponential Distribution Formulation
Inter-departure delay $\tau$ is sampled independently from an exponential distribution with parameter $\mu$:
$$f(\tau; \mu) = \mu e^{-\mu \tau}, \quad \tau \ge 0$$
Mean latency induced per mix node:
$$\mathbb{E}[\tau] = \frac{1}{\mu}$$

### 2.2 Anonymity Set Entropy Bound
For a continuous flow of $n$ indistinguishable packets buffered within a mixing epoch $\Delta t$, the anonymity set entropy $\mathcal{H}$ satisfies:
$$\mathcal{H}(X) = - \sum_{i=1}^n p_i \log_2(p_i) = \log_2(n) \text{ bits}$$
With uniform mixing distribution, the adversary advantage is strictly bounded:
$$\mathbf{Adv}_{\text{traffic}}(A) \le 2^{-\mathcal{H}(X)} = \frac{1}{n}$$

## 3. Mixnet & Sphinx Architectural Parameters Table
| Protocol Parameter | Specification | Architectural Purpose |
| :--- | :--- | :--- |
| **Strict Packet Size** | 4096 Bytes (4 KB) | Prevents packet size correlation |
| **Header Allocation** | 192 Bytes | Onion routing key derivation & MAC |
| **Payload Capacity** | 3904 Bytes | Post-quantum lattice ciphertext carrying capacity |
| **Delay Strategy** | Poisson Process (Mean $\mu = 50\text{ms}$) | Destroys timing correlation vectors |
| **Security Standard** | IACR Sphinx Spec & Anonymity Entropy Bounds | Provably secure traffic analysis defense |
