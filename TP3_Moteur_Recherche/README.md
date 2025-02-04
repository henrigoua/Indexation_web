# TP3 - Moteur de Recherche

## Objectif

Développer un moteur de recherche qui utilise les index créés précédemment pour retourner et classer des résultats pertinents.

## Fonctionnalités

- Recherche rapide à partir d'une base de données JSON indexée.
- Gestion des synonymes pour améliorer la pertinence des résultats.
- Classement des résultats basé sur des scores de pertinence.
- Interface utilisateur avec une barre de recherche simple.
- API REST permettant d'effectuer des recherches et de retourner les résultats sous forme de JSON.

---

## Structure du Projet

```
TP3_Moteur_Recherche/
├── data/                   # Contient les fichiers de données pour le moteur de recherche
│   ├── brand_index.json         # Index des marques
│   ├── description_index.json   # Index des descriptions
│   ├── domain_index.json        # Index des domaines
│   ├── origin_index.json        # Index des origines
│   ├── origin_synonyms.json     # Synonymes pour l'amélioration des recherches
│   ├── products.jsonl           # Liste des produits au format JSONL
│   ├── rearranged_products.jsonl # Produits réorganisés pour une meilleure recherche
│   ├── reviews_index.json       # Index des avis clients
│   ├── title_index.json         # Index des titres
│
├── static/                 # Fichiers statiques pour le frontend
│   ├── css/                    # Dossier contenant les fichiers CSS
│   │   ├── styles.css          # Feuille de style principale
│   ├── js/                     # Dossier contenant les scripts JavaScript
│       ├── script.js           # Logique de recherche côté client
│
├── templates/             # Modèles HTML
│   ├── index.html             # Interface utilisateur principale
│
├── utils/                  # Modules utilitaires
│   ├── data_loader.py         # Chargement et manipulation des fichiers de données
│   ├── synonym_handler.py     # Gestion et expansion des synonymes
│   ├── tokenizer.py           # Tokenisation et normalisation des textes
│
├── core/                   # Modules principaux pour le moteur de recherche
│   ├── filter.py              # Logique de filtrage des documents
│   ├── ranking.py             # Algorithmes de classement des résultats
│   ├── search_engine.py       # Logique principale pour le moteur de recherche
│
├── tests/                  # Tests unitaires et d'intégration pour valider le projet
│   ├── test_api.py            # Tests pour l'API FastAPI
│   ├── test_data_loader.py    # Tests pour le module data_loader
│   ├── test_filter.py         # Tests pour le module de filtrage
│   ├── test_ranking.py        # Tests pour le module de classement
│   ├── test_search_engine.py  # Tests pour le moteur de recherche
│
├── env/                   # Dossier pour les variables d'environnement et configurations locales
│   ├── .env                  # Fichier des variables d'environnement (ex : clés API, paramètres sensibles)
│
├── api.py                  # API FastAPI qui expose les fonctionnalités du moteur de recherche
├── config.py               # Configuration globale du projet (paramètres par défaut, chemins, etc.)
├── README.md               # Documentation du projet (description, installation, utilisation)
├── requirements.txt
```

---

## Installation et Lancement

### Pré-requis

- Python 3.8 ou supérieur
- Pip installé
- Un éditeur de texte ou IDE

### Étapes d'installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-projet/moteur-recherche.git
   cd moteur-recherche
   ```

2. **Créer un environnement virtuel :**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer le serveur :**
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Accéder à l'interface utilisateur :**
   - Ouvrez [http://localhost:8000](http://localhost:8000) dans votre navigateur.

---

## API

### Endpoint principal

- **URL :** `/search`
- **Méthode :** `POST`
- **Payload :**
  ```json
  {
    "query": "exemple de recherche",
    "search_type": "any",
    "top_k": 5
  }
  ```
- **Réponse :**
  ```json
  {
    "query": "exemple de recherche",
    "expanded_tokens": ["exemple", "recherche"],
    "execution_time": "0.002 sec",
    "results": [
      {
        "score": 4.5,
        "title": "Exemple de produit",
        "url": "http://example.com/product/1"
      }
    ]
  }
  ```

---

## Tests

### Ajouter des tests

1. Créez un répertoire `tests` si ce n'est pas encore fait.
2. Ajoutez des fichiers de tests pour chaque module :
   - `test_data_loader.py`
   - `test_search_engine.py`
   - `test_filter.py`
   - `test_ranking.py`
3. Exemple de commande pour exécuter les tests :
   ```bash
   pytest tests/
   ```

---

## Interface utilisateur

1. Entrez une requête dans la barre de recherche.
2. Cliquez sur le bouton "Rechercher".
3. Visualisez les résultats avec le titre, le score, l'origine, la description et un lien vers le produit.

---

## Contribution

1. Forkez le projet.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b ma-branche
   ```
3. Faites vos modifications et commitez-les :
   ```bash
   git commit -m "Description de la modification"
   ```
4. Poussez vos modifications :
   ```bash
   git push origin ma-branche
   ```
5. Ouvrez une pull request.

---

## Auteurs

**GOUA Beedi**