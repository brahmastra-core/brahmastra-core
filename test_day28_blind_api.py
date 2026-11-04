import unittest
import json
import base64
import os
from blind_api import BlindAPIServer, BlindAPIError

class TestBlindAPISuite(unittest.TestCase):
 def setUp(self):
 self.server = BlindAPIServer()
 # 64-byte random encrypted mock ciphertext
 self.valid_ciphertext = base64.b64encode(os.urandom(64)).decode('utf-8')

 def test_01_valid_ciphertext_accepted(self):
 """Task 2: Ensure valid ciphertext JSON is accepted."""
 req = json.dumps({
 "version": "1.0",
 "payload_type": "FHE_CIPHERTEXT",
 "ciphertext": self.valid_ciphertext,
 "zkp_proof": "valid_zkp_signature_stub"
 })
 res = self.server.process_blind_request(req)
 self.assertIn("BLIND_HOMOMORPHIC_PROCESSED", res)

 def test_02_plaintext_leak_rejected(self):
 """Task 3: Ensure human-readable plaintext is rejected immediately."""
 leaked_plaintext = base64.b64encode(b"This is secret unencrypted data! Hello Server").decode('utf-8')
 req = json.dumps({
 "version": "1.0",
 "payload_type": "FHE_CIPHERTEXT",
 "ciphertext": leaked_plaintext,
 "zkp_proof": "stub"
 })
 with self.assertRaises(BlindAPIError) as ctx:
 self.server.process_blind_request(req)
 self.assertIn("SECURITY ALERT: Plaintext detected", str(ctx.exception))

 def test_03_invalid_payload_type_rejected(self):
 """Task 2: Reject non-FHE types."""
 req = json.dumps({
 "version": "1.0",
 "payload_type": "PLAINTEXT_DATA",
 "ciphertext": self.valid_ciphertext,
 "zkp_proof": "stub"
 })
 with self.assertRaises(BlindAPIError):
 self.server.process_blind_request(req)

if __name__ == "__main__":
 unittest.main()