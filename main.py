"""Interface en ligne de commande pour gérer un Tamagotchi."""

from models import Tamagotchi
from storage import save_game, load_game

def banner():
    """Affiche le menu principal au démarrage."""
    # Le titre est mis à jour pour être plus générique
    print("=== Mon Animal Virtuel ===")
    print("1. Créer une nouvelle partie")
    print("2. Charger la partie")
    print("3. Quitter")

def menu(espece: str):
    """Présente les actions disponibles durant une partie."""
    # Affiche l'espèce stockée
    print(f"\nActions pour ton {espece.capitalize()} :")
    print("1. Nourrir  ")
    print("2. Jouer  ")
    print("3. Dormir  ")
    print("4. Laver  ")
    print("5. Passer  ")
    print("6. Quitter")

def show(t: Tamagotchi):
    """Affiche l'état courant du Tamagotchi."""
    # Utilise t.espece pour l'affichage
    print(f"\nEspèce: {t.espece.capitalize()} | Nom: {t.nom} | Âge: {t.age}")
    print(f"Faim: {t.faim} ")
    print(f"Énergie: {t.energie} ")
    print(f"Humeur: {t.humeur} ")
    print(f"Hygiène: {t.hygiene}")
    print("Statut:", "VIVANT !! ✅" if t.vivant else "MORT ❌")

def loop(t: Tamagotchi):
    """Boucle principale d'interaction tant que le Tamagotchi est vivant."""
    while t.vivant:
        show(t)
        # Passe l'espèce au menu
        menu(t.espece)
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
        # Utilise t.espece dans le message de mort
        print(f"\n💀 Ton {t.espece} est mort. Fin de la partie.")
        save_game(t)

def get_pet_choice() -> str:
    """Demande à l'utilisateur de choisir entre chat et chien."""
    while True:
        print("\nChoisissez votre animal :")
        print("1. Chat")
        print("2. Chien")
        choice = input("> Votre choix: ").strip()
        if choice == "1":
            return "chat"
        elif choice == "2":
            return "chien"
        else:
            print("Choix invalide. Veuillez choisir 1 ou 2.")

def main():
    """Point d'entrée du programme et gestion des choix initiaux."""
    while True:
        banner()
        ch = input("> ").strip()
        if ch == "1":
            # 1. Demander le choix de l'espèce
            espece = get_pet_choice()
            # 2. Demander le nom
            nom = input(f"Nom de votre {espece}: ").strip() or "Pixel"
            # 3. Créer le Tamagotchi avec l'espèce
            t = Tamagotchi(nom=nom, espece=espece)
            save_game(t)
            loop(t)
        elif ch == "2":
            t = load_game()
            if not t:
                print("Aucune sauvegarde trouvée.")
                continue
            # Les anciennes sauvegardes auront "Tamagotchi" comme espèce par défaut.
            loop(t)
        elif ch == "3":
            print("À bientôt.")
            return
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()