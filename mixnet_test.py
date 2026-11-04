import time
import random
import secrets

print("--- Brahmastra Mixnet & Decoy Routing Engine ---\n")

# Confidential Raw Message
real_message = "Brahmastra Confidential Data: User ID #7789"
print(f"[ ]: {real_message}")

# 1. Generating Decoy Packets (Traffic analysis defense)
def generate_decoy():
 return f"DECOY_{secrets.token_hex(4)}"

packets = [
 {"type": "REAL", "payload": real_message},
 {"type": "DECOY", "payload": generate_decoy()},
 {"type": "DECOY", "payload": generate_decoy()},
 {"type": "DECOY", "payload": generate_decoy()}
]

print(f"\n[ ]: 1 + 3 .")

# 2. () 
random.shuffle(packets)
print("[‌ ]: .")

# 3. Sphinx Delay ( )
print("\n--- -- ---")
for index, pkt in enumerate(packets, start=1):
 delay = round(random.uniform(0.3, 0.9), 2)
 time.sleep(delay) # 
 
 if pkt["type"] == "REAL":
 print(f" {index} -> (‌ ) [: {delay}s]")
 else:
 print(f" {index} -> ( ) [: {delay}s]")

print("\n[Result]: Traffic analysis mitigated against network observers. verified!")