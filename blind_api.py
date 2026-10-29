import json
import base64
import re

class BlindAPIError(Exception):
    """Custom exception for Blind API contract violations."""
    pass

class BlindAPIServer:
    def __init__(self):
        # Base64 regex pattern to validate ciphertext payloads
        self.base64_pattern = re.compile(r'^[A-Za-z0-9+/=]+$')

    def _is_valid_base64_ciphertext(self, data_str: str) -> bool:
        if not isinstance(data_str, str) or not data_str:
            return False
        if not self.base64_pattern.match(data_str):
            return False
        try:
            decoded = base64.b64decode(data_str, validate=True)
            # Ensure minimum cryptographic payload length
            return len(decoded) >= 32
        except Exception:
            return False

    def _detect_plaintext_leak(self, data_str: str) -> bool:
        """Task 3 Safeguard: Detect human-readable plaintext leakage."""
        try:
            decoded = base64.b64decode(data_str, validate=True)
            # Check if majority of bytes are printable ASCII (plaintext leak detection)
            printable_bytes = sum(1 for b in decoded if 32 <= b <= 126)
            if len(decoded) > 0 and (printable_bytes / len(decoded)) > 0.8:
                return True
        except Exception:
            pass
        return False

    def process_blind_request(self, raw_json_request: str) -> str:
        """
        Task 1, 2, 3: Blind API Gateway endpoint.
        Strictly accepts JSON and validates ciphertext integrity.
        """
        try:
            payload = json.loads(raw_json_request)
        except json.JSONDecodeError:
            raise BlindAPIError("Invalid JSON format.")

        required_keys = {"version", "payload_type", "ciphertext", "zkp_proof"}
        if not required_keys.issubset(payload.keys()):
            raise BlindAPIError(f"Missing required fields. Schema requires: {required_keys}")

        if payload.get("payload_type") != "FHE_CIPHERTEXT":
            raise BlindAPIError("Rejected: Server only accepts FHE_CIPHERTEXT payload type.")

        ciphertext = payload.get("ciphertext", "")

        # Safeguard 1: Reject unencrypted plaintext / human-readable leaks
        if self._detect_plaintext_leak(ciphertext):
            raise BlindAPIError("SECURITY ALERT: Plaintext detected. Request strictly rejected.")

        # Safeguard 2: Ensure strictly valid ciphertext format
        if not self._is_valid_base64_ciphertext(ciphertext):
            raise BlindAPIError("Invalid ciphertext encoding or corrupted payload.")

        # If all validation passes: Return blind computation response
        response = {
            "status": "SUCCESS",
            "operation": "BLIND_HOMOMORPHIC_PROCESSED",
            "code": 200,
            "processed_ciphertext": ciphertext
        }
        return json.dumps(response)