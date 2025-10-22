
"""Modèle représentant l'état et les actions d'un Tamagotchi."""

from dataclasses import dataclass, asdict
import random

BOUND_MIN = 0
BOUND_MAX = 100

def clamp(v: int) -> int:
    """Ramène la valeur fournie dans l'intervalle [BOUND_MIN, BOUND_MAX]."""
    return max(BOUND_MIN, min(BOUND_MAX, v))

@dataclass
class Tamagotchi:
    """Entité principale stockant les statistiques et comportements."""
    nom: str
    faim: int = 50
    energie: int = 70
    humeur: int = 60
    hygiene: int = 60
    age: int = 0
    vivant: bool = True

    def _degrade(self) -> None:
        """Applique la dégradation naturelle après chaque action."""
        self.faim = clamp(self.faim - 6)
        self.energie = clamp(self.energie - 5)
        self.humeur = clamp(self.humeur - 4)
        self.hygiene = clamp(self.hygiene - 3)
        self.age += 1
        self._check_vie()

    def _check_vie(self) -> None:
        """Déclare le Tamagotchi mort si l'une des statistiques est à zéro."""
        if any([self.faim == 0, self.energie == 0, self.humeur == 0, self.hygiene == 0]):
            self.vivant = False

    # Actions
    def nourrir(self) -> str:
        """Réduit la faim au prix d'une légère baisse de l'humeur."""
        self.faim = clamp(self.faim + 30)
        self.humeur = clamp(self.humeur - 5)
        self._random_event()
        self._degrade()
        return "🍖 Tu as nourri {0}.".format(self.nom)

    def jouer(self) -> str:
        """Améliore l'humeur mais consomme énergie et nourriture."""
        self.humeur = clamp(self.humeur + 20)
        self.energie = clamp(self.energie - 10)
        self.faim = clamp(self.faim - 10)
        self._random_event()
        self._degrade()
        return "🎲 Vous jouez avec {0}.".format(self.nom)

    def dormir(self) -> str:
        """Recharge l'énergie tout en laissant un peu baisser la faim."""
        self.energie = clamp(BOUND_MAX)
        self.faim = clamp(self.faim - 10)
        self._random_event()
        self._degrade()
        return "😴 {0} a bien dormi.".format(self.nom)

    def laver(self) -> str:
        """Augmente l'hygiène et apporte un léger bonus de bonne humeur."""
        self.hygiene = clamp(self.hygiene + 35)
        self.humeur = clamp(self.humeur + 5)
        self._random_event()
        self._degrade()
        return "🛁 {0} est tout propre.".format(self.nom)

    def passer(self) -> str:
        """Laisse passer un tour en ne déclenchant qu'occasionnellement un événement."""
        self._random_event(force=False)
        self._degrade()
        return "⏭️ Le temps passe..."

    def _random_event(self, force: bool = True) -> None:
        """Déclenche aléatoirement un bonus ou malus sur les statistiques."""
        # 20% de chances lorsqu'on passe un tour, toujours sinon
        if not force and random.random() > 0.2:
            return
        r = random.random()
        if r < 0.1:
            # Petit bonus
            self.humeur = clamp(self.humeur + 10)
        elif r < 0.2:
            # Petit malus
            self.hygiene = clamp(self.hygiene - 10)
        elif r < 0.25:
            # Événement rare
            self.energie = clamp(self.energie - 15)

    def as_dict(self) -> dict:
        """Expose les attributs sous forme de dictionnaire sérialisable."""
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Tamagotchi":
        """Reconstruit un Tamagotchi depuis un dictionnaire de données."""
        return Tamagotchi(**d)
