#!/bin/bash

BRIGHT_MAGENTA="\033[38;5;201m"
BRIGHT_BLUE="\033[1;38;5;33m"
BLUE_VIOLET="\033[1;38;5;99m"
NC="\033[0m"

SCRIPT="..."

if [ "$SUDO_USER" ]; then
  USER_TO_RUN="$SUDO_USER"
else
  USER_TO_RUN="$(whoami)"
fi

echo -e "${BRIGHT_MAGENTA}=== Lancement du script avec sudo et permissions ===${NC}"
echo -e "${BLUE_VIOLET}Utilisateur détecté : $USER_TO_RUN${NC}"

if [ ! -f "$SCRIPT" ]; then
    echo -e "${BRIGHT_BLUE}Erreur : Le script $SCRIPT est introuvable.${NC}"
    exit 1
fi

echo -e "${BLUE_VIOLET}Donner les permissions d'exécution à $SCRIPT...${NC}"
sudo chmod +x "$SCRIPT"
if [ $? -ne 0 ]; then
    echo -e "${BRIGHT_MAGENTA}Erreur : Impossible de changer les permissions.${NC}"
    exit 1
fi

echo -e "${BLUE_VIOLET}Exécution du script avec sudo python3...${NC}"
sudo python3 "$SCRIPT"
if [ $? -ne 0 ]; then
    echo -e "${BRIGHT_MAGENTA}Erreur : L'exécution du script a échoué.${NC}"
    exit 1
fi

echo -e "${BRIGHT_MAGENTA}Script lancé avec succès.${NC}"
