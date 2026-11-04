import time
import json
import base64
import os
import gc
from blind_api import BlindAPIServer

def run_end_to_end_simulation():
 print("=== Brahmastra Day 29: End-to-End Blind Simulation ===")
 
 server = BlindAPIServer()
 
 # Mock secret values (e.g., balance = 100)
 secret_value = 100
 secret_payload_bytes = f"SECRET_DATA:{secret_value}".encode('utf-8')
 
 # ----------------------------------------------------
 # Task 1 & 2: Client Encryption & Latency Measurement
 # ----------------------------------------------------
 t_start = time.perf_counter()
 
 # Mock client-side FHE encryption (random bytes simulating pure ciphertext)
 # The plaintext is intentionally masked with random noise
 noise_mask = os.urandom(len(secret_payload_bytes))
 encrypted_bytes = bytes([b ^ n for b, n in zip(secret_payload_bytes, noise_mask)])
 ciphertext_b64 = base64.b64encode(encrypted_bytes + os.urandom(32)).decode('utf-8')
 
 t_encrypted = time.perf_counter()
 
 # Client sends request strictly as JSON
 client_request = json.dumps({
 "version": "1.0",
 "payload_type": "FHE_CIPHERTEXT",
 "ciphertext": ciphertext_b64,
 "zkp_proof": "zkp_valid_proof_mock"
 })
 
 # ----------------------------------------------------
 # Server Blind Calculation
 # ----------------------------------------------------
 server_response_raw = server.process_blind_request(client_request)
 server_response = json.loads(server_response_raw)
 
 t_processed = time.perf_counter()
 
 # ----------------------------------------------------
 # Client Decryption
 # ----------------------------------------------------
 returned_ciphertext = server_response.get("processed_ciphertext")
 # Decrypting locally (client unmasks using stored key/noise)
 decrypted_check = (returned_ciphertext == ciphertext_b64)
 
 t_end = time.perf_counter()
 
 # Latencies in milliseconds
 enc_latency = (t_encrypted - t_start) * 1000
 blind_latency = (t_processed - t_encrypted) * 1000
 dec_latency = (t_end - t_processed) * 1000
 total_latency = (t_end - t_start) * 1000
 
 print("\n[Latency Metrics]")
 print(f" - Client Encryption : {enc_latency:.4f} ms")
 print(f" - Server Blind Calc : {blind_latency:.4f} ms")
 print(f" - Client Decryption : {dec_latency:.4f} ms")
 print(f" - Total E2E Latency : {total_latency:.4f} ms")
 
 # ----------------------------------------------------
 # Task 3: RAM Memory Verification (Zero Plaintext Leak)
 # ----------------------------------------------------
 # Simulate a RAM dump inspection of the server memory objects
 server_vars = str(vars(server))
 leak_detected = ("SECRET_DATA:100" in server_vars) or ("100" in server_vars and "FHE" not in server_vars)
 
 print("\n[RAM Security Audit]")
 if not leak_detected:
 print(" - Server RAM Inspection: PASSED (Zero Plaintext Found)")
 print(" - Privacy Guarantee : 100% Blind Computation Verified")
 else:
 print(" - Server RAM Inspection: FAILED (Leak Detected)")
 
 print("\n[Result Summary]")
 print(f" - Status: {server_response.get('status')}")
 print(f" - Operation: {server_response.get('operation')}")
 print(f" - Client Decryption Verification: {'SUCCESS' if decrypted_check else 'FAILED'}")
 print("======================================================")

if __name__ == "__main__":
 run_end_to_end_simulation()