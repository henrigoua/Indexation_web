import json
import os
from src.parser import parse_jsonl_file
from src.indexer import (
    create_inverted_index,
    create_reviews_index,
    create_features_index,
    create_positional_index  )
from src.storage import save_index

# Assurer que le répertoire 'index' existe
os.makedirs("index", exist_ok=True)

# Charger le dataset JSONL
input_file = "data/products.jsonl"

try:
    data = parse_jsonl_file(input_file)
except Exception as e:
    print(f"Error loading JSONL file: {e}")
    exit(1)

# Vérifier si les données ont bien été chargées
if not data:
    print("No documents loaded. Check if the JSONL file is empty or corrupted.")
    exit(1)

print(f"{len(data)} documents successfully loaded.")
print(f"Example document: {data[0] if data else 'No data available'}")

# Étape 1: Extraction et nettoyage des données
processed_data = []
for doc in data:
    try:
        url = doc.get("url", "")
        id_product = doc.get("id_product", None)
        variant = doc.get("variant", None)

        # Vérification et normalisation des reviews
        reviews = doc.get("reviews") or doc.get("customer_reviews") or doc.get("testimonials") or []
        if isinstance(reviews, str):
            reviews = [reviews] if reviews.strip() else []
        elif not isinstance(reviews, list):
            reviews = []

        # Extraction des features
        features = doc.get("features") or doc.get("product_features") or {}
        if isinstance(features, dict):
            features_text = " ".join(features.values())
        elif isinstance(features, list):
            features_text = " ".join(features)
        else:
            features_text = str(features).strip()

        # Conserver un doc seulement s'il a un URL
        if url:
            processed_data.append({
                "url": url,
                "id_product": id_product,
                "variant": variant,
                "title": doc.get("title", "").strip(),
                "description": doc.get("description", "").strip(),
                "features_text": features_text,
                "features": features,
                "reviews": reviews
            })
    except Exception as e:
        print(f"Error extracting information from a document: {e}")

# Vérifier si les données extraites sont valides
if not processed_data:
    print("No valid documents extracted. Check your data.")
    exit(1)

print(f"{len(processed_data)} documents were successfully processed.")

# Sauvegarde des données extraites
output_file = "index/processed_data.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=4, ensure_ascii=False)
    print(f"Extracted data saved in {output_file}.")
except Exception as e:
    print(f"Error saving extracted data: {e}")

print("URL processing and information extraction completed successfully.")

# Étape 2: Création et sauvegarde des index inversés (title & description)
try:
    inverted_indexes = {
        "title": create_inverted_index(processed_data, "title"),
        "description": create_inverted_index(processed_data, "description")
    }

    for field, index_data in inverted_indexes.items():
        if index_data:
            save_index(index_data, f"index/{field}_inverted_index.json")
            print(f"Inverted index for '{field}' created and saved.")
        else:
            print(f"No data found for inverted index '{field}', skipping.")

    print("Inverted index creation completed successfully.")

except Exception as e:
    print(f"Error during index creation: {e}")
    exit(1)

# Étape 3: Création et sauvegarde de l'index des reviews
try:
    reviews_count = sum(
        1 for doc in processed_data
        if isinstance(doc["reviews"], list) and doc["reviews"]
    )
    print(f"Total documents with reviews: {reviews_count}")

    reviews_index = create_reviews_index(processed_data)
    if reviews_index:
        save_index(reviews_index, "index/reviews_index.json")
        print("Reviews index successfully created and saved.")
    else:
        print("No reviews data found. Skipping reviews index creation.")

    print("Review processing completed successfully.")

except Exception as e:
    print(f"Error during reviews index creation: {e}")

# Étape 4: Création et sauvegarde de l'index des features
try:
    features_index, brand_origin_index = create_features_index(processed_data)

    if features_index:
        save_index(features_index, "index/features_index.json")
        print("Features index successfully created and saved.")
    else:
        print("No feature data found in features_index. Skipping.")

    if brand_origin_index:
        save_index(brand_origin_index, "index/brand_origin_index.json")
        print("Brand and Origin index successfully created and saved.")
    else:
        print("No brand/origin data found. Skipping.")

    print("Feature processing completed successfully.")

except Exception as e:
    print(f"Error during features index creation: {e}")

# Étape 5: Création et sauvegarde de l'index de positions (title, description)
try:
    from src.indexer import create_positional_index  # Assure-toi que create_positional_index est importée

    # Index de positions pour title
    title_pos_index = create_positional_index(processed_data, "title")
    if title_pos_index:
        save_index(title_pos_index, "index/title_pos_index.json")
        print("Positional index for 'title' created and saved.")
    else:
        print("No data for positional index 'title', skipping.")

    # Index de positions pour description
    desc_pos_index = create_positional_index(processed_data, "description")
    if desc_pos_index:
        save_index(desc_pos_index, "index/description_pos_index.json")
        print("Positional index for 'description' created and saved.")
    else:
        print("No data for positional index 'description', skipping.")

    print("Positional index creation completed successfully.")

except Exception as e:
    print(f"Error during positional index creation: {e}")
