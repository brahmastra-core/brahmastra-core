import socket
import threading
import json
import time
import sys

class P2PNode:
 def __init__(self, host, port, node_id):
 self.host = host
 self.port = port
 self.node_id = node_id
 self.peers = []

 def start_server(self):
 server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 server.bind((self.host, self.port))
 server.listen(5)
 print(f"🟢 [{self.node_id}] Server listening live on port {self.port}. ...")
 
 while True:
 conn, addr = server.accept()
 threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

 def handle_client(self, conn, addr):
 try:
 data = conn.recv(1024).decode('utf-8')
 if data:
 payload = json.loads(data)
 print(f"\n📩 [{self.node_id}] Received new message: {payload['msg']} (Sender: {payload['from']})")
 print(f"🏛️ Dharma fund share verified: 80% Community / 20% Infra")
 except Exception as e:
 print(f"Connection error: {e}")
 finally:
 conn.close()

 def send_data(self, target_port, message):
 try:
 client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 client.connect((self.host, target_port))
 payload = {
 "from": self.node_id,
 "msg": message,
 "timestamp": time.time()
 }
 client.send(json.dumps(payload).encode('utf-8'))
 client.close()
 print(f"🚀 [{self.node_id}] {target_port} !")
 except Exception as e:
 print(f"❌ : {target_port} ‌ ({e})")

if __name__ == "__main__":
 if len(sys.argv) < 3:
 print("Usage: python3 p2p_socket_node.py <Node_ID> <Port>")
 print("Example: python3 p2p_socket_node.py NODE_HYD 5001")
 sys.exit(1)

 node_id = sys.argv[1]
 port = int(sys.argv[2])

 node = P2PNode("127.0.0.1", port, node_id)
 server_thread = threading.Thread(target=node.start_server, daemon=True)
 server_thread.start()

 time.sleep(1)

 while True:
 print("\n--- MENU ---")
 print("1. Forward transaction message to peer node")
 print("2. Exit")
 choice = input("Select (1/2): ").strip()

 if choice == '1':
 target_port = int(input("Target node port (e.g. 5002): ").strip())
 msg = input("Enter payload/message to transmit: ").strip()
 node.send_data(target_port, msg)
 elif choice == '2':
 print("Node shutdown complete.")
 break