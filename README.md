# 🧅 OnionRouter - SAÉ 3.02 & R3.09

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Educational-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

**Projet Universitaire - Implémentation d'un protocole de routage en oignon.**

- **Auteurs :** Rayan & Arjanit
- **Groupe :** RayAnit
- **Année :** 2025
- **Cadre :** Architecture Distribuée & Cryptographie

---

## 📝 Description

**OnionRouter** permet à deux clients de communiquer de manière anonyme à travers un réseau de routeurs virtuels. Le message est encapsulé dans plusieurs couches de chiffrement, qui sont pelées une à une par les nœuds intermédiaires.

### 🔧 Points Forts Techniques

- **🔐 Cryptographie "Maison" :** Implémentation RSA manuelle (génération de clés, chiffrement modulaire) sans librairie de crypto externe.
- **🌐 Architecture Distribuée :** Séparation stricte entre **Client** (Windows), **Routeurs** (Linux) et **Master** (base de données).
- **🖥️ Supervision :** Interface graphique d'administration pour visualiser la topologie réseau en temps réel.
- **⚡ Automatisation :** Scripts de déploiement automatique des nœuds (ex. `start_routers.sh`).

---

## 🛠️ Installation & Pré-requis

Cette section détaille l'installation complète du projet.

### 🐧 Préparation du Système (Linux)

Distribution conseillée : Debian/Ubuntu (ou dérivés).
Le script d'automatisation utilise **xfce4-terminal** pour ouvrir plusieurs fenêtres.

#### 1. Installation des dépendances système

```bash
sudo apt update
sudo apt install git python3-pip python3-venv mariadb-server xfce4-terminal -y
```

#### 2. Cloner le projet

```bash
git clone https://github.com/Ryn-s/Onion_Router.git
cd Onion_Router
```

#### 3. Créer et activer l'environnement virtuel

Sous Linux / macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

Sous Windows :

```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### 4. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

Paquets principaux : **PyQt5**, `mysql-connector-python`, `sympy`.

#### 5. Configuration de la Base de Données (Master uniquement)

Assurez-vous que le service MariaDB est lancé, puis importez le schéma :

```bash
sudo systemctl start mariadb
sudo mariadb < sql/init_db.sql
```

---

## 🌐 Configuration Réseau (IMPORTANT)

Le fichier de configuration se trouve dans :

```
src/common/config.py
```

- Pour un test **local** (une seule machine) :

```python
MASTER_IP = "127.0.0.1"
```

- Pour un test **distribué** (VMs / plusieurs machines) :

```python
MASTER_IP = "192.168.1.XX"  # Remplacez par l'IP réelle de la machine master
```

Pour récupérer votre IP locale sous Linux :

```bash
ip a
```

---

## 🚀 Guide de Lancement (Ordre conseillé)

### Étape 1 : Le Master (Serveur Annuaire)

Sur la machine/VM Linux dédiée au Master :

```bash
# Service principal du Master
python src/master/main.py

# (Optionnel) Interface de supervision graphique
python src/master/monitor.py
```

### Étape 2 : Les Routeurs (Nœuds de transport)

Sur la machine hôte ou une autre VM :

```bash
# Option A : Lancement via script d'automatisation (Linux/XFCE)
chmod +x start_routers.sh
./start_routers.sh

# Option B : Lancement manuel (ouvrir plusieurs terminaux)
python src/router/main.py
```

### Étape 3 : Le Serveur de Réception

Pour simuler le destinataire final :

```bash
python tests/dummy_server.py
```

### Étape 4 : Le Client (Utilisateur)

Sur la machine cliente (Windows ou autre) :

```bash
python src/client/gui.py
```

1. Cliquer sur **« Actualiser »** pour récupérer la liste des routeurs.
2. Saisir le message à envoyer.
3. Cliquer sur **« Envoyer »**.

---

## 📂 Organisation du Code

```
src/
  common/
    crypto_utils.py
    protocol.py
    config.py
  master/
    db_manager.py
    monitor.py
    main.py
  router/
    main.py
  client/
    gui.py
    core.py
docs/
sql/
  init_db.sql
start_routers.sh
tests/
  dummy_server.py
