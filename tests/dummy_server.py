import socket

# Serveur simple qui affiche ce qu'il reçoit
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8000))
sock.listen(1)
print("Client B (Destinataire) en attente sur 127.0.0.1:8000...")

while True:
    conn, addr = sock.accept()
    data = conn.recv(4096)
    print(f"\n--- MESSAGE REÇU ! ---")
    print(f"Contenu : {data.decode('utf-8')}")
    print("----------------------\n")
    conn.close()