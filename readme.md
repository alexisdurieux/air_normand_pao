# Atmonormandie PAO Documentation

## Installation

**Prérequis: Python3**

* Créer un environnement virtuel *python3*: `virtualenv venv --python=python3`
* Pour lancer l'environnement virtuel: `source venv/bin/activate` et `deactivate` pour désactiver.
* `pip install -r requirements.txt` pour installer les dépendances

## Preprocessing

Le script `preprocessing.py` à la racine du projet permet d'effectuer des transformations sur les données.
Fonctionnement du script:
* `python preprocessing.py -h`: affiche l'aide
* `python preprocessing.py <mode> <input>`:
    * `python preprocessing.py clean <input>`: *input* est soit un fichier `csv` ou bien un répertoire. Le cas échéant, tous les fichiers `csv` du répertoire seront processés. Ce script permet de transformer les fichiers csv en changeant les noms des colonnes. Pour modifier le mapping il faut modifier le dictionnaire `NORMALIZED_COLUMN_NAMES` définissant ces transformations dans le fichier `preprocessing.py`
    * `python preprocessing.py create_pickle <folder> --type <NO2/PM>`: *folder* est un répertoire contenant un fichier d'environnement contenant les données telles que le gradient de température, la température, la pluviométrie, la pression et l'humidité ainsi qu'un csv contenant les données PM ou NO2. Les noms des fichiers doivent être: *ENV_QH.csv*, *AllNO2_QH.csv*, *AllPM_QH.csv* ou bien être modifiés dans le code.
    *type* est un argument obligatoire pour ce mode. Soit il est *NO2*, ou bien *PM* afin de savoir quel pickle créer.
    * `python preprocessing.py normalize_pickle <input_name> --type <NO2/PM>`: normalise un pickle. Le type est nécessaire puisque les colonnes cibles sont différentes en fonction du pickle.
    * L'argument optionel *--output OUTPUT* peut être ajouté à l'usage de chacun des modes pour donner un nom de fichier de sortie (ne marche pas si un répertoire est en entrée pour le *clean* mode).

### Exemple d'utilisation
```
# Clean des csv
Avec data/sud3 contenant AllNO2_QH.csv, AllPM_QH.csv, Env_QH.csv et GradientTemp_15minDataSet.csv.
python preprocessing.py clean data/sud3 --output data/clean 
==> data/sud3/GradientTemp_15minDataSet.csv cleaned with success !
    data/sud3/AllPM_QH.csv cleaned with success !
    data/sud3/AllNO2_QH.csv cleaned with success !


# Création des pickles
python preprocessing.py create_pickle data/clean --type NO2 --output data/clean/sud3_no2.pkl
python preprocessing.py create_pickle data/clean --type PM --output data/clean/sud3_pm.pkl

# Normalisation des pickles
python preprocessing.py normalize_pickle data/clean/sud3_no2.pkl --type NO2 --output data/clean/sud3_no2_normalized.pkl
python preprocessing.py normalize_pickle data/clean/sud3_pm.pkl --type PM --output data/clean/sud3_pm_normalized.pkl

```

**Modifier directement le code en cas de changement de format des csv d'entrée. (i.e noms des capteurs, nombre de variables à normaliser etc..)**