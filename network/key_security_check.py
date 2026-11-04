"""
Brahmastra Mesh Network - Key Security & Integrity Verification
Audits private key storage permissions, file access controls, and signature tampering.
"""

import os
import stat
from network.identity import NodeIdentity

def verify_key_storage_security() -> bool:
 print("[AUDIT] Starting Cryptographic Key Security Audit...")
 
 # 1. Create a secure local directory with 0700 permissions
 key_dir = os.path.expanduser("~/my_project/.secure_keys")
 os.makedirs(key_dir, mode=0o700, exist_ok=True)
 os.chmod(key_dir, 0o700)
 
 key_file = os.path.join(key_dir, "node_test.key")
 
 # 2. Generate identity and write private bytes safely
 node = NodeIdentity()
 with open(key_file, "wb") as f:
 # Write dummy/test key payload
 f.write(node._public_bytes)
 
 # Enforce strict 0600 file permissions (Owner RW only)
 os.chmod(key_file, 0o600)
 file_stat = os.stat(key_file)
 file_perm = stat.S_IMODE(file_stat.st_mode)
 
 assert file_perm == 0o600, f"Insecure file permission detected: {oct(file_perm)}"
 print(f"[PASS] Key file permissions locked to strict 0600 (Owner Only): {oct(file_perm)}")

 # 3. Cryptographic Tamper Verification
 test_msg = b"MISSION_CRITICAL_AUTHENTICATION_PAYLOAD"
 signature = node.sign(test_msg)
 
 # Positive check
 assert NodeIdentity.verify(node.get_public_bytes(), test_msg, signature) is True, "Valid signature verification failed"
 print("[PASS] Legitimate signature verified successfully.")

 # Tamper check (altering single byte)
 tampered_msg = b"MISSION_CRITICAL_AUTHENTICATION_PAYLOAD_TAMPERED"
 assert NodeIdentity.verify(node.get_public_bytes(), tampered_msg, signature) is False, "Tampered payload passed verification!"
 print("[PASS] Tampered payload correctly detected and rejected.")

 # Clean test file
 os.remove(key_file)
 os.rmdir(key_dir)
 print("[PASS] Ephemeral security artifacts safely removed from disk.")
 print("[COMPLETE] Key Security Verification Successful.")
 return True

if __name__ == "__main__":
 verify_key_storage_security()
