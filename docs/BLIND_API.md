# Brahmastra Protocol - Blind API Documentation (Day 28)

## 1. Overview
The Blind API enforces a zero-trust interface between nodes and clients. The server executes computations strictly on ciphertext without ever decrypting or inspecting plaintext payloads.

## 2. Security Safeguards
- **Zero-Plaintext Policy**: Any human-readable or unencrypted plaintext payload is rejected at the gateway.
- **Ciphertext Validation**: Payloads must be base64-encoded encrypted byte blocks meeting cryptographic minimum lengths.
- **Payload Type Enforcement**: Only `FHE_CIPHERTEXT` requests are permitted.

## 3. Communication Schema (JSON / Wire Format)

### Request Specification
```json
{
 "version": "1.0",
 "payload_type": "FHE_CIPHERTEXT",
 "ciphertext": "<base64-encoded-fhe-ciphertext>",
 "zkp_proof": "<base64-encoded-zero-knowledge-proof>"
}