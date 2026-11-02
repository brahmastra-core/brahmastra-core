# Domain Fronting & Traffic Obfuscation Architecture (Brahmastra Core)

## 1. Threat Model & DPI Circumvention
Censorship firewalls and Deep Packet Inspection (DPI) engines inspect TLS Server Name Indication (SNI) and HTTP headers to identify and block onion routing protocols.

## 2. Domain Fronting Mechanics
- **Outer TLS SNI (Front Domain):** `ajax.googleapis.com` or `d111111abcdef8.cloudfront.net` (Permitted legitimate traffic).
- **Inner HTTP Host Header:** `entry.brahmastra.internal.net` (Target ingress node).
- **Result:** Intermediary firewalls observe ordinary Google/AWS TLS sessions, routing packets directly through trusted CDN edge points without disruption.

## 3. Traffic Camouflage & Mimicry
- Outer frames are encapsulated as standard HTTPS POST transactions (`/videoplayback`, `video/mp4`, `text/html; charset=UTF-8`).
- DPI inspection heuristics classify streams as regular YouTube video streaming or background browser telemetry.
