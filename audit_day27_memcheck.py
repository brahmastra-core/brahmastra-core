import sys
from test_day26_suite import TestBrahmastraDay26Suite

def run_memory_audit():
 suite = TestBrahmastraDay26Suite()
 suite.setUp()
 
 # 1. Test FHE operations
 suite.test_01_fhe_homomorphic_addition()
 
 # 2. Test ZKP logic
 suite.test_02_zkp_verification_logic()
 
 # 3. Test 4KB padding
 suite.test_03_packet_padding_4kb()
 
 # 4. Stress run 100 iterations
 suite.test_04_stress_test_100_random_inputs()
 
 print("[AUDIT] All cryptographic and padding modules executed cleanly.")

if __name__ == "__main__":
 run_memory_audit()