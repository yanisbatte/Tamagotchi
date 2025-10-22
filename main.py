
"""Interface en ligne de commande pour gérer un Tamagotchi."""

from models import Tamagotchi
from storage import save_game, load_game

def banner():
    """Affiche le menu principal au démarrage."""
    print("=== Tamagotchi ===")
    print("1. Créer une nouvelle partie")
    print("2. Charger la partie")
    print("3. Quitter")

def menu():
    """Présente les actions disponibles durant une partie."""
    print("\nActions :")
    print("1. Nourrir  2. Jouer  3. Dormir  4. Laver  5. Passer  6. Quitter")

def show(t: Tamagotchi):
    """Affiche l'état courant du Tamagotchi."""
    print(f"\nNom: {t.nom} | Âge: {t.age}")
    print(f"Faim: {t.faim} | Énergie: {t.energie} | Humeur: {t.humeur} | Hygiène: {t.hygiene}")
    print("Statut:", "VIVANT ✅" if t.vivant else "MORT ❌")

def loop(t: Tamagotchi):
    """Boucle principale d'interaction tant que le Tamagotchi est vivant."""
    while t.vivant:
        show(t)
        menu()
        try:
            ch = input("> Votre choix: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSortie...")
            break
        if ch == "1":
            print(t.nourrir())
        elif ch == "2":
            print(t.jouer())
        elif ch == "3":
            print(t.dormir())
        elif ch == "4":
            print(t.laver())
        elif ch == "5":
            print(t.passer())
        elif ch == "6":
            break
        else:
            print("Choix invalide.")
            continue
        save_game(t)
    if not t.vivant:
        show(t)
        print("\n💀 Votre Tamagotchi est mort. Fin de la partie.")
        save_game(t)

def main():
    """Point d'entrée du programme et gestion des choix initiaux."""
    while True:
        banner()
        ch = input("> ").strip()
        if ch == "1":
            nom = input("Nom du Tamagotchi: ").strip() or "Pixel"
            t = Tamagotchi(nom=nom)
            save_game(t)
            loop(t)
        elif ch == "2":
            t = load_game()
            if not t:
                print("Aucune sauvegarde trouvée.")
                continue
            loop(t)
        elif ch == "3":
            print("À bientôt.")
            return
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
