import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QMessageBox, QCheckBox, QComboBox, QGroupBox)
from PyQt5.QtCore import QTimer

from core import ClientCore

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.core = ClientCore()
        
        self.setWindowTitle("OnionRouter - Client Anonyme")
        self.setGeometry(100, 100, 650, 600) # Un peu plus grand pour les options
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # --- Zone Connexion ---
        self.lbl_status = QLabel("Statut: Non connecté au réseau")
        self.lbl_status.setStyleSheet("color: orange")
        layout.addWidget(self.lbl_status)

        self.btn_refresh = QPushButton("Actualiser la liste des routeurs (Master)")
        self.btn_refresh.clicked.connect(self.refresh_topology)
        layout.addWidget(self.btn_refresh)

        # --- Zone Configuration du Chemin (NOUVEAU) ---
        self.group_routing = QGroupBox("Configuration du Chemin")
        layout_routing = QVBoxLayout()
        
        self.chk_manual = QCheckBox("Choisir manuellement les routeurs (Ordre imposé)")
        self.chk_manual.toggled.connect(self.toggle_manual_mode)
        layout_routing.addWidget(self.chk_manual)
        
        # Layout horizontal pour les 3 choix
        h_layout = QHBoxLayout()
        
        # Routeur 1
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("1. Entrée :"))
        self.combo_r1 = QComboBox()
        self.combo_r1.setEnabled(False)
        v1.addWidget(self.combo_r1)
        h_layout.addLayout(v1)

        # Routeur 2
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("2. Relais :"))
        self.combo_r2 = QComboBox()
        self.combo_r2.setEnabled(False)
        v2.addWidget(self.combo_r2)
        h_layout.addLayout(v2)

        # Routeur 3
        v3 = QVBoxLayout()
        v3.addWidget(QLabel("3. Sortie :"))
        self.combo_r3 = QComboBox()
        self.combo_r3.setEnabled(False)
        v3.addWidget(self.combo_r3)
        h_layout.addLayout(v3)
        
        layout_routing.addLayout(h_layout)
        self.group_routing.setLayout(layout_routing)
        layout.addWidget(self.group_routing)

        # --- Zone Message ---
        layout.addWidget(QLabel("Destinataire (IP:Port) :"))
        self.txt_dest = QLineEdit("127.0.0.1:8000") 
        layout.addWidget(self.txt_dest)
        
        layout.addWidget(QLabel("Message :"))
        self.txt_msg = QTextEdit()
        self.txt_msg.setPlaceholderText("Votre message secret ici...")
        self.txt_msg.setMaximumHeight(80)
        layout.addWidget(self.txt_msg)
        
        self.btn_send = QPushButton("ENVOYER")
        self.btn_send.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_send.clicked.connect(self.send_onion)
        layout.addWidget(self.btn_send)
        
        # --- Logs ---
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        layout.addWidget(self.txt_logs)

        central_widget.setLayout(layout)
        QTimer.singleShot(500, self.refresh_topology)

    def log(self, message):
        self.txt_logs.append(f"> {message}")

    def toggle_manual_mode(self):
        """Active ou désactive les menus déroulants"""
        state = self.chk_manual.isChecked()
        self.combo_r1.setEnabled(state)
        self.combo_r2.setEnabled(state)
        self.combo_r3.setEnabled(state)
        if state:
            self.log("Mode Manuel activé : Sélectionnez l'ordre des routeurs.")
        else:
            self.log("Mode Aléatoire activé.")

    def refresh_topology(self):
        self.log("Mise à jour topologie...")
        if self.core.fetch_topology():
            routers = self.core.available_routers
            count = len(routers)
            self.lbl_status.setText(f"Statut: Connecté ({count} nœuds)")
            self.lbl_status.setStyleSheet("color: green")
            
            # Mise à jour des ComboBox
            # On garde la sélection actuelle si possible
            current_r1 = self.combo_r1.currentIndex()
            current_r2 = self.combo_r2.currentIndex()
            current_r3 = self.combo_r3.currentIndex()

            self.combo_r1.clear()
            self.combo_r2.clear()
            self.combo_r3.clear()
            
            for r in routers:
                label = f"Routeur {r['port']} ({r['ip']})"
                self.combo_r1.addItem(label)
                self.combo_r2.addItem(label)
                self.combo_r3.addItem(label)

            # Restauration index (ou 0 par défaut)
            if count > 0:
                self.combo_r1.setCurrentIndex(current_r1 if current_r1 != -1 else 0)
                self.combo_r2.setCurrentIndex(current_r2 if current_r2 != -1 else 0)
                self.combo_r3.setCurrentIndex(current_r3 if current_r3 != -1 else 0)
                
            self.log(f"Liste actualisée : {count} routeurs trouvés.")
        else:
            self.lbl_status.setText("Statut: Erreur Master")
            self.lbl_status.setStyleSheet("color: red")

    def send_onion(self):
        msg = self.txt_msg.toPlainText()
        dest = self.txt_dest.text()
        
        if not msg:
            QMessageBox.warning(self, "Erreur", "Message vide !")
            return

        try:
            dest_ip, dest_port = dest.split(':')
            dest_port = int(dest_port)
        except:
            QMessageBox.warning(self, "Erreur", "Format IP:Port invalide")
            return

        # Gestion du chemin
        manual_path = None
        if self.chk_manual.isChecked():
            # On récupère les index sélectionnés
            idx1 = self.combo_r1.currentIndex()
            idx2 = self.combo_r2.currentIndex()
            idx3 = self.combo_r3.currentIndex()
            
            if idx1 == -1 or idx2 == -1 or idx3 == -1:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner 3 routeurs.")
                return
                
            # On vérifie qu'il y a assez de routeurs
            if len(self.core.available_routers) < 1:
                QMessageBox.warning(self, "Erreur", "Aucun routeur disponible !")
                return

            # On construit la liste des objets routeurs
            r1 = self.core.available_routers[idx1]
            r2 = self.core.available_routers[idx2]
            r3 = self.core.available_routers[idx3]
            
            # (Optionnel) On pourrait empêcher de choisir 3 fois le même, 
            # mais techniquement c'est possible (boucle), donc on laisse.
            manual_path = [r1, r2, r3]
            self.log(f"Envoi MANUEL : {r1['port']} -> {r2['port']} -> {r3['port']}")
        else:
            self.log("Envoi ALÉATOIRE...")

        # Envoi
        success, info = self.core.send_message(msg, dest_ip, dest_port, manual_path)
        
        if success:
            self.log(f"SUCCÈS : {info}")
            self.txt_msg.clear()
            QMessageBox.information(self, "Envoyé", "Message parti !")
        else:
            self.log(f"ERREUR : {info}")
            QMessageBox.critical(self, "Erreur", f"Échec : {info}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientWindow()
    window.show()
    sys.exit(app.exec_())