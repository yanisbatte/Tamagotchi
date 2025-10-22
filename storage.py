
"""Fonctions utilitaires pour la persistance des données du Tamagotchi."""

import json, os
from typing import Optional
from models import Tamagotchi

SAVE_FILE = "save.json"

def save_game(t: Tamagotchi) -> None:
    """Sauvegarde l'état courant dans un fichier JSON."""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(t.as_dict(), f, ensure_ascii=False, indent=2)

def load_game() -> Optional[Tamagotchi]:
    """Charge une sauvegarde si disponible, sinon renvoie None."""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Tamagotchi.from_dict(data)
    except Exception:
        # Fichier invalide ou corrompu : la partie ne peut pas être chargée.
        return None
