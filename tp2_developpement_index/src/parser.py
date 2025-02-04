import json
from urllib.parse import urlparse, parse_qs
import re

def parse_jsonl_file(filename):
    """
    Reads a JSONL file and extracts product information including URLs, ID, variant,
    and other relevant fields for indexing.

    Args:
        filename (str): Path to the JSONL file.

    Returns:
        list: A list of dictionaries containing:
            - "id_product" (str or None): Extracted product ID.
            - "variant" (str or None): Product variant (if present).
            - "url" (str): Original URL.
            - "title" (str): Product title.
            - "description" (str): Product description.
            - "features" (list): List of product features.
            - "features_text" (str): Concatenated features for indexing.
            - "reviews" (list): List of reviews.

    """
    results = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)

                    # Extract URL-related information
                    url = data.get('url', "").strip()
                    id_product, variant = None, None

                    if url:
                        parsed_url = urlparse(url)
                        product_id_match = re.search(r'/product[s]?/(\d+)', parsed_url.path)
                        id_product = product_id_match.group(1) if product_id_match else None
                        variant = parse_qs(parsed_url.query).get('variant', [None])[0]

                    # Convert empty ID to None
                    id_product = id_product if id_product else None
                    variant = variant if variant else None

                    # Ignore products without an ID
                    if not id_product:
                        print(f"Skipping document without product ID: {data.get('title', 'No title')}")
                        continue

                    # Extract product fields
                    title = str(data.get('title', "")).strip()
                    description = str(data.get('description', "")).strip()

                    # Handle features: Normalize to a list
                    features = data.get('features', data.get('product_features', {}))
                    if isinstance(features, dict):
                        features_text = " ".join(features.values())  # Convertir un dict en texte
                        features_list = list(features.values())  # Convertir en liste
                    elif isinstance(features, str):
                        features_text = features.strip()
                        features_list = [features] if features.strip() else []
                    elif isinstance(features, list):
                        features_text = " ".join(features)
                        features_list = features
                    else:
                        features_text = ""
                        features_list = []

                    # Handle reviews: Try multiple keys in case reviews are stored differently
                    reviews = (
                        data.get("reviews")
                        or data.get("product_reviews")
                        or data.get("customer_reviews")
                        or data.get("testimonials")
                        or []
                    )

                    # Ensure reviews are a valid list
                    if isinstance(reviews, str):
                        reviews = [reviews] if reviews.strip() else []
                    elif not isinstance(reviews, list):
                        reviews = []

                    # Debug: Log extracted features and reviews
                    print(f"DEBUG - Extracted features for Product {id_product}: {features_text}")
                    print(f"DEBUG - Extracted {len(reviews)} reviews for Product {id_product}: {reviews[:3]}")

                    # Append structured data
                    results.append({
                        "id_product": id_product,
                        "variant": variant,
                        "url": url,
                        "title": title,
                        "description": description,
                        "features": features_list,
                        "features_text": features_text,  # Nouveau champ pour indexation
                        "reviews": reviews
                    })

                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {line.strip()} - {e}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    
    return results
