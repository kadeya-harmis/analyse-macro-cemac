"""
Étape 2 — Analyse exploratoire.

Nettoie les données brutes, produit les statistiques descriptives et
enregistre quatre figures dans figures/.

Usage :
    python src/02_analyse.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from theme import (
    CATEGORIELLE,
    DIVERGENTE,
    SEQUENTIELLE,
    TEXTE_SECONDAIRE,
    appliquer_theme,
)

RACINE = Path(__file__).resolve().parents[1]
FICHIER_BRUT = RACINE / "data" / "raw" / "wdi_cemac.csv"
DOSSIER_PROPRE = RACINE / "data" / "processed"
DOSSIER_FIGURES = RACINE / "figures"

ETIQUETTES = {
    "croissance_pib": "Croissance du PIB (%)",
    "inflation": "Inflation (%)",
    "pib_par_habitant": "PIB par habitant (USD)",
    "ide_entrants": "IDE entrants (% du PIB)",
    "exportations": "Exportations (% du PIB)",
    "rentes_ressources": "Rentes des ressources naturelles (% du PIB)",
}


# --- Préparation -----------------------------------------------------------

def charger() -> pd.DataFrame:
    """Charge les données brutes et les met au format large (une colonne par indicateur)."""
    brut = pd.read_csv(FICHIER_BRUT)
    large = (
        brut.pivot_table(
            index=["pays", "annee"], columns="indicateur", values="valeur"
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    return large.sort_values(["pays", "annee"])


def resumer(donnees: pd.DataFrame) -> pd.DataFrame:
    """Statistiques descriptives par indicateur : couverture, centre, dispersion."""
    colonnes = [c for c in ETIQUETTES if c in donnees.columns]
    resume = donnees[colonnes].describe().T
    resume["taux_manquant"] = donnees[colonnes].isna().mean()
    return resume.round(2)


# --- Figures ---------------------------------------------------------------

def figure_evolution(donnees: pd.DataFrame) -> None:
    """Évolution temporelle : une ligne par pays, légende obligatoire."""
    fig, ax = plt.subplots()
    pays_tries = sorted(donnees["pays"].unique())

    for i, pays in enumerate(pays_tries):
        sous_ensemble = donnees[donnees["pays"] == pays]
        ax.plot(
            sous_ensemble["annee"],
            sous_ensemble["croissance_pib"],
            color=CATEGORIELLE[i % len(CATEGORIELLE)],
            label=pays,
        )

    ax.axhline(0, color=TEXTE_SECONDAIRE, linewidth=0.8, zorder=1)
    ax.set_title("Croissance du PIB dans la CEMAC")
    ax.set_xlabel("Année")
    ax.set_ylabel("Croissance annuelle (%)")
    ax.legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.28))
    fig.savefig(DOSSIER_FIGURES / "01_croissance_pib.png")
    plt.close(fig)


def figure_comparaison(donnees: pd.DataFrame, indicateur: str = "inflation") -> None:
    """Comparaison entre pays : série unique, donc pas de légende mais des valeurs affichées."""
    moyennes = (
        donnees.groupby("pays")[indicateur].mean().sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    barres = ax.barh(
        moyennes.index, moyennes.values, color=CATEGORIELLE[0], height=0.62
    )
    ax.bar_label(
        barres, fmt="%.1f", padding=4, color=TEXTE_SECONDAIRE, fontsize=9
    )

    ax.set_title(f"{ETIQUETTES[indicateur]} — moyenne sur la période")
    ax.set_xlabel(ETIQUETTES[indicateur])
    ax.grid(axis="y", visible=False)
    ax.margins(x=0.12)
    fig.savefig(DOSSIER_FIGURES / "02_comparaison_pays.png")
    plt.close(fig)


def figure_correlations(donnees: pd.DataFrame) -> None:
    """Corrélations : grandeur signée, donc rampe divergente centrée sur zéro."""
    colonnes = [c for c in ETIQUETTES if c in donnees.columns]
    matrice = donnees[colonnes].corr()
    noms = [ETIQUETTES[c].split(" (")[0] for c in colonnes]

    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    image = ax.imshow(matrice, cmap=DIVERGENTE, vmin=-1, vmax=1)

    ax.set_xticks(range(len(noms)), noms, rotation=40, ha="right")
    ax.set_yticks(range(len(noms)), noms)
    ax.grid(visible=False)

    for i in range(len(noms)):
        for j in range(len(noms)):
            valeur = matrice.iloc[i, j]
            ax.text(
                j, i, f"{valeur:.2f}",
                ha="center", va="center", fontsize=8,
                color="#ffffff" if abs(valeur) > 0.55 else TEXTE_SECONDAIRE,
            )

    ax.set_title("Corrélations entre indicateurs")
    barre = fig.colorbar(image, ax=ax, shrink=0.75)
    barre.outline.set_visible(False)
    fig.savefig(DOSSIER_FIGURES / "03_correlations.png")
    plt.close(fig)


def figure_distribution(donnees: pd.DataFrame) -> None:
    """Distribution d'une variable clé : forme, dispersion, valeurs extrêmes."""
    valeurs = donnees["croissance_pib"].dropna()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(valeurs, bins=24, color=SEQUENTIELLE(0.55), edgecolor="#ffffff")
    ax.axvline(
        valeurs.median(), color="#0b0b0b", linewidth=1.5, linestyle="--",
        label=f"Médiane : {valeurs.median():.1f} %",
    )

    ax.set_title("Distribution de la croissance du PIB")
    ax.set_xlabel("Croissance annuelle (%)")
    ax.set_ylabel("Nombre d'observations")
    ax.grid(axis="x", visible=False)
    ax.legend()
    fig.savefig(DOSSIER_FIGURES / "04_distribution.png")
    plt.close(fig)


# --- Programme principal ---------------------------------------------------

def main() -> None:
    appliquer_theme()
    DOSSIER_FIGURES.mkdir(parents=True, exist_ok=True)
    DOSSIER_PROPRE.mkdir(parents=True, exist_ok=True)

    donnees = charger()
    donnees.to_csv(DOSSIER_PROPRE / "cemac_large.csv", index=False)

    resume = resumer(donnees)
    resume.to_csv(DOSSIER_PROPRE / "statistiques_descriptives.csv")
    print("Statistiques descriptives\n")
    print(resume[["count", "mean", "std", "min", "max", "taux_manquant"]])

    figure_evolution(donnees)
    figure_comparaison(donnees)
    figure_correlations(donnees)
    figure_distribution(donnees)

    print(f"\nQuatre figures enregistrées dans {DOSSIER_FIGURES}")


if __name__ == "__main__":
    main()
