"""
Thème graphique du projet.

Centraliser les couleurs et le style ici garantit que toutes les figures
du dépôt forment un ensemble cohérent, et permet de changer la charte
en un seul endroit.

Palette validée pour la lisibilité, y compris en cas de daltonisme :
les teintes sont attribuées dans un ordre fixe, jamais recyclé.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- Palette catégorielle (identité : une teinte par pays) -----------------
# L'ordre est volontaire : il maximise l'écart perceptif entre teintes voisines.
CATEGORIELLE = [
    "#2a78d6",  # bleu
    "#eb6834",  # orange
    "#1baf7a",  # aqua
    "#eda100",  # jaune
    "#e87ba4",  # magenta
    "#008300",  # vert
]

# --- Encre (textes, axes, grille) ------------------------------------------
TEXTE_PRINCIPAL = "#0b0b0b"
TEXTE_SECONDAIRE = "#52514e"
GRILLE = "#e5e4e0"
SURFACE = "#ffffff"

# --- Rampe séquentielle (magnitude : une seule teinte, clair -> foncé) -----
SEQUENTIELLE = LinearSegmentedColormap.from_list(
    "bleu_sequentiel", ["#cde2fb", "#3987e5", "#104281"]
)

# --- Rampe divergente (polarité : deux pôles + gris neutre au centre) -----
# Réservée aux grandeurs signées, comme les corrélations.
DIVERGENTE = LinearSegmentedColormap.from_list(
    "bleu_gris_rouge", ["#2a78d6", "#f0efec", "#d03b3b"]
)


def appliquer_theme() -> None:
    """Applique le style du projet à toutes les figures matplotlib."""
    plt.rcParams.update(
        {
            "figure.figsize": (9, 5),
            "figure.dpi": 130,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "axes.edgecolor": GRILLE,
            "axes.labelcolor": TEXTE_SECONDAIRE,
            "axes.titlecolor": TEXTE_PRINCIPAL,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 14,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRILLE,
            "grid.linewidth": 0.8,
            "xtick.color": TEXTE_SECONDAIRE,
            "ytick.color": TEXTE_SECONDAIRE,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.frameon": False,
            "legend.fontsize": 9,
            "lines.linewidth": 2,
            "lines.solid_capstyle": "round",
            "font.size": 10,
            "savefig.bbox": "tight",
            "savefig.facecolor": SURFACE,
        }
    )
