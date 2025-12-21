import socket
import threading
import sys
import os

# Ajout du chemin parent pour importer les modules communs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from common import protocol
from master.db_manager import DBManager

"""
SERVEUR MASTER - ONION ROUTER
Rôle : Annuaire central. Reçoit les clés des routeurs et les donne aux clients.
Ne route PAS les messages, gère juste la topologie.
"""

HOST = '0.0.0.0' # Écoute sur toutes les interfaces
PORT = 5000      # Port par défaut du Master

class MasterServer:
    def __init__(self):
        self.db = DBManager()
        self.running = True

    def handle_client(self, conn, addr):
        """Gère une connexion entrante (Routeur ou Client)"""
        print(f"[Master] Nouvelle connexion de {addr}")
        
        try:
            data = conn.recv(4096)
            if not data:
                return

            # Utilisation de notre protocole maison (pas de JSON)
            header, args = protocol.parse_message(data)
            
            if header == "REGISTER_ROUTER":
                # args: [port_ecoute, pub_key_e, pub_key_n]
                if len(args) == 3:
                    router_port = int(args[0])
                    pub_e = args[1]
                    pub_n = args[2]
                    
                    # On enregistre l'IP réelle de la connexion
                    self.db.register_router(addr[0], router_port, pub_e, pub_n)
                    self.db.log_event(f"Router-{addr[0]}", "REGISTER", "Nouveau routeur enregistré")
                    
                    conn.send(protocol.format_message("OK", "Enregistrement reussi").encode('utf-8'))
                else:
                    print("[Master] Erreur format REGISTER")

            elif header == "GET_TOPOLOGY":
                # Le client demande la liste des routeurs
                routers = self.db.get_all_active_routers()
                
                # On doit transformer la liste en string pour l'envoyer via socket
                # Format: COUNT|||IP1:Port1:KeyE:KeyN|||IP2...
                response_args = [len(routers)]
                for r in routers:
                    # On concatène les infos d'un routeur avec ':'
                    r_str = f"{r['ip_address']}:{r['port']}:{r['pub_key_e']}:{r['pub_key_n']}"
                    response_args.append(r_str)
                
                resp = protocol.format_message("TOPOLOGY", *response_args)
                conn.send(resp.encode('utf-8'))
                self.db.log_event("Client", "REQUEST", "Topologie envoyée")

        except Exception as e:
            print(f"[Master] Erreur thread: {e}")
        finally:
            conn.close()

    def start(self):
        self.db.connect()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        
        print(f"--- SERVER MASTER EN LIGNE SUR {HOST}:{PORT} ---")
        print("En attente des routeurs...")

        try:
            while self.running:
                conn, addr = server_socket.accept()
                # Création d'un thread pour chaque connexion (AC23.03)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
        except KeyboardInterrupt:
            print("Arrêt du serveur...")
        finally:
            self.db.close()
            server_socket.close()

if __name__ == "__main__":
    master = MasterServer()
    master.start()