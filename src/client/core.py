import socket
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from common import protocol
from common.crypto_utils import RSACipher

class ClientCore:
    def __init__(self, master_ip='127.0.0.1', master_port=5000):
        self.master_ip = master_ip
        self.master_port = master_port
        self.rsa = RSACipher() 
        self.available_routers = []

    def fetch_topology(self):
        """Demande la liste des routeurs au Master"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.master_ip, self.master_port))
            
            sock.send(protocol.format_message("GET_TOPOLOGY").encode('utf-8'))
            data = sock.recv(16384).decode('utf-8')
            sock.close()

            header, args = protocol.parse_message(data)
            if header == "TOPOLOGY":
                self.available_routers = []
                for r_str in args[1:]:
                    ip, port, e, n = r_str.split(':')
                    self.available_routers.append({
                        'ip': ip,
                        'port': int(port),
                        'pub_key': (int(e), int(n))
                    })
                return True
            return False
        except Exception as e:
            print(f"[Client] Erreur connexion Master : {e}")
            return False

    def create_onion(self, message, destination_ip, destination_port, specific_path=None):
        """
        Construit le message en oignon.
        specific_path : Liste ordonnée de 3 routeurs (optionnel).
        """
        if len(self.available_routers) < 3:
            raise Exception("Pas assez de routeurs en ligne (min 3 requis)")

        # --- LOGIQUE DE SÉLECTION ---
        if specific_path:
            # Mode Manuel : On utilise la liste fournie par l'IHM
            if len(specific_path) != 3:
                raise Exception("Le chemin manuel doit contenir exactement 3 routeurs.")
            r1, r2, r3 = specific_path[0], specific_path[1], specific_path[2]
            print(f"[Oignon] Mode MANUEL : R1({r1['port']}) -> R2({r2['port']}) -> R3({r3['port']})")
        else:
            # Mode Aléatoire
            path = random.sample(self.available_routers, 3)
            r1, r2, r3 = path[0], path[1], path[2]
            print(f"[Oignon] Mode ALÉATOIRE : R1({r1['port']}) -> R2({r2['port']}) -> R3({r3['port']})")

        # --- CONSTRUCTION (Identique à avant) ---
        
        # COUCHE 3 (Pour R3 -> Dest)
        payload_3 = f"{destination_ip}:{destination_port}|||{message}"
        c3_str = self.rsa.encrypt(payload_3, r3['pub_key'])

        # COUCHE 2 (Pour R2 -> R3)
        payload_2 = f"{r3['ip']}:{r3['port']}|||{c3_str}"
        c2_str = self.rsa.encrypt(payload_2, r2['pub_key'])

        # COUCHE 1 (Pour R1 -> R2)
        payload_1 = f"{r2['ip']}:{r2['port']}|||{c2_str}"
        c1_str = self.rsa.encrypt(payload_1, r1['pub_key'])

        return r1['ip'], r1['port'], c1_str

    def send_message(self, message, dest_ip, dest_port, specific_path=None):
        try:
            # Étape 1 : Mettre à jour la topologie (sauf si manuel, on suppose que l'user a refresh)
            if not specific_path:
                self.fetch_topology()
            
            # Étape 2 : Créer l'oignon (avec ou sans chemin imposé)
            entry_ip, entry_port, onion = self.create_onion(message, dest_ip, dest_port, specific_path)
            
            # Étape 3 : Envoyer
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((entry_ip, entry_port))
            sock.send(onion.encode('utf-8'))
            sock.close()
            
            return True, f"Envoyé via {entry_ip}:{entry_port}"
        except Exception as e:
            return False, str(e)