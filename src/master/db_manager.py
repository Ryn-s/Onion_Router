import mysql.connector
from mysql.connector import Error

"""
Gestionnaire de Base de Données (MariaDB)
Permet au Master de stocker les routeurs et les logs.
Auteur : Arjanit
"""

import mysql.connector
from mysql.connector import Error

class DBManager:
    def __init__(self):
        self.host = "localhost"
        self.user = "onion_user"
        self.password = "onion_pass"
        self.database = "onion_db"
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"[BDD] Erreur : {e}")

    #  Nettoyage complet ---
    def reset_routers_table(self):
        """Vide la table des routeurs au démarrage pour éviter les fantômes"""
        if not self.connection:
            self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute("TRUNCATE TABLE routers") # Vide tout !
            self.connection.commit()
            cursor.close()
            print("[BDD] Table 'routers' remise à zéro avec succès.")
        except Error as e:
            print(f"[BDD] Erreur reset: {e}")

   
    def remove_router(self, ip, port):
        """Supprime un routeur spécifique quand il se déconnecte"""
        if not self.connection:
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM routers WHERE ip_address = %s AND port = %s"
            cursor.execute(query, (ip, port))
            self.connection.commit()
            cursor.close()
            print(f"[BDD] Routeur supprimé : {ip}:{port}")
        except Error as e:
            print(f"[BDD] Erreur suppression: {e}")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
   
    
    def register_router(self, ip, port, pub_e, pub_n):
        if not self.connection: self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM routers WHERE ip_address = %s AND port = %s", (ip, port))
        if cursor.fetchone():
            cursor.execute("UPDATE routers SET pub_key_e=%s, pub_key_n=%s, status='online' WHERE ip_address=%s AND port=%s", (str(pub_e), str(pub_n), ip, port))
        else:
            cursor.execute("INSERT INTO routers (ip_address, port, pub_key_e, pub_key_n, status) VALUES (%s, %s, %s, %s, 'online')", (ip, port, str(pub_e), str(pub_n)))
        self.connection.commit()
        cursor.close()

    def get_all_active_routers(self):
        if not self.connection: self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT ip_address, port, pub_key_e, pub_key_n FROM routers WHERE status='online'")
        res = cursor.fetchall()
        cursor.close()
        return res

    def log_event(self, source, event_type, message):
        if not self.connection: self.connect()
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO logs (source, event_type, message) VALUES (%s, %s, %s)", (source, event_type, message))
        self.connection.commit()
        cursor.close()