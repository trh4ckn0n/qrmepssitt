#!/bin/bash

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
NC="\033[0m"

SCRIPT="..."  
if [ "$SUDO_USER" ]; then
  USER_TO_RUN="$SUDO_USER"
else
  USER_TO_RUN="$(whoami)"
fi

echo -e "${GREEN}=== Lancement du script avec sudo et permissions ===${NC}"
echo -e "${YELLOW}Utilisateur détecté : $USER_TO_RUN${NC}"

if [ ! -f "$SCRIPT" ]; then
    echo -e "${RED}Erreur : Le script $SCRIPT est introuvable.${NC}"
    exit 1
fi

echo -e "${YELLOW}Donner les permissions d'exécution à $SCRIPT...${NC}"
sudo chmod +x "$SCRIPT"
if [ $? -ne 0 ]; then
    echo -e "${RED}Erreur : Impossible de changer les permissions.${NC}"
    exit 1
fi

echo -e "${YELLOW}Exécution du script avec sudo python3...${NC}"
sudo python3 "$SCRIPT"
if [ $? -ne 0 ]; then
    echo -e "${RED}Erreur : L'exécution du script a échoué.${NC}"
    exit 1
fi

echo -e "${GREEN}Script lancé avec succès.${NC}"
