from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import hashlib

pdf_file = "Brahmastra_Whitepaper.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica-Bold", 16)
c.drawString(100, 750, "PROJECT BRAHMASTRA")
c.setFont("Helvetica", 12)
c.drawString(100, 720, "Sovereign Zero-Trust Computing Architecture & Dharma Economics")
c.drawString(100, 690, "Author: Naresh (Architect)")
c.drawString(100, 660, "License: Apache 2.0 | Core: Post-Quantum Lattice & FHE Primitives")
c.drawString(100, 630, "Allocation: 80% Dharma Welfare / 20% Core R&D")
c.save()

with open(pdf_file, "rb") as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

print(f"[SUCCESS] PDF Generated: {pdf_file}")
print(f"[SHA-256 HASH]: {file_hash}")