requirements.txt
README.md
```

| Dossier            | Description                                                                       |
|--------------------|-----------------------------------------------------------------------------------|
| `src/common/`      | Cœur du projet : cryptographie RSA manuelle et protocole réseau.                 |
| `src/master/`      | Gestion de la base de données et interface d'admin (`monitor.py`).               |
| `src/router/`      | Logique de routage, inscription/désinscription des nœuds.                        |
| `src/client/`      | Interface utilisateur PyQt5 et logique client.                                   |
| `docs/`            | Documentation, notes techniques et schémas.                                      |
| `sql/`             | Scripts SQL d'initialisation (`init_db.sql`).                                    |
| `tests/`           | Tests et serveur dummy pour simulation.                                          |
| `start_routers.sh` | Script de lancement automatique des routeurs.                                    |

---

## 🔐 Sécurité & Cryptographie

### Protocole Onion

Le protocole Onion est basé sur le chiffrement par couches :

1. **Client** chiffre le message avec la clé publique du **dernier routeur**.
2. Chaque **routeur intermédiaire** ajoute une couche de chiffrement.
3. Les routeurs déchiffrent progressivement jusqu'à atteindre le **serveur final**.
4. Le **serveur dummy** reçoit et traite le message en clair.

### Implémentation RSA

L'implémentation RSA manuelle comprend :

- **Génération de clés** : p, q, e, d
- **Chiffrement modulaire** : c ≡ m^e (mod n)
- **Déchiffrement modulaire** : m ≡ c^d (mod n)
- **Gestion des padding** et formatage des messages

**Aucune dépendance externe** pour la cryptographie (pas de `cryptography`, `PyCryptodome`, etc.).

---

## 💾 Base de Données

### Tables principales

La base de données MariaDB contient :

- **routers** : Enregistrement des nœuds actifs (IP, port, statut)
- **logs** : Historique des messages routés et timestamps

### Initialisation

Le fichier `sql/init_db.sql` crée automatiquement :

```sql
CREATE TABLE routers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ip VARCHAR(15) NOT NULL,
  port INT NOT NULL,
  status ENUM('active', 'inactive') DEFAULT 'active',
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  router_id INT,
  message_hash VARCHAR(64),
  action VARCHAR(50),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (router_id) REFERENCES routers(id)
);
```

---

## 🖥️ Interface Graphique (PyQt5)

### Client GUI (`src/client/gui.py`)

- Liste déroulante des **routeurs disponibles**
- Champ de **saisie de message**
- Bouton **Actualiser** pour récupérer l'état du réseau
- Bouton **Envoyer** pour initier la transmission
- **Zone de logs** affichant l'historique

### Monitoring (`src/master/monitor.py`)

- Visualisation de la **topologie réseau**
- État des routeurs (actif/inactif)
- **Graphique temps réel** des messages routés
- **Tableau des logs** avec timestamps

---

## 📋 Fichiers Importants

### `requirements.txt`

```
PyQt5==5.15.9
mysql-connector-python==8.0.33
sympy==1.12
```

### `src/common/config.py`

Configuration centrale du projet incluant :

- `MASTER_IP` : IP du serveur master
- `MASTER_PORT` : Port du master (ex. 5000)
- `DB_CONFIG` : Identifiants MariaDB
- `RSA_KEY_SIZE` : Taille des clés RSA (ex. 1024 bits)
- `PACKET_SIZE` : Taille des paquets réseau

### `start_routers.sh`

Script Bash pour lancer automatiquement 3 routeurs dans des terminaux XFCE séparés.

---

## 🧪 Tests & Débogage

### Serveur Dummy

```bash
python tests/dummy_server.py
```

Simule un serveur qui :
- Écoute les connexions entrantes
- Affiche les messages reçus (en clair)
- Confirme la réception

### Logs et Monitoring

- **Logs locaux** : `src/master/logs/`
- **Base de données** : Consultez les tables via `mariadb` ou un GUI comme `DBeaver`
- **Interface monitor** : Graphiques en temps réel avec PyQt5

---

## 🐛 Troubleshooting

### Problème : Connexion au Master refusée

**Solution** : Vérifiez que `MASTER_IP` correspond à l'IP réelle du serveur master.

```bash
# Sur la machine master
ip a

# Copiez l'IP eth0 ou enp0s3
# Modifiez src/common/config.py
```

### Problème : Port déjà utilisé

```bash
# Trouvez le processus
lsof -i :5000

# Tuez-le
kill -9 <PID>
```

### Problème : MariaDB ne démarre pas

```bash
sudo systemctl restart mariadb
sudo systemctl status mariadb
```

### Problème : PyQt5 ne s'affiche pas

Si vous lancez depuis SSH, exportez l'affichage :

```bash
export DISPLAY=:0
python src/client/gui.py
```

---

## 📚 Documentation Supplémentaire

- **Architecture** : `docs/architecture.md`
- **Protocole Onion** : `docs/protocol.md`
- **Schémas réseau** : `docs/schemas/`
- **Notes techniques** : `docs/notes.md`

---

## 🤝 Contribution

Ce projet est **éducatif**. Les modifications et améliorations sont bienvenues pour les travaux de recherche ou d'enseignement.

---

## 📜 Licence

Projet à but **éducatif** dans le cadre d'une SAÉ d'architecture distribuée et cryptographie.

Année académique : 2025

---

**Dernière mise à jour :** 31/12/2025
