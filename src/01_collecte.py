"""
Étape 1 — Collecte des données.

Télécharge une sélection d'indicateurs macroéconomiques de la Banque mondiale
(World Development Indicators) pour les six pays de la CEMAC, et enregistre
le résultat brut dans data/raw/wdi_cemac.csv.

Aucune clé d'API n'est nécessaire : l'API de la Banque mondiale est ouverte.

Usage :
    python src/01_collecte.py
"""

from pathlib import Path

import pandas as pd
import requests

# --- Paramètres de la collecte ---------------------------------------------

PAYS = {
    "TCD": "Tchad",
    "CMR": "Cameroun",
    "COG": "Congo",
    "GAB": "Gabon",
    "GNQ": "Guinée équatoriale",
    "CAF": "République centrafricaine",
}

INDICATEURS = {
    "NY.GDP.MKTP.KD.ZG": "croissance_pib",
    "FP.CPI.TOTL.ZG": "inflation",
    "NY.GDP.PCAP.CD": "pib_par_habitant",
    "BX.KLT.DINV.WD.GD.ZS": "ide_entrants",
    "NE.EXP.GNFS.ZS": "exportations",
    "NY.GDP.TOTL.RT.ZS": "rentes_ressources",
}

ANNEE_DEBUT, ANNEE_FIN = 2000, 2024

RACINE = Path(__file__).resolve().parents[1]
FICHIER_SORTIE = RACINE / "data" / "raw" / "wdi_cemac.csv"

URL = "https://api.worldbank.org/v2/country/{pays}/indicator/{indicateur}"


def parser_reponse(charge_utile: list, nom_indicateur: str) -> pd.DataFrame:
    """Transforme la réponse JSON de l'API en tableau propre.

    La réponse a la forme [metadonnees, observations]. Chaque observation
    contient le pays, l'année et la valeur (parfois nulle).
    """
    if not isinstance(charge_utile, list) or len(charge_utile) < 2:
        raise ValueError("Réponse inattendue de l'API Banque mondiale.")

    observations = charge_utile[1] or []
    lignes = [
        {
            "code_pays": obs["countryiso3code"],
            "annee": int(obs["date"]),
            "indicateur": nom_indicateur,
            "valeur": obs["value"],
        }
        for obs in observations
    ]
    return pd.DataFrame(lignes)


def telecharger_indicateur(code: str, nom: str) -> pd.DataFrame:
    """Télécharge un indicateur pour tous les pays retenus."""
    reponse = requests.get(
        URL.format(pays=";".join(PAYS), indicateur=code),
        params={
            "format": "json",
            "per_page": 20000,
            "date": f"{ANNEE_DEBUT}:{ANNEE_FIN}",
        },
        timeout=60,
    )
    reponse.raise_for_status()
    return parser_reponse(reponse.json(), nom)


def main() -> None:
    tableaux = []
    for code, nom in INDICATEURS.items():
        print(f"Téléchargement de {nom} ({code})…")
        tableaux.append(telecharger_indicateur(code, nom))

    donnees = pd.concat(tableaux, ignore_index=True)
    donnees["pays"] = donnees["code_pays"].map(PAYS)
    donnees = donnees.dropna(subset=["pays"])

    FICHIER_SORTIE.parent.mkdir(parents=True, exist_ok=True)
    donnees.to_csv(FICHIER_SORTIE, index=False)

    print(f"\n{len(donnees)} observations enregistrées dans {FICHIER_SORTIE}")
    print(f"Période : {donnees['annee'].min()}–{donnees['annee'].max()}")
    print(f"Valeurs manquantes : {donnees['valeur'].isna().mean():.1%}")


if __name__ == "__main__":
    main()
