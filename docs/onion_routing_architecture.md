# 3-Hop Onion Routing Mathematical Architecture

## 1. Overview
The CloakCompute onion routing protocol employs a 3-hop layered cryptographic model designed for resource-constrained mesh nodes. The architecture guarantees zero-knowledge routing where no single node knows both the origin and final destination.

## 2. Mathematical Layer Formulation
Given:
- Plaintext payload: $M$
- Destination address: $D$
- Nodes in circuit: $N_1$ (Entry), $N_2$ (Relay), $N_3$ (Exit)
- Public keys: $PK_1, PK_2, PK_3$

The onion envelope is constructed in reverse order by the sender:
1. **Layer 3 (Exit Layer):**
 $$C_3 = \text{Encrypt}(PK_3, M \parallel D)$$
2. **Layer 2 (Relay Layer):**
 $$C_2 = \text{Encrypt}(PK_2, C_3 \parallel \text{Addr}(N_3))$$
3. **Layer 1 (Entry Layer):**
 $$C_1 = \text{Encrypt}(PK_1, C_2 \parallel \text{Addr}(N_2))$$

The final packet dispatched to $N_1$ is $C_1$.

## 3. Node Unwrapping Properties (Hop Isolation)
- **Node 1 ($N_1$ - Entry):**
 Decrypts $C_1$ using secret key $SK_1$. Learns $\text{Addr}(N_2)$ and receives opaque payload $C_2$. Origin is known; destination and payload $M$ remain hidden.
- **Node 2 ($N_2$ - Relay):**
 Decrypts $C_2$ using secret key $SK_2$. Learns $\text{Addr}(N_3)$ and receives opaque payload $C_3$. Neither origin nor destination is known.
- **Node 3 ($N_3$ - Exit):**
 Decrypts $C_3$ using secret key $SK_3$. Recovers final payload $M$ and forwards to destination $D$. Origin remains completely hidden.

## 4. Resource Constraints Compliance
- Cryptographic operations strictly adhere to the 80MB RAM ceiling and sub-millisecond per-hop peel latency.
