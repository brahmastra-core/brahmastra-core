# Security Policy & Bug Bounty Program

## Brahmastra Protocol Security Commitment
Security and cryptographic integrity are paramount to the **Brahmastra Protocol**. We operate on zero-trust principles and welcome ethical hackers, cryptanalysts, and developers to audit our codebase.

---

## Scope of Bounty Program
The bounty program covers critical vulnerabilities across the following modules:
1. **Lattice-Based Homomorphic Encryption (BFV Core)**: Ciphertext malleability, plaintext leakage, or lattice parameter downgrade attacks.
2. **Decentralized P2P Mixnet**: Sphinx packet padding verification (4096-byte constant verification), timing resistance, and zero-metadata guarantees.
3. **Schnorr ZKP Engine**: Zero-knowledge proof forgery or private key exposure.
4. **Dharma Welfare Smart Accounting**: Exploitation of the immutable 80/20 allocation mechanism or ledger manipulation.

---

## Vulnerability Severity & Reward Structure

| Severity | Description | Reward & Recognition |
| :--- | :--- | :--- |
| **Critical** | Remote code execution, lattice decryption breakdown, secret key exposure. | Protocol Grant Bounty Allocation + Permanent Hall of Fame |
| **High** | Traffic deanonymization in mixnet, denial of service across consensus nodes. | Grant Bounty Share + Permanent Hall of Fame |
| **Medium** | Edge-case consensus stalls, serialization exceptions in context split. | Priority Attribution in `docs/HALL_OF_FAME.md` |
| **Low** | Minor documentation, typing, or logging inconsistencies. | Contributor Attribution in Release Notes |

---

## Reporting a Vulnerability
- **Do not open public GitHub issues for security vulnerabilities.**
- Submit detailed proof-of-concept (PoC) reports via GitHub Security Advisories or directly to the core architecture maintainers.
- Responsible disclosure applies: please allow up to 72 hours for triage before public discussion.
