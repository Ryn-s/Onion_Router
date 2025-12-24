# 🧅 OnionRouter - SAÉ 3.02 & R3.09

**Auteurs :** Rayan & Arjanit  
**Année :** 2025  
**État du projet :** ✅ Fonctionnel (Testé sur architecture distribuée Linux/Windows)

---

## 📝 Description
OnionRouter est une implémentation éducative du protocole de routage en oignon (type Tor). Il permet l'échange de messages chiffrés et anonymes à travers un réseau de nœuds intermédiaires.

**Points forts techniques :**
* **Cryptographie "Maison" :** Implémentation RSA manuelle (génération de clés, chiffrement modulaire) sans librairie crypto externe.
* **Architecture Distribuée :** Séparation stricte entre Client, Routeurs et Master (Annuaire).
* **Administration :** Interface graphique de supervision pour le Master et scripts d'automatisation.

---

## 🛠️ Installation

### Pré-requis
* Python 3.8 ou supérieur
* Un serveur SQL (MariaDB ou MySQL) pour le Master

### 1. Cloner le projet
```bash
git clone [https://github.com/Ryn-s/Onion_Router.git](https://github.com/Ryn-s/Onion_Router.git)
cd Onion_Router

2. Installer les dépendances
Bash

pip install -r requirements.txt

3. Configuration de la Base de Données (Master uniquement)

    Assurez-vous que MariaDB est lancé (sudo systemctl start mariadb).

    Importez le schéma SQL :

Bash

sudo mariadb < sql/init_db.sql

4. ⚠️ Configuration Réseau (IMPORTANT)

Le fichier de configuration se trouve dans src/common/config.py.

    Pour un test local (1 seule machine) : Laissez MASTER_IP = '127.0.0.1'.

    Pour un test distribué (VMs) : Modifiez MASTER_IP avec l'adresse IP de la machine hébergeant le Master.


🚀 Guide de Lancement

Lancer les composants dans cet ordre précis :
Étape 1 : Le Master (Serveur Annuaire)

Sur la machine serveur :
Bash

# Lance le service Master
python src/master/main.py

# (Optionnel) Lance l'interface graphique de supervision
python src/master/monitor.py

Étape 2 : Les Routeurs (Nœuds)

Sur les machines routeurs :
Bash

# Lancement manuel
python src/router/main.py

# OU via le script d'automatisation (si sous Linux avec xfce4-terminal)
./start_routers.sh

Attendez que les routeurs affichent "Routeur prêt".

C'est la dernière ligne droite ! Pour que le prof n'ait aucun blocage et te mette une bonne note, ton README.md doit être son guide de survie. Il doit pouvoir installer et lancer le projet les yeux fermés.

Voici le contenu exact pour ton README.md et ensuite la procédure pour le fichier de logs.
1. Le Fichier README.md (Copie-colle ça)

Remplace tout le contenu de ton fichier README.md actuel par ceci. C'est clair, pro, et ça prévient les erreurs de configuration IP.
Markdown

# 🧅 OnionRouter - SAÉ 3.02 & R3.09

**Auteurs :** Rayan & Arjanit  
**Année :** 2024-2025  
**État du projet :** ✅ Fonctionnel (Testé sur architecture distribuée Linux/Windows)

---

## 📝 Description
OnionRouter est une implémentation éducative du protocole de routage en oignon (type Tor). Il permet l'échange de messages chiffrés et anonymes à travers un réseau de nœuds intermédiaires.

**Points forts techniques :**
* **Cryptographie "Maison" :** Implémentation RSA manuelle (génération de clés, chiffrement modulaire) sans librairie crypto externe.
* **Architecture Distribuée :** Séparation stricte entre Client, Routeurs et Master (Annuaire).
* **Administration :** Interface graphique de supervision pour le Master et scripts d'automatisation.

---

## 🛠️ Installation

### Pré-requis
* Python 3.8 ou supérieur
* Un serveur SQL (MariaDB ou MySQL) pour le Master

### 1. Cloner le projet
```bash
git clone [https://github.com/Ryn-s/Onion_Router.git](https://github.com/Ryn-s/Onion_Router.git)
cd Onion_Router

2. Installer les dépendances
Bash

pip install -r requirements.txt

3. Configuration de la Base de Données (Master uniquement)

    Assurez-vous que MariaDB est lancé (sudo systemctl start mariadb).

    Importez le schéma SQL :

Bash

sudo mariadb < sql/init_db.sql

4. ⚠️ Configuration Réseau (IMPORTANT)

Le fichier de configuration se trouve dans src/common/config.py.

    Pour un test local (1 seule machine) : Laissez MASTER_IP = '127.0.0.1'.

    Pour un test distribué (VMs) : Modifiez MASTER_IP avec l'adresse IP de la machine hébergeant le Master.

🚀 Guide de Lancement

Lancer les composants dans cet ordre précis :
Étape 1 : Le Master (Serveur Annuaire)

Sur la machine serveur :
Bash

# Lance le service Master
python src/master/main.py

# (Optionnel) Lance l'interface graphique de supervision
python src/master/monitor.py

Étape 2 : Les Routeurs (Nœuds)

Sur les machines routeurs :
Bash

# Lancement manuel
python src/router/main.py

# OU via le script d'automatisation (si sous Linux avec xfce4-terminal)
./start_routers.sh

Attendez que les routeurs affichent "Routeur prêt".
Étape 3 : Le Serveur de Réception (Destinataire)
Bash

python tests/dummy_server.py

C'est la dernière ligne droite ! Pour que le prof n'ait aucun blocage et te mette une bonne note, ton README.md doit être son guide de survie. Il doit pouvoir installer et lancer le projet les yeux fermés.

Voici le contenu exact pour ton README.md et ensuite la procédure pour le fichier de logs.
1. Le Fichier README.md (Copie-colle ça)

Remplace tout le contenu de ton fichier README.md actuel par ceci. C'est clair, pro, et ça prévient les erreurs de configuration IP.
Markdown

# 🧅 OnionRouter - SAÉ 3.02 & R3.09

**Auteurs :** Rayan & Arjanit  
**Année :** 2024-2025  
**État du projet :** ✅ Fonctionnel (Testé sur architecture distribuée Linux/Windows)

---

## 📝 Description
OnionRouter est une implémentation éducative du protocole de routage en oignon (type Tor). Il permet l'échange de messages chiffrés et anonymes à travers un réseau de nœuds intermédiaires.

**Points forts techniques :**
* **Cryptographie "Maison" :** Implémentation RSA manuelle (génération de clés, chiffrement modulaire) sans librairie crypto externe.
* **Architecture Distribuée :** Séparation stricte entre Client, Routeurs et Master (Annuaire).
* **Administration :** Interface graphique de supervision pour le Master et scripts d'automatisation.

---

## 🛠️ Installation

### Pré-requis
* Python 3.8 ou supérieur
* Un serveur SQL (MariaDB ou MySQL) pour le Master

### 1. Cloner le projet
```bash
git clone [https://github.com/Ryn-s/Onion_Router.git](https://github.com/Ryn-s/Onion_Router.git)
cd Onion_Router

2. Installer les dépendances
Bash

pip install -r requirements.txt

3. Configuration de la Base de Données (Master uniquement)

    Assurez-vous que MariaDB est lancé (sudo systemctl start mariadb).

    Importez le schéma SQL :

Bash

sudo mariadb < sql/init_db.sql

4. ⚠️ Configuration Réseau (IMPORTANT)

Le fichier de configuration se trouve dans src/common/config.py.

    Pour un test local (1 seule machine) : Laissez MASTER_IP = '127.0.0.1'.

    Pour un test distribué (VMs) : Modifiez MASTER_IP avec l'adresse IP de la machine hébergeant le Master.

🚀 Guide de Lancement

Lancer les composants dans cet ordre précis :
Étape 1 : Le Master (Serveur Annuaire)

Sur la machine serveur :
Bash

# Lance le service Master
python src/master/main.py

# (Optionnel) Lance l'interface graphique de supervision
python src/master/monitor.py

Étape 2 : Les Routeurs (Nœuds)

Sur les machines routeurs :
Bash

# Lancement manuel
python src/router/main.py

# OU via le script d'automatisation (si sous Linux avec xfce4-terminal)
./start_routers.sh

Attendez que les routeurs affichent "Routeur prêt".
Étape 3 : Le Serveur de Réception (Destinataire)
Bash

python tests/dummy_server.py

Étape 4 : Le Client

Sur la machine utilisateur :
Bash

python src/client/gui.py

    Cliquez sur Actualiser pour récupérer la liste des routeurs.

    Écrivez votre message et cliquez sur Envoyer.

📂 Organisation du Code

    src/common/ : Cryptographie RSA et protocole réseau.

    src/master/ : Gestion de la BDD et interface de monitoring.

    src/router/ : Logique de transfert et de désinscription automatique.

    src/client/ : Interface utilisateur PyQt5.