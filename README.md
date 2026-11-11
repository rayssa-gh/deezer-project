# deezer-project

Script Python qui collecte des titres via l'API publique de Deezer, puis les analyse
(popularité et nombre de fans, comparaison entre genres).

## Prérequis

- Python 3.11
- Aucune clé d'API nécessaire (endpoints publics de Deezer)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

Le script crée deux fichiers dans `data/` : `genres.csv` et `tracks.csv`.
La collecte prend quelques minutes, car une pause est faite entre les appels pour
respecter le quota de l'API (50 appels / 5 s).

Elle est **reprenable** : si elle est interrompue, relancer la commande reprend où elle
s'était arrêtée, sans redemander les titres déjà collectés. Pour repartir de zéro,
supprimer le dossier `data/`.

## Structure du projet

```
.
├── main.py             # point d'entrée
├── config.py           # constantes (URL, chemins, colonnes, genres exclus...)
├── data_collector.py   # collecte : genres, classements, détails album et artiste
├── utils.py            # outils : appels API, lecture/écriture CSV, cache
├── requirements.txt
└── data/               # CSV générés
```

## Partie 1 : stratégie de collecte

Les titres sont collectés via les **classements par genre** de l'API Deezer
(`/chart/{genre_id}/tracks`).

1. **Choix des genres** : on récupère la liste des genres (`/genre`), puis on retire
   ceux qui ne sont pas purement musicaux ou trop régionaux (liste `EXCLUDE_GENRES`
   dans `config.py`). Il reste 15 genres internationaux comparables (Pop, Rock,
   Rap/Hip-Hop, Electro, Jazz...).
2. **Volume** : pour chaque genre, on prend les 100 premiers titres du classement,
   soit jusqu'à 1 500 lignes. Un titre présent dans plusieurs classements est conservé
   une fois par genre ; les titres uniques se comptent avec `track_id`.
3. **Équilibre entre genres** : chaque genre apporte environ le même nombre de titres.
4. **Enrichissement** : chaque titre est complété par deux appels, `/album/{id}`
   (date de sortie, label, durée, fans, type de disque) et `/artist/{id}`
   (nombre d'albums et de fans). Ces infos sont mises en cache : un titre déjà connu
   n'est jamais redemandé.
5. **Années de sortie** : les classements mêlent succès récents et titres plus anciens.
   La répartition par année n'est pas imposée à la collecte, elle est examinée
   lors de l'analyse.

### Données collectées

| Niveau  | Colonnes |
|---------|----------|
| Titre   | `track_id`, `track_title`, `track_duration`, `track_bpm`, `track_release_date`, `track_rank` |
| Album   | `album_title`, `album_release_date`, `label`, `album_duration`, `album_nb_fan`, `record_type` |
| Artiste | `artist_name`, `nb_album`, `nb_fan` |
| Genre   | `genre` |

### Limites

- Les classements reflètent la popularité actuelle : l'échantillon est biaisé vers les
  titres populaires et récents.
- Le `genre` d'un titre est celui du classement dans lequel il apparaît.
- Les valeurs manquantes sont remplacées par `0` ou `Inconnu`. Pour le BPM et le rang,
  `0` signifie « non renseigné » et sera exclu des calculs.
- Les rangs et nombres de fans évoluent dans le temps : les données correspondent à
  la date de collecte.

## Partie 2 : analyse

À venir.