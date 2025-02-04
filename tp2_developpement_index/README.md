
# **README - TP d'Indexation**

Ce projet a pour objectif de créer différents types d’index (inversés, positionnels, features, reviews) à partir d’un jeu de données e-commerce.

## **1. Structure du projet**

```
├── data/
│   └── products.jsonl      # Jeu de données JSONL (un document par ligne)
├── index/
│   ├── processed_data.json         # Données nettoyées et structurées
│   ├── title_inverted_index.json   # Index inversé sur le titre
│   ├── description_inverted_index.json  # Index inversé sur la description
│   ├── reviews_index.json          # Index stockant stats sur les reviews
│   ├── features_index.json         # Index textuel des features
│   ├── brand_origin_index.json     # Index dédié à la marque & l'origine (optionnel)
│   ├── title_pos_index.json        # Index de positions pour les titres
│   ├── description_pos_index.json  # Index de positions pour les descriptions
│   └── ...
├── src/
│   ├── parser.py          # Extrait & nettoie les données depuis products.jsonl
│   ├── indexer.py         # Regroupe les fonctions de création d'index
│   ├── storage.py         # Fonctions de sauvegarde/chargement (JSON)
│   └── ...
├── main.py                # Point d'entrée pour l'exécution du pipeline
├── stopwords.txt          # Fichier de stopwords (si nécessaire)
└── README.md              # Présentation globale du projet
```

---

## **2. Description des fichiers principaux**

### **2.1 `parser.py`**
- Contient la fonction `parse_jsonl_file` qui :
  - Lit le fichier `products.jsonl`.
  - Extrait les champs nécessaires : `id_product`, `url`, `title`, `description`, `features`, `reviews`, etc.
  - Fait un prétraitement (suppression des documents sans ID, normalisation de certains champs).
  - Retourne une liste de dictionnaires structurés.

### **2.2 `indexer.py`**
- Regroupe les fonctions de création d’index :
  - **`create_inverted_index(data, field)`** : crée un index inversé pour un champ simple (ex. *title*, *description*).
  - **`create_features_index(data)`** : crée un index inversé pour les *features* (caractéristiques du produit) et, éventuellement, un index séparé pour la *marque* et l’*origine* (ex. `brand_origin_index`).
  - **`create_reviews_index(data)`** : crée un index où on stocke le nombre total de reviews, la moyenne et la dernière note pour chaque produit.
  - **`create_positional_index(data, field)`** : crée un index de positions pour un champ donné (ex. *title*, *description*), permettant de retrouver la position de chaque mot dans chaque document.

### **2.3 `storage.py`**
- Fonctions utilitaires pour sauvegarder et charger un dictionnaire Python au format JSON.
- Exemples : 
  - **`save_index(index, filename)`** : enregistre un index sous forme de fichier JSON.
  - **`load_index(filename)`** : charge l’index depuis un fichier JSON.

### **2.4 `main.py`**
- Point d’entrée du pipeline :
  1. Charge et parse les données brutes (`products.jsonl`) via `parser.py`.
  2. Génère un ensemble de `processed_data.json`.
  3. Appelle les fonctions d’indexation de `indexer.py` (inverted index, positional index, reviews, features, etc.).
  4. Sauvegarde les résultats dans le dossier `index/`.

---

## **3. Étapes pour exécuter le pipeline**

1. **Installer les dépendances** (si besoin) :
   ```bash
   pip install -r requirements.txt
   ```

2. **Vérifier la présence des données** :
   - Assure-toi que `products.jsonl` se trouve bien dans le répertoire `data/`.

3. **Lancer le script principal** :
   ```bash
   python main.py
   ```
   - Le script va lire `data/products.jsonl`, extraire et normaliser les documents, et créer divers index dans `index/`.

4. **Consulter les index** :
   - `head -n 20 index/title_inverted_index.json` pour voir un extrait de l’index inversé sur les titres.
   - `head -n 20 index/features_index.json` pour voir l’index textuel des features.
   - `head -n 20 index/title_pos_index.json` pour voir l’index de positions du *title*, etc.

---

## **4. Fonctionnalités couvertes**

1. **Index inversé simple** 
   - Sur les champs *title* et *description*, création d’un dictionnaire `{ mot : [liste_produits] }`.

2. **Index de position**
   - Sur *title* et *description*, pour retrouver la position de chaque mot dans chaque document.

3. **Index des reviews**  
   - Stocke :
     - le nombre total de reviews par produit,
     - la note moyenne,
     - la dernière note enregistrée,
     - sous forme d’un dictionnaire `{ "product_id": {"total_reviews": X, "average_rating": Y, ...}, ... }`.

4. **Index des features**  
   - Un index inversé pour les caractéristiques du produit (matériau, couleur, etc.).
   - Possibilité d’avoir un **index séparé** pour la marque et l’origine (`brand`, `made in`).

---

---

## **6. Auteurs**

- **Auteur** : Goua BBEDI
-

