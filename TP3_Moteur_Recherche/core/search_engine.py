import time
import random
from utils.data_loader import load_all_data
from utils.tokenizer import process_query, tokenize
from utils.synonym_handler import expand_query_with_synonyms
from core.filter import filter_documents_any, filter_documents_all
from core.ranking import linear_score, extract_title_and_variant

# Global variable to avoid repeated logs
query_logged = set()

def adjusted_linear_score(query, doc, data, avg_doc_length=10):
    """
    Computes an adjusted linear score by adding weighting for title matches and a slight random variation.

    Args:
        query (str): The search query.
        doc (dict): The document to be ranked.
        data (dict): The dataset containing indexed documents.
        avg_doc_length (int): The average document length for normalization (default: 10).

    Returns:
        float: The adjusted score of the document.
    """
    base_score = linear_score(query, doc, data, avg_doc_length=avg_doc_length)

    # Bonus if the title contains the exact query
    title_match_bonus = 0.3 if query.lower() in doc.get("title", "").lower() else 0

    # Add a small random variation to avoid ties
    random_variation = random.uniform(0.01, 0.05)

    return base_score + title_match_bonus + random_variation


def search(query, data, search_type="any", avg_doc_length=10, min_match=1):
    """
    Performs a search query by filtering and ranking relevant documents.

    Args:
        query (str): The search query.
        data (dict): The dataset containing indexed documents.
        search_type (str): Filtering mode, either "any" (match any term) or "all" (match all terms).
        avg_doc_length (int): Average document length for ranking (default: 10).
        min_match (int): Minimum number of matched tokens required for filtering (default: 1).

    Returns:
        list: A list of ranked documents sorted by relevance.
    """
    
    global query_logged
    start_time = time.time()  # Start the execution timer

    # Avoid duplicate logging for the same query
    if query not in query_logged:
        query_tokens = process_query(query)
        expanded_query_tokens = expand_query_with_synonyms(query_tokens, data["origin_synonyms"])
        print(f"\nSearching for: {query} (tokens: {expanded_query_tokens})")
        query_logged.add(query)
    else:
        expanded_query_tokens = set(query.split())  # Directly use split words if already logged

    filtered_documents = set()  # Use a set to avoid duplicates
    
    for product in data["products"]:
        title_tokens, variant_tokens = extract_title_and_variant(product.get("title", ""))
        description_tokens = tokenize(product.get("description", ""))

        # Check if query matches title, description, or variant
        match_title = filter_documents_any(title_tokens, expanded_query_tokens)
        match_variant = filter_documents_any(variant_tokens, expanded_query_tokens)
        match_description = filter_documents_any(description_tokens, expanded_query_tokens)

        if search_type == "any":
            if match_title or match_variant or match_description:
                filtered_documents.add(product["url"])
        elif search_type == "all":
            if filter_documents_all(title_tokens, expanded_query_tokens, min_match=min_match) or \
               filter_documents_all(variant_tokens, expanded_query_tokens, min_match=min_match) or \
               filter_documents_all(description_tokens, expanded_query_tokens, min_match=min_match):
                filtered_documents.add(product["url"])
        else:
            raise ValueError("Invalid search type, specify 'all' or 'any'")

    # Rank documents using the adjusted linear score
    ranked_documents = sorted(
        [doc for doc in data["products"] if doc["url"] in filtered_documents],
        key=lambda doc: adjusted_linear_score(query, doc, data, avg_doc_length=avg_doc_length),
        reverse=True
    )

    elapsed_time = time.time() - start_time  # Execution time
    print(f"Search completed in {elapsed_time:.4f} seconds")

    return ranked_documents


if __name__ == '__main__':
    # Load data
    data_directory = 'data'
    data = load_all_data(data_directory)

    queries = [
        "sweet chocolate treat from usa",
        "chocolate from united states",
        "Nike Rouge",
        "leather sneakers",
        "teal potion"
    ]

    for query in queries:
        results = search(query, data, search_type="any")
        
        # Structured display of results
        print(f"\nResults for: {query}")
        print(f"  Top 5 ranked results:")
        for i, doc in enumerate(results[:5], start=1):
            score = adjusted_linear_score(query, doc, data)
            print(f"    {i}. Score: {score:.2f} - {doc.get('title')} ({doc.get('url')})")
