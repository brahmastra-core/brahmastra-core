# Sphinx Packet Poisson Delay Architecture

## 1. Overview
In a sovereign decentralized mixnet, constant-size packets (1024 bytes) prevent packet-size correlation attacks. However, a Global Passive Adversary (GPA) monitoring network link ingress and egress can still perform timing analysis (traffic correlation).

To neutralize timing correlation attacks, each relay node introduces a stochastic delay sampled from an exponential distribution (Poisson process) before forwarding the Sphinx packet.

## 2. Mathematical Foundation
The arrival and departure intervals follow a Poisson process. The inter-hop delay \Delta t is computed using the inverse transform sampling of the continuous exponential distribution:

\Delta t = - \ln(U) / \lambda

Where:
- U in (0, 1] is a cryptographically secure uniform random variable.
- \lambda (lambda) is the Poisson rate parameter (packets per second or scale factor).
- Mean delay is E[\Delta t] = 1 / \lambda.
- A ceiling clamp of T_max = 200 ms is enforced to guarantee user experience and prevent indefinite packet hoarding.

## 3. Data Structures & Engine Interface
- `DelayedSphinxPacket`: Encapsulates Sphinx packet payload, ingestion timestamp, scheduled release timestamp, and target routing hop.
- `SphinxDelayEngine`: Non-blocking, event-driven queue prioritizing release times without violating the strict 80MB RAM envelope.
