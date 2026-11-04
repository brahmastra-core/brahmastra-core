import os
import sys
import json
import time

LEDGER_FILE = "dharma_ledger.json"

def clear_screen():
 os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
 clear_screen()
 print("=" * 60)
 print(" 🏹 BRAHMASTRA-CORE DASHBOARD 🏹 ")
 print(" Decentralized Dharma Protocol Command Center ")
 print("=" * 60)

def view_ledger():
 if not os.path.exists(LEDGER_FILE):
 print("\n⚠️ Ledger file not found. Please initiate a transaction.")
 return
 with open(LEDGER_FILE, "r") as f:
 data = json.load(f)
 
 print("\n--- [On-Chain Dharma Fund Reserves] ---")
 print(f"🏛️ Dharma Welfare Pool : {data.get('total_dharma_pool', 0):.2f} Credits")
 print(f"⚙️ Network Infra Pool : {data.get('total_infra_pool', 0):.2f} Credits")
 print(f"📦 Total Blocks : {len(data.get('chain', []))}")
 print("\n--- [Recent Blocks History] ---")
 for block in data.get('chain', [])[-3:]:
 print(f"Block #{block['block_id']} | From: {block['sender']} -> To: {block['receiver']} | Amt: {block['amount']} Cr")
 print(f"Hash: {block['block_hash'][:24]}...")
 print("-" * 40)

def send_transaction():
 try:
 from dharma_ledger import record_transaction
 print("\n--- [Create New Transaction] ---")
 sender = input("Sender Node ID (e.g. NODE_HYD_01): ").strip()
 receiver = input("Receiver Node ID (e.g. NODE_SGP_01): ").strip()
 amount_str = input("‌ Credits : ").strip()
 if not sender or not receiver or not amount_str:
 print("❌ Invalid input details provided!")
 return
 amount = float(amount_str)
 record_transaction(sender, receiver, amount)
 except Exception as e:
 print(f"❌ Transaction Failed: {e}")

def main_menu():
 while True:
 show_banner()
 print("\n1. 📊 View Dharma Fund & Blockchain Ledger")
 print("2. 💸 Record New Transaction")
 print("3. 🛡️ Run Abhedya Shield Security Audit")
 print("4. 🌐 Simulate 5-Node Multi Consensus")
 print("5. ❌ Exit")
 print("=" * 60)
 
 choice = input("Enter your choice (1-5): ").strip()
 
 if choice == '1':
 view_ledger()
 input("\nPress Enter to continue...")
 elif choice == '2':
 send_transaction()
 input("\nPress Enter to continue...")
 elif choice == '3':
 os.system("python3 security_audit.py")
 input("\nPress Enter to continue...")
 elif choice == '4':
 os.system("python3 multi_node_sim.py")
 input("\nPress Enter to continue...")
 elif choice == '5':
 print("\n👋 Brahmastra Command Center Terminated.")
 sys.exit(0)
 else:
 print("❌ Choice !")
 time.sleep(1)

if __name__ == "__main__":
 main_menu()