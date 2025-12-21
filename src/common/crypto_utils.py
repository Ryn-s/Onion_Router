import random
import sympy
import math

"""
MODULE DE CRYPTOGRAPHIE - PROJET ONION ROUTER (VERSION CORRIGÉE - BLOCKS)
Auteur : Rayan
Description : Implémentation RSA avec support des messages longs (découpage par blocs).
"""

class RSACipher:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        # Taille max d'un bloc en octets (Key_bits / 8). 
        # On enlève une marge de sécurité (ex: 10 octets) pour éviter les erreurs de limite mathématique.
        self.block_size = (self.key_size // 8) - 10 

    def generate_keys(self):
        # 1. Choix de p et q
        p = sympy.randprime(2**(self.key_size//2 - 1), 2**(self.key_size//2))
        q = sympy.randprime(2**(self.key_size//2 - 1), 2**(self.key_size//2))
        while p == q:
            q = sympy.randprime(2**(self.key_size//2 - 1), 2**(self.key_size//2))

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        if math.gcd(e, phi) != 1:
            e = sympy.randprime(3, phi - 1)

        d = pow(e, -1, phi)
        self.public_key = (e, n)
        self.private_key = (d, n)
        return self.public_key, self.private_key

    def encrypt(self, message_str, pub_key):
        """
        Chiffre un message de n'importe quelle taille en le découpant en blocs.
        Retourne une chaîne de nombres séparés par des '/'
        """
        e, n = pub_key
        message_bytes = message_str.encode('utf-8')
        
        encrypted_blocks = []
        
        # On découpe le message en morceaux de taille self.block_size
        for i in range(0, len(message_bytes), self.block_size):
            chunk = message_bytes[i : i + self.block_size]
            m_int = int.from_bytes(chunk, byteorder='big')
            
            # Chiffrement du bloc
            c_int = pow(m_int, e, n)
            encrypted_blocks.append(str(c_int))
            
        # On joint les blocs chiffrés avec un séparateur unique '/'
        return "/".join(encrypted_blocks)

    def decrypt(self, encrypted_str):
        """
        Déchiffre une chaîne contenant plusieurs blocs séparés par '/'
        """
        if not self.private_key:
            raise Exception("Pas de clé privée chargée !")
            
        d, n = self.private_key
        decrypted_bytes = b""
        
        # On sépare les blocs
        blocks = encrypted_str.split('/')
        
        for block_str in blocks:
            if not block_str: continue # Ignorer vide
            try:
                c_int = int(block_str)
                m_int = pow(c_int, d, n)
                
                # Conversion int -> bytes
                # On calcule la taille nécessaire
                byte_len = (m_int.bit_length() + 7) // 8
                chunk = m_int.to_bytes(byte_len, byteorder='big')
                decrypted_bytes += chunk
            except Exception as e:
                print(f"[Crypto] Erreur bloc: {e}")
        
        return decrypted_bytes.decode('utf-8', errors='ignore')

# Test rapide
if __name__ == "__main__":
    rsa = RSACipher(key_size=1024)
    pub, priv = rsa.generate_keys()
    
    # Test avec un message TRÈS long pour vérifier le découpage
    gros_message = "A" * 300 # 300 octets (plus grand que 128)
    print(f"Test message long ({len(gros_message)} octets)...")
    
    crypted = rsa.encrypt(gros_message, pub)
    print(f"Chiffré (taille): {len(crypted)}")
    
    decrypted = rsa.decrypt(crypted)
    print(f"Déchiffré correct ? {decrypted == gros_message}")