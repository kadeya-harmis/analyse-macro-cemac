# Analyse exploratoire des économies de la CEMAC

Analyse exploratoire de six indicateurs macroéconomiques pour les six pays de la
Communauté économique et monétaire de l'Afrique centrale (CEMAC), sur la période
2000-2024, à partir des données ouvertes de la Banque mondiale.

**Question de départ :** dans une zone monétaire commune largement dépendante des
ressources naturelles, la croissance et l'inflation suivent-elles des trajectoires
comparables d'un pays à l'autre, ou les divergences nationales dominent-elles ?

## Données

| | |
| --- | --- |
| **Source** | Banque mondiale — World Development Indicators (API ouverte, sans clé) |
| **Pays** | Cameroun, Congo, Gabon, Guinée équatoriale, République centrafricaine, Tchad |
| **Période** | 2000-2024 |
| **Indicateurs** | croissance du PIB, inflation, PIB par habitant, IDE entrants, exportations (% du PIB), rentes des ressources naturelles (% du PIB) |

Les données brutes ne sont pas versionnées : le script de collecte les retélécharge
à l'identique depuis la source, ce qui garantit la reproductibilité sans alourdir
le dépôt.

## Méthode

1. **Collecte** — interrogation de l'API de la Banque mondiale, un appel par indicateur, et enregistrement du résultat brut sans transformation.
2. **Mise en forme** — passage au format large (une ligne par pays et par année, une colonne par indicateur).
3. **Description** — couverture, valeurs manquantes, centre et dispersion de chaque indicateur.
4. **Exploration** — évolutions temporelles, comparaison entre pays, corrélations entre indicateurs, distribution de la variable centrale.

Le choix des représentations suit une règle simple : les teintes distinguent des
pays (identité), une rampe divergente centrée sur zéro sert aux corrélations
(polarité), une rampe d'une seule teinte sert aux magnitudes.

## Structure du dépôt

```
.
├── src/
│   ├── theme.py         # palette et style commun à toutes les figures
│   ├── 01_collecte.py   # téléchargement des données brutes
│   └── 02_analyse.py    # nettoyage, statistiques descriptives, figures
├── data/
│   ├── raw/             # données brutes (non versionnées)
│   └── processed/       # données mises en forme et tableaux de résultats
├── figures/             # figures produites par l'analyse
└── requirements.txt
```

## Reproduire l'analyse

```bash
git clone https://github.com/Kadeya-harmis/analyse-macro-cemac.git
cd analyse-macro-cemac

python -m venv .venv
source .venv/bin/activate        # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt

python src/01_collecte.py        # télécharge les données
python src/02_analyse.py         # produit les statistiques et les figures
```

## Résultats

<!--
À compléter après le premier passage de l'analyse. Pour chaque figure :
l'insérer, puis écrire deux ou trois phrases sur ce qu'elle montre.
Un lecteur doit comprendre vos conclusions sans lire le code.

![Croissance du PIB](figures/01_croissance_pib.png)
-->



## Limites

- Les indicateurs de la Banque mondiale comportent des données manquantes, inégalement réparties selon les pays et les années ; les taux de couverture sont reportés dans les statistiques descriptives.
- Les corrélations observées ne disent rien de la causalité : elles servent ici à orienter l'exploration, pas à conclure.
- L'analyse est descriptive. La modélisation (séries temporelles, prévision) fera l'objet d'un dépôt distinct.

## Auteure

**KADEYA HARMIS** — Data Scientist · Data Analyst
[LinkedIn](https://linkedin.com/in/kadeya-harmis-3b185b348) · [GitHub](https://github.com/Kadeya-harmis)
