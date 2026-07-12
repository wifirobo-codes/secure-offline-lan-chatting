# Secure Offline LAN based Chating App

A lightweight, terminal-based chat application that enables secure, peer-to-peer communication over a local network using **AES-GCM encryption**.

## Features

*   **Peer-to-Peer:** Direct connection between two machines on the same network.
*   **Encrypted Messaging:** Uses AES-256 (GCM mode) to ensure data confidentiality and integrity.
*   **Password-Protected:** Shared "Room Codes" derive a symmetric key, ensuring only parties with the same code can read the messages.
*   **Simple Setup:** No external server infrastructure required—just a local network IP.

---

## Technical Specifications

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Cryptography** | `pycryptodome` (AES-GCM) | Provides authenticated encryption to prevent tampering. |
| **Networking** | Python `socket` | Handles low-level TCP/IP connections. |
| **Concurrency** | `threading` | Enables simultaneous sending and receiving of messages. |
| **Key Derivation** | `hashlib` (SHA-256) | Converts the room password into a fixed-length key. |

---

## Prerequisites

You will need Python 3 installed. This application requires the `pycryptodome` library. Install it via terminal/command prompt:

```bash
pip install pycryptodome
