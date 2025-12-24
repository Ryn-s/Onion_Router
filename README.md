# 🧅 OnionRouter - SAÉ 3.02 & R3.09

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Educational-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

**Projet Universitaire - Implémentation d'un protocole de routage en oignon.**

* **Auteurs :** Rayan & Arjanit
* **Année :** 2025
* **Cadre :** Architecture Distribuée & Cryptographie

---

## 📝 Description

**OnionRouter** permet à deux clients de communiquer de manière anonyme à travers un réseau de routeurs virtuels. Le message est encapsulé dans plusieurs couches de chiffrement, qui sont "pelées" une à une par les nœuds intermédiaires.

### ✨ Points Forts Techniques
* **🔐 Cryptographie "Maison" :** Implémentation RSA manuelle (génération de clés, chiffrement modulaire) sans aucune librairie de crypto externe.
* **🌐 Architecture Distribuée :** Séparation stricte entre le **Client** (Windows), les **Routeurs** (Linux) et le **Master** (Base de données).
* **🖥️ Supervision :** Interface graphique d'administration pour visualiser la topologie réseau en temps réel.
* **⚡ Automatisation :** Scripts de déploiement automatique des nœuds.

---

## 🛠️ Installation

### Pré-requis
* **Langage :** Python 3.8 ou supérieur.
* **Base de données :** MariaDB ou MySQL (uniquement pour la machine Master).
* **Système :** Testé sur Linux (Serveur/Routeurs) et Windows (Client).

### 1. Cloner le projet
```bash
git clone https://github.com/Ryn-s/Onion_Router.git
cd Onion_Router
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration de la Base de Données (Master uniquement)
Assurez-vous que le service SQL est lancé, puis importez le schéma :
```bash
sudo systemctl start mariadb
sudo mariadb < sql/init_db.sql
```

### ⚠️ Configuration Réseau (IMPORTANT)
Le fichier de configuration se trouve dans src/common/config.py.

    Modification requise avant lancement :

        Pour un test local (1 PC) : Laissez MASTER_IP = '127.0.0.1'.

        Pour un test distribué (VMs) : Modifiez MASTER_IP avec l'adresse IP réelle de la machine hébergeant le Master (ex: '192.168.1.15').


### 🚀 Guide de Lancement (Ordre Précis)

## Étape 1 : Le Master (Serveur Annuaire)

Sur la VM Linux dédiée au Master :
```bash
# 1. Lance le service principal
python src/master/main.py

# 2. (Optionnel) Ouvre l'interface de supervision graphique
python src/master/monitor.py
```

### Étape 2 : Les Routeurs (Nœuds de transport)

Sur la machine hôte (ou une autre VM) :
```bash
# Option A : Lancement via le script d'automatisation (Linux/XFCE)
./start_routers.sh

# Option B : Lancement manuel (Ouvrir 3 terminaux)
python src/router/main.py
```

### Étape 3 : Le Serveur de Réception

Pour simuler le destinataire final :
```bash
python tests/dummy_server.py
```

### Étape 4 : Le Client (Utilisateur)

Sur la VM Windows (ou autre) :
```bash 
python src/client/gui.py
```

1. Cliquez sur "Actualiser" pour récupérer la liste des routeurs.

2. Saisissez votre message.

3. Cliquez sur "Envoyer".

### 📂 Organisation du Code

| Dossier | Description |
| :--- | :--- |
| `src/common/` | **Cœur du projet :** Crypto RSA manuelle et Protocole réseau. |
| `src/master/` | Gestion de la BDD et Interface Admin ( `monitor.py` ). |
| `src/router/` | Logique de transfert et désinscription automatique. |
| `src/client/` | Interface utilisateur PyQt5. |
| `docs/` | Documentation et schémas. |