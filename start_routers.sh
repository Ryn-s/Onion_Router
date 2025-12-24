#!/bin/bash
# Script d'automatisation AC23.01
echo "Lancement de l'infrastructure de routage..."

# Lance 3 terminaux (xfce4-terminal pour EndeavourOS/XFCE)
xfce4-terminal --title="Routeur 1" --hold -e "python src/router/main.py" &
sleep 1
xfce4-terminal --title="Routeur 2" --hold -e "python src/router/main.py" &
sleep 1
xfce4-terminal --title="Routeur 3" --hold -e "python src/router/main.py" &

echo "3 Routeurs déployés."