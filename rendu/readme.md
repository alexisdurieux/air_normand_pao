# Air Normandie PAO

## Installation

Dépendances: `virtualenv`
``` shell

# Récupération du répertoire
git clone *url*

# Création de l'environnement virtuel
virtualenv venv --python=python3
source venv/bin/activate 

# Installation des dépendances
pip install -r requirements.txt


```

## Preprocessing

On suppose que les fichiers `csv` permettant la génération des données ne comportent pas de headers. De plus on suppose 
que le séparateur des fichiers `csv` est `;`.

Commandes disponibles:
- `python preprocessing.py clean *fichier.csv*`. En fonction du mapping dans le dictionnaire présent dans `preprocessing.py` 
(à remplacer par un fichier .json) remplace les clés pour les uniformiser pour l'apprentissage à venir.
- `python preprocessing.py create_pickle *folder* *pickle_name.pkl*`: Crée un pickle à partir d'un répertoire contenant deux csv:
    - **AllNO2_QH.csv** contenant l'ensemble des données relatives au NO2
    - **Env_QH.csv** contenant l'ensemble des données de l'environnement (gradient, température, pressure...)
- `python preprocessing.py normalize_pickle *input_pickle.pkl* *output_pickle.pkl*`: normalisation d'un pickle
    
## TODO

- Preprocessing adaptatif en fonction des données (PM, NO2 etc..)
- training.py
- visualize.py
