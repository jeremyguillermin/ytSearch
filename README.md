# YouTube Transcript Search

Ce script Python permet de rechercher des vidéos sur YouTube, de récupérer leurs transcriptions et d'y rechercher des mots-clés spécifiques. Il affiche les extraits de la transcription où les mots-clés ont été trouvés, avec le texte surligné et un lien direct vers le moment correspondant dans la vidéo.

## Fonctionnalités

- Recherche de vidéos sur l'ensemble de YouTube ou au sein d'une chaîne spécifique.
- Filtrage des résultats par langue, date de publication, et ordre de tri.
- Recherche de plusieurs mots-clés dans les transcriptions.
- Prise en charge des expressions régulières (regex) pour des recherches avancées.
- Affichage des extraits pertinents avec contexte (quelques phrases avant et après).
- Surlignage des mots-clés dans la console pour une meilleure lisibilité.
- Lien direct vers le moment précis de la vidéo où le mot-clé apparaît.
- Outil intégré pour trouver l'ID d'une chaîne à partir de son nom.

## Prérequis

- Python 3
- Un compte Google et une clé d'API pour le **YouTube Data API v3**.

## Installation

1.  **Clonez le projet ou téléchargez le script.**

2.  **Installez les dépendances Python :**
    Créez un environnement virtuel (recommandé) et installez les paquets nécessaires à partir de votre fichier `requirements.txt`. Si vous n'en avez pas, installez-les manuellement :

    ```bash
pip install google-api-python-client youtube-transcript-api youtube-dl
    ```

3.  **Configurez votre clé d'API :**
    Ouvrez le script et remplacez la valeur de la variable `api_key` par votre propre clé d'API YouTube.

    ```python
    api_key = "VOTRE_CLE_API_ICI"
    ```

## Utilisation

Le script s'utilise en ligne de commande avec différents arguments pour affiner votre recherche.

### Arguments

| Argument | Raccourci | Description | Défaut |
| --- | --- | --- |
| `--query` | `-q` | Termes de recherche pour les vidéos. | `None` |
| `--keywords` | `-k` | Mots-clés à rechercher dans la transcription (peut être multiple). | `None` |
| `--language` | `-l` | Code de la langue pour les transcriptions (ex: `fr`, `en`). | `en` |
| `--max-results` | `-m` | Nombre maximum de vidéos à analyser. | `10` |
| `--channel-id` | `-c` | ID de la chaîne YouTube pour limiter la recherche. | `None` |
| `--search-channel`| `-s` | Nom de la chaîne pour trouver son ID. | `None` |
| `--sort-by` | `-d` | Critère de tri (`date`, `relevance`, `viewCount`, etc.). | `relevance` |
| `--published-after`| `-a` | Filtre les vidéos publiées après cette date (YYYY-MM-DD). | `None` |
| `--published-before`| `-b` | Filtre les vidéos publiées avant cette date (YYYY-MM-DD). | `None` |
| `--use-regex` | `-r` | Active la recherche par expressions régulières pour les mots-clés. | `False` |

### Exemples

**1. Trouver l'ID d'une chaîne :**

```bash
python ytSearchV4.py -s "Nom De La Chaîne"
```

**2. Recherche simple dans tout YouTube :**
Rechercher des vidéos sur "l'intelligence artificielle" et y trouver les mots "futur" et "éthique".

```bash
python ytSearchV4.py -q "intelligence artificielle" -k futur éthique -l fr
```

**3. Recherche dans une chaîne spécifique avec tri par date :**
Rechercher "processeur" et "benchmark" dans les vidéos de la chaîne avec l'ID `UCXXXX...` , triées par date.

```bash
python ytSearchV4.py -c "UCXXXX..." -k processeur benchmark -d date
```

**4. Recherche avec des filtres de date :**
Rechercher des vidéos sur "ReactJS" publiées en 2023 et y trouver le mot "hooks".

```bash
python ytSearchV4.py -q "ReactJS" -k hooks -a 2023-01-01 -b 2023-12-31
```

**5. Utiliser des expressions régulières :**
Rechercher des mots commençant par "crypto" (comme "cryptomonnaie", "cryptographie") dans des vidéos sur la "blockchain".

```bash
python ytSearchV4.py -q "blockchain" -k "crypto\w*" -r
```
