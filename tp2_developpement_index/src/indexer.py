import json
import re
from collections import defaultdict

def load_stopwords(filepath="stopwords.txt"):
    """
    Loads a list of stopwords from a file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(word.strip() for word in f.readlines())
    except FileNotFoundError:
        print(f"Warning: Stopwords file '{filepath}' not found. Using an empty set.")
        return set()

STOPWORDS = load_stopwords()

def clean_text(text):
    """
    Tokenizes and cleans text by removing non-alphanumeric characters, lowercasing,
    and filtering out stopwords.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word not in STOPWORDS]

def create_inverted_index(data, field):
    """
    Creates an inverted index for a given field (title or description).
    Each word is mapped to a set of product IDs where it appears.
    """
    inverted_index = defaultdict(set)

    for doc in data:
        product_id = str(doc.get("id_product")) if doc.get("id_product") else None
        if not product_id:
            continue

        field_content = doc.get(field, "")
        if isinstance(field_content, str) and field_content.strip():
            words = clean_text(field_content)
            for w in words:
                inverted_index[w].add(product_id)

    return {k: list(v) for k, v in inverted_index.items()}

def create_positional_index(data, field):
    """
    Creates a positional index for a given field (e.g., 'title' or 'description').
    Each word is associated with a list of [doc_id, [positions]] pairs.

    Structure intermédiaire:
      positional_index[word][doc_id] = {positions}
    
    Puis conversion en JSON:
      final_index[word] = [
         [doc_id, [pos1, pos2, ...]], ...
      ]
    """
    from collections import defaultdict

    # { word: { doc_id: set of positions } }
    positional_index = defaultdict(lambda: defaultdict(set))

    for doc in data:
        # Récupérer l'ID du document
        product_id = str(doc.get("id_product")) if doc.get("id_product") else None
        if not product_id:
            continue  # Ignorer si pas d'ID produit

        # Récupérer le contenu du champ (title ou description)
        field_content = doc.get(field, "")
        if not isinstance(field_content, str) or not field_content.strip():
            continue  # Ignorer si pas une chaîne valide

        # Nettoyer le texte et récupérer la liste de mots
        words = clean_text(field_content)

        # Ajouter les positions (index dans la liste de mots)
        for pos, word in enumerate(words):
            positional_index[word][product_id].add(pos)

    # Conversion en format final
    final_index = {}
    for word, doc_map in positional_index.items():
        final_index[word] = []
        for doc_id, positions_set in doc_map.items():
            # Trier et convertir l'ensemble en liste pour JSON
            sorted_positions = sorted(positions_set)
            final_index[word].append([doc_id, sorted_positions])

    return final_index


def create_features_index(data):
    from collections import defaultdict
    features_index = defaultdict(set)
    brand_origin_index = defaultdict(set)

    for doc in data:
        product_id = str(doc.get("id_product")) if doc.get("id_product") else None
        if not product_id:
            continue
        
        # Extraire features_text comme d'habitude
        features_text = doc.get("features_text", "")
        # Nettoyer et indexer la partie textuelle
        if features_text:
            words = clean_text(features_text)
            for word in words:
                features_index[word].add(product_id)

        # Récupérer le dictionnaire features pour trouver brand et made in
        features_dict = doc.get("features", {})
        if isinstance(features_dict, dict):
            # Extraire la marque et l'origine
            brand_value = features_dict.get("brand", "").strip()
            origin_value = features_dict.get("made in", "").strip()

            # Mettre en minuscule pour uniformiser
            brand = brand_value.lower()
            origin = origin_value.lower()

            # Indexer la marque
            if brand:
                brand_origin_index[brand].add(product_id)
            # Indexer l'origine
            if origin:
                brand_origin_index[origin].add(product_id)

    # Convertir en format JSON-friendly
    features_index_json = {k: list(v) for k, v in features_index.items()}
    brand_origin_index_json = {k: list(v) for k, v in brand_origin_index.items()}

    return features_index_json, brand_origin_index_json


def create_reviews_index(data):
    """
    Creates an index for reviews, storing:
    - total number of reviews
    - average rating
    - last rating
    """
    reviews_index = {}

    for doc in data:
        product_id = str(doc.get("id_product")) if doc.get("id_product") else None
        if not product_id:
            continue

        reviews = doc.get("reviews", [])
        if not isinstance(reviews, list) or not reviews:
            continue

        try:
            ratings = []
            for r in reviews:
                if isinstance(r, dict):
                    for k in ["rating", "score", "stars"]:
                        if k in r and isinstance(r[k], (int, float)):
                            ratings.append(r[k])

            if ratings:
                reviews_index[product_id] = {
                    "total_reviews": len(ratings),
                    "average_rating": round(sum(ratings) / len(ratings), 2),
                    "last_rating": ratings[-1]
                }
        except Exception as e:
            print(f"Error processing reviews for product {product_id}: {e}")

    return reviews_index
