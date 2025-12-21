import mysql.connector
from mysql.connector import Error

"""
Gestionnaire de Base de Données (MariaDB)
Permet au Master de stocker les routeurs et les logs.
Auteur : Arjanit
"""

class DBManager:
    def __init__(self):
        self.host = "localhost"
        self.user = "onion_user"
        self.password = "onion_pass"
        self.database = "onion_db"
        self.connection = None

    def connect(self):
        """Établit la connexion à la BDD"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            # print("Connecté à MariaDB")
        except Error as e:
            print(f"[BDD] Erreur de connexion : {e}")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def register_router(self, ip, port, pub_e, pub_n):
        """
        Enregistre ou met à jour un routeur dans la topologie.
        Les clés sont stockées en string pour éviter l'overflow.
        """
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor()
        
        # On vérifie si ce couple IP/Port existe déjà
        check_query = "SELECT id FROM routers WHERE ip_address = %s AND port = %s"
        cursor.execute(check_query, (ip, port))
        result = cursor.fetchone()

        if result:
            # Update (le routeur redémarre)
            query = """UPDATE routers SET pub_key_e=%s, pub_key_n=%s, status='online' 
                       WHERE id=%s"""
            cursor.execute(query, (str(pub_e), str(pub_n), result[0]))
        else:
            # Insert (nouveau routeur)
            query = """INSERT INTO routers (ip_address, port, pub_key_e, pub_key_n, status)
                       VALUES (%s, %s, %s, %s, 'online')"""
            cursor.execute(query, (ip, port, str(pub_e), str(pub_n)))
            
        self.connection.commit()
        cursor.close()
        print(f"[BDD] Routeur enregistré : {ip}:{port}")

    def get_all_active_routers(self):
        """Retourne la liste des routeurs en ligne pour les clients"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT ip_address, port, pub_key_e, pub_key_n FROM routers WHERE status='online'"
        cursor.execute(query)
        routers = cursor.fetchall()
        cursor.close()
        return routers

    def log_event(self, source, event_type, message):
        """Log un événement (AC23.04)"""
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        query = "INSERT INTO logs (source, event_type, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (source, event_type, message))
        self.connection.commit()
        cursor.close()

# Test rapide
if __name__ == "__main__":
    db = DBManager()
    db.connect()
    # Test d'insertion bidon
    db.register_router("127.0.0.1", 8080, "12345", "99999")
    print(db.get_all_active_routers())
    db.close()