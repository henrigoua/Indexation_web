import math
import random
from collections import Counter
from config import STOPWORDS
from utils.tokenizer import tokenize, process_query
from utils.synonym_handler import expand_query_with_synonyms

def bm25_score(query_tokens, document_tokens, k=1.2, b=0.75, avg_doc_length=10, total_documents=10):
    """
    Computes the BM25 relevance score for a document.

    Args:
        query_tokens (list): Tokenized words from the query.
        document_tokens (list): Tokenized words from the document.
        k (float): BM25 term frequency scaling parameter (default: 1.2).
        b (float): BM25 document length normalization parameter (default: 0.75).
        avg_doc_length (int): Average document length in the corpus (default: 10).
        total_documents (int): Total number of documents in the dataset (default: 10).

    Returns:
        float: The BM25 score for the document.
    """
    doc_length = len(document_tokens)
    doc_freq = Counter(document_tokens)
    score = 0.0

    for query_token in query_tokens:
        freq_of_query_token = doc_freq.get(query_token, 0)
        n_docs_with_token = sum(1 for doc in document_tokens if query_token in doc)
        
        if freq_of_query_token > 0:
            idf = math.log((total_documents - n_docs_with_token + 0.5) / (n_docs_with_token + 0.5) + 1)
            tf = freq_of_query_token / (freq_of_query_token + k * (1 - b + b * (doc_length / avg_doc_length)))
            score += idf * tf

    return score


def extract_title_and_variant(title):
    """
    Splits the product title into its main title and variant if separated by a hyphen.

    Args:
        title (str): The product title.

    Returns:
        tuple: A tuple containing:
            - List of tokens from the main title.
            - List of tokens from the variant (empty if no variant exists).
    """
    if " - " in title:
        main_title, variant = title.split(" - ", 1)
        return tokenize(main_title), tokenize(variant)
    return tokenize(title), []


def linear_score(query, document, data, title_boost=2.0, variant_boost=1.5, review_boost=0.5,
                 description_boost=0.3, brand_boost=0.7, avg_doc_length=10, review_count_cutoff=5,
                 few_review_penalty=0.01):
    """
    Computes a linear relevance score to rank documents based on multiple factors.

    The score is calculated using BM25 for term matching and additional factors like title match, 
    product variant match, customer reviews, brand, and description.

    Args:
        query (str): The search query.
        document (dict): The document containing title, description, and other features.
        data (dict): Dataset containing index structures for filtering and ranking.
        title_boost (float): Weight for title matches (default: 2.0).
        variant_boost (float): Weight for variant matches (default: 1.5).
        review_boost (float): Weight for review score contribution (default: 0.5).
        description_boost (float): Weight for description token matches (default: 0.3).
        brand_boost (float): Weight for brand presence (default: 0.7).
        avg_doc_length (int): Average document length for BM25 normalization (default: 10).
        review_count_cutoff (int): Minimum review count required for review contribution (default: 5).
        few_review_penalty (float): Small penalty for products with few reviews (default: 0.01).

    Returns:
        float: The computed relevance score for the document.
    """
    
    # Extract document tokens
    description = document.get("description", "")
    document_tokens = tokenize(description)

    title_tokens, variant_tokens = extract_title_and_variant(document.get("title", ""))
    
    query_tokens = process_query(query)
    expanded_query_tokens = expand_query_with_synonyms(query_tokens, data["origin_synonyms"])

    # Compute BM25-based score
    total_documents = len(data["products"])
    score = bm25_score(expanded_query_tokens, document_tokens, avg_doc_length=avg_doc_length, total_documents=total_documents)

    # Boost based on title matches
    title_match_score = sum(1 for query_token in expanded_query_tokens if query_token in title_tokens)
    score += title_match_score * title_boost

    # Boost based on variant matches
    variant_match_score = sum(1 for query_token in expanded_query_tokens if query_token in variant_tokens)
    score += variant_match_score * variant_boost  

    # Contribution based on description match
    description_score = sum(description_boost * (1 / (i + 1)) for i, token in enumerate(document_tokens) if token in expanded_query_tokens)
    score += description_score

    # Contribution based on customer reviews
    review_score = few_review_penalty  
    if document['url'] in data['reviews_index']:
        review_data = data['reviews_index'][document['url']]
        review_count = review_data['total_reviews']
        if review_count > review_count_cutoff:
            review_score = review_data['mean_mark'] * review_boost
    score += review_score

    # Contribution based on brand presence
    brand_score = brand_boost if document['url'] in data['brand_index'] else 0
    score += brand_score

    # Add slight random noise to prevent identical scores
    score += random.uniform(0.01, 0.05)

    return score


if __name__ == '__main__':
    # Example test cases
    data = {
        "title_index": {
            "chocolate": {"https://web-scraping.dev/product/1": [1]},
            "treat": {"https://web-scraping.dev/product/1": [2]},
        },
        "brand_index": {
            "chocodelight": [
                "https://web-scraping.dev/product/1", "https://web-scraping.dev/product/13"
            ],
            "timelessfootwear": [
                "https://web-scraping.dev/product/11"
            ],
        },
        "reviews_index": {
            "https://web-scraping.dev/product/1": {"total_reviews": 10, "mean_mark": 4.5},
            "https://web-scraping.dev/product/13": {"total_reviews": 3, "mean_mark": 3.2},
        },
        "products": [
            {
                "url": "https://web-scraping.dev/product/1",
                "title": "Nike Air Max - Rouge",
                "description": "Chaussures de sport Nike pour la course."
            },
            {
                "url": "https://web-scraping.dev/product/13",
                "title": "Montre de luxe - Édition limitée",
                "description": "Montre haut de gamme avec bracelet en cuir."
            }
        ]
    }

    query = "Nike Rouge"
    document_1 = data["products"][0]
    document_2 = data["products"][1]

    score_1 = linear_score(query, document_1, data, avg_doc_length=10)
    print(f"Linear score (Nike Rouge): {score_1}")

    score_2 = linear_score(query, document_2, data, avg_doc_length=10)
    print(f"Linear score (Montre Édition Limitée): {score_2}")
