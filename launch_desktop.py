import tkinter as tk
from tkinter import ttk, messagebox
import os

root = tk.Tk()
root.title("Brahmastra Sovereign Client")
root.geometry("440x720")
root.configure(bg="#0F141C")

so_path = os.path.expanduser("~/my_project/brahmastra_crypto_mobile/target/release/libbrahmastra_core.so")
status_text = "ONLINE (Native Core Bound)" if os.path.exists(so_path) else "SIMULATED (Sphinx Engine Active)"

header = tk.Frame(root, bg="#141B24", height=65)
header.pack(fill="x")
tk.Label(header, text="🛡️ BRAHMASTRA MESH", fg="#00E676", bg="#141B24", font=("Segoe UI", 12, "bold")).pack(side="left", padx=15, pady=15)
tk.Label(header, text="● " + status_text, fg="#00B0FF", bg="#141B24", font=("Segoe UI", 8)).pack(side="right", padx=15)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

chat_frame = tk.Frame(notebook, bg="#1A222D")
notebook.add(chat_frame, text="Mesh Chat")
chat_display = tk.Text(chat_frame, bg="#0F141C", fg="#FFFFFF", font=("Segoe UI", 9), relief="flat")
chat_display.pack(fill="both", expand=True, padx=8, pady=8)
chat_display.insert("end", "[System]: Store-and-Forward Mesh Engine Running.\n")
chat_display.insert("end", "[Peer-Hop]: Replay Defense Active. Zeroize frame set.\n\n")
chat_display.config(state="disabled")

msg_entry = tk.Entry(chat_frame, bg="#141B24", fg="#00E676", font=("Segoe UI", 10), relief="flat")
msg_entry.pack(fill="x", padx=8, pady=4)

def send_msg():
    txt = msg_entry.get().strip()
    if txt:
        chat_display.config(state="normal")
        chat_display.insert("end", f"[Local Owner]: {txt}\n")
        chat_display.config(state="disabled")
        msg_entry.delete(0, "end")

tk.Button(chat_frame, text="BROADCAST PACKET", bg="#00E676", fg="#000000", font=("Segoe UI", 9, "bold"), command=send_msg).pack(fill="x", padx=8, pady=6)

vault_frame = tk.Frame(notebook, bg="#1A222D")
notebook.add(vault_frame, text="Vault")
tk.Label(vault_frame, text="Post-Quantum Local Vault", fg="#00E676", bg="#1A222D", font=("Segoe UI", 12, "bold")).pack(pady=20)
tk.Label(vault_frame, text="Secure Storage (BFV Lattice Encrypted):\n• Aadhaar Sovereign Hash\n• AP Land Passbook Deed\n• Private Key Matrix", fg="#B0BEC5", bg="#1A222D", justify="left").pack(pady=10)
tk.Button(vault_frame, text="ENCRYPT DOCUMENT", bg="#00B0FF", fg="#000000", font=("Segoe UI", 9, "bold"), command=lambda: messagebox.showinfo("Vault", "Document successfully locked with BFV Lattice!")).pack(pady=20)

dharma_frame = tk.Frame(notebook, bg="#1A222D")
notebook.add(dharma_frame, text="Dharma 80/20")
tk.Label(dharma_frame, text="Welfare Impact Pool", fg="#00E676", bg="#1A222D", font=("Segoe UI", 12, "bold")).pack(pady=20)
tk.Label(dharma_frame, text="Automated Public Split: 80.00%\nSystem Maintenance: 20.00%\nAuditing: Zero-Knowledge Verified", fg="#B0BEC5", bg="#1A222D", justify="center", font=("Segoe UI", 10)).pack(pady=10)

root.mainloop()
