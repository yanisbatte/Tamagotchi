
# Tamagotchi - Python CLI

Un petit jeu console type **Tamagotchi** pour le BTS SIO SLAM (POO, persistance JSON, menu CLI).

## 🚀 Lancer
```bash
cd tamagotchi_python_cli
python3 main.py
```
*(Aucune dépendance externe requise - Python 3.10+)*

## 🎮 Règles
- Les stats vont de 0 à 100.
- À chaque tour, le temps passe et les stats évoluent.
- Si une stat tombe à 0, le Tamagotchi meurt.
- Sauvegarde auto dans `save.json` à chaque action.

## 📚 Compétences visées
- POO (classe `Tamagotchi`), gestion d'état
- Entrées/sorties fichiers (JSON)
- Menus et contrôles d'entrées utilisateurs
- (Optionnel) Tests unitaires basiques

## 📁 Structure
```
tamagotchi_python_cli/
  ├─ main.py
  ├─ models.py
  ├─ storage.py
  ├─ save.json        # créé automatiquement
  └─ README.md
```

## ✅ Idées d'améliorations
- Plusieurs Tamagotchi
- Événements aléatoires (maladie, bonus)
- Mode difficile (dégradation + rapide)
- Interface graphique (Tkinter) ou Web (Flask)
