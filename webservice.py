
from flask import Flask, jsonify, request
from models import Tamagotchi
from storage import save_game, load_game

app = Flask(__name__)


def get_current_tamagotchi():
    """Charge la sauvegarde courante ou Non si aucune partie."""
    return load_game()


@app.get("/tamagotchi")
def get_tamagotchi():
    """Retourne l'état courant du Tamagotchi."""
    t = get_current_tamagotchi()
    if t is None:
        return jsonify({"error": "Aucune partie trouvée."}), 404
    return jsonify({"tamagotchi": t.as_dict()})


@app.post("/tamagotchi")
def create_tamagotchi():
    """Crée une nouvelle partie."""
    payload = request.get_json(silent=True) or {}
    nom = payload.get("nom") or payload.get("name") or "Pixel"

    t = Tamagotchi(nom=nom)
    save_game(t)

    return (
        jsonify(
            {
                "message": f"Nouvelle partie créée pour {t.nom}.",
                "tamagotchi": t.as_dict(),
            }
        ),
        201,
    )


@app.post("/tamagotchi/action")
def do_action():
    """Applique une action sur le Tamagotchi (nourrir, jouer, dormir...)."""
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").lower()

    allowed_actions = {
        "nourrir": "nourrir",
        "manger": "nourrir",
        "jouer": "jouer",
        "play": "jouer",
        "dormir": "dormir",
        "sleep": "dormir",
        "laver": "laver",
        "wash": "laver",
        "passer": "passer",
        "wait": "passer",
        "attendre": "passer",
    }

    if action not in allowed_actions:
        return (
            jsonify(
                {
                    "error": "Action invalide.",
                    "actions_autorisees": [
                        "nourrir",
                        "jouer",
                        "dormir",
                        "laver",
                        "passer",
                    ],
                }
            ),
            400,
        )

    t = get_current_tamagotchi()
    if t is None:
        return jsonify({"error": "Aucune partie chargée."}), 404

    # On empêche d'agir sur un Tamagotchi mort
    if not t.vivant:
        return (
            jsonify(
                {
                    "error": "Le Tamagotchi est mort, aucune action possible.",
                    "tamagotchi": t.as_dict(),
                }
            ),
            410,
        )

    # Appel dynamique de la bonne méthode
    method_name = allowed_actions[action]
    method = getattr(t, method_name)
    message = method()
    save_game(t)

    return jsonify(
        {
            "message": message,
            "tamagotchi": t.as_dict(),
            "vivant": t.vivant,
        }
    )


@app.delete("/tamagotchi")
def reset_tamagotchi():
    """Supprime la sauvegarde courante (reset de la partie)."""
    t = get_current_tamagotchi()
    # On supprime simplement le fichier de sauvegarde si nécessaire
    import os
    from storage import SAVE_FILE

    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)

    return jsonify({"message": "Partie réinitialisée."}), 200


if __name__ == "__main__":
    # debug=True pratique en dev, à désactiver en prod
    app.run(host="0.0.0.0", port=5000, debug=True)
