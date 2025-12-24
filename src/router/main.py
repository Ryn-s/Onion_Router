import socket
import threading
import sys
import os
import time

# Permet d'importer nos modules communs (Crypto et Protocol)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from common.config import MASTER_IP, MASTER_PORT
from common import protocol
from common.crypto_utils import RSACipher

"""
ROUTEUR ONION - PROJET R3.09
Auteur : Rayan
Description : 
Le routeur génère ses clés au démarrage, s'enregistre au Master,
et attend les paquets. Il ne connait que le saut suivant.
"""

# Configuration
MASTER_PORT = 5000
MY_PORT = 0 

class OnionRouter:
    def __init__(self):
        self.running = True
        self.rsa = RSACipher(key_size=1024) 
        self.port = 0
        
        print("[Router] Génération des clés RSA (ça peut prendre 5-10 sec)...")
        self.pub_key, self.priv_key = self.rsa.generate_keys()
        print(f"[Router] Clés générées. Exposant public : {self.pub_key[0]}")

    def register_to_master(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((MASTER_IP, MASTER_PORT))
            
            # Protocole : REGISTER_ROUTER ||| PORT ||| KEY_E ||| KEY_N
            msg = protocol.format_message(
                "REGISTER_ROUTER", 
                self.port, 
                self.pub_key[0], 
                self.pub_key[1]
            )
            
            sock.send(msg.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            print(f"[Master] Réponse : {response}")
            sock.close()
            return True
        except ConnectionRefusedError:
            print("[Erreur] Impossible de joindre le Master. Est-il lancé ?")
            return False

    def handle_incoming_packet(self, conn, addr):
        """
        Cœur du routage : Reçoit un message chiffré, le déchiffre et le transfère.
        """
        print(f"[Réseau] Connexion entrante de {addr}")
        try:
            # On reçoit le paquet chiffré (format string avec des /)
            encrypted_data = conn.recv(16384).decode('utf-8') # J'ai augmenté le buffer au cas où
            
            print(f"[Anonymat] Trame chiffrée reçue : {encrypted_data[:30]}... [Total: {len(encrypted_data)} octets]")

            if not encrypted_data:
                return

            print(f"[Crypto] Message chiffré reçu ({len(encrypted_data)} bytes). Déchiffrement...")
            
            
            # On passe directement la chaîne (ex: "123/456") à decrypt.
            # On NE convertit PAS en int() car c'est une suite de blocs maintenant.
            decrypted_packet = self.rsa.decrypt(encrypted_data)
            
            if decrypted_packet is None or decrypted_packet == "":
                print("[Erreur] Échec du déchiffrement (Mauvaise clé ou message vide)")
                return

            # 2. ANALYSE DU PAQUET DÉCHIFFRÉ
            if "|||" in decrypted_packet:
                # Ce n'est pas la destination finale, il faut faire suivre
                routing_info, next_payload = decrypted_packet.split("|||", 1)
                
                try:
                    next_ip, next_port = routing_info.split(":")
                    next_port = int(next_port)
                    
                    print(f"[Routage] Relai vers {next_ip}:{next_port}")
                    self.forward_packet(next_ip, next_port, next_payload)
                except ValueError:
                    print(f"[Erreur] Format de route incorrect : {routing_info}")
            else:
                # C'est la destination finale ou le dernier saut a mal formaté
                # Si on est le dernier routeur, decrypted_packet contient "IP_DEST:PORT|||MESSAGE"
                # Mais ici on a déjà splité plus haut si il y avait des |||
                # Si on est ici, c'est que le message est le payload final
                print(f"[Final] Message déchiffré (contenu brut) : {decrypted_packet}")

        except Exception as e:
            print(f"[Erreur] Traitement paquet : {e}")
            import traceback
            traceback.print_exc() # Affiche l'erreur exacte pour nous aider
        finally:
            conn.close()

    def forward_packet(self, ip, port, payload):
        """Envoie le paquet restant au prochain nœud"""
        try:
            time.sleep(1) 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(payload.encode('utf-8'))
            sock.close()
            print(f"[Succès] Paquet transféré à {ip}:{port}")
        except Exception as e:
            print(f"[Erreur] Impossible de transférer à {ip}:{port} - {e}")

    def unregister_from_master(self):
        """Prévient le Master qu'on s'éteint"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((MASTER_IP, MASTER_PORT))
            # On envoie : UNREGISTER_ROUTER ||| MON_PORT
            msg = protocol.format_message("UNREGISTER_ROUTER", self.port)
            sock.send(msg.encode('utf-8'))
            sock.close()
            print("[Info] Désinscription envoyée au Master.")
        except:
            print("[Warning] Impossible de prévenir le Master (déjà éteint ?)")


    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', MY_PORT))
        self.port = server_socket.getsockname()[1]
        server_socket.listen(10)
        
        print(f"--- ROUTEUR DÉMARRÉ SUR LE PORT {self.port} ---")
        
        if self.register_to_master():
            print("[Info] Routeur prêt et en attente de paquets...")
            try:
                while self.running:
                    conn, addr = server_socket.accept()
                    t = threading.Thread(target=self.handle_incoming_packet, args=(conn, addr))
                    t.start()
            except KeyboardInterrupt:
                print("\n[Arrêt] Interruption détectée (Ctrl+C).")
                # ---  On se désinscrit avant de quitter ---
                self.unregister_from_master()
                # -----------------------------------------------------
            finally:
                server_socket.close()
        else:
            print("Arrêt : Impossible de s'enregistrer au Master.")
if __name__ == "__main__":
    router = OnionRouter()
    router.start()