import socket
import threading
import hashlib
import sys
from Crypto.Cipher import AES

# --- SECURITY FUNCTIONS ---
def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce + tag + ciphertext

def decrypt_message(key, encrypted_data):
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# --- NETWORK FUNCTIONS ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_chat():
    print("--- Secure Offline Chat ---")
    name = input("Enter your display name: ")
    mode = input("Enter 'host' to create a room, 'join' to connect: ").lower()
    room_code = input("Enter secret room code: ")
    key = derive_key(room_code)

    if mode == 'host':
        local_ip = get_local_ip()
        print(f"\n[!] Room Created! IP: {local_ip}")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 5000))
        server.listen(1)
        conn, addr = server.accept()
        print(f"[+] {addr} connected.")
    else:
        host_ip = input("Enter host IP address: ")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host_ip, 5000))
        print(f"[+] Connected to {host_ip}")

    # Exchange names immediately
    conn.send(encrypt_message(key, name))
    peer_name = decrypt_message(key, conn.recv(4096))
    print(f"--- Chat started with {peer_name} ---\n")

    # Receive thread
    def receive():
        while True:
            try:
                data = conn.recv(4096)
                if not data: break
                msg = decrypt_message(key, data)
                print(f"\n[{peer_name}]: {msg}")
                print("> ", end="", flush=True)
            except Exception:
                print("\n[!] Decryption failed. Incorrect room code?")
                break

    threading.Thread(target=receive, daemon=True).start()

    # Send loop
    while True:
        msg = input("> ")
        if msg.lower() == 'quit':
            conn.close()
            break
        conn.send(encrypt_message(key, msg))

if __name__ == "__main__":
    try:
        start_chat()
    except KeyboardInterrupt:
        sys.exit()
