from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time
from fastapi.responses import HTMLResponse
from utils.data_loader import load_all_data
from utils.tokenizer import process_query, tokenize
from utils.synonym_handler import expand_query_with_synonyms
from utils.scraper import scrape_product_details
from core.filter import filter_documents_any, filter_documents_all
from core.ranking import linear_score, extract_title_and_variant
from fuzzywuzzy import fuzz

# Initialize FastAPI
app = FastAPI(title="Search Engine API", description="API for a search engine using FastAPI")

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load data on startup
data_directory = "data"
data = load_all_data(data_directory)

class SearchRequest(BaseModel):
    """
    Defines the request body for the search endpoint.

    Attributes:
        query (str): The search query.
        search_type (str): The type of search ("any" or "all").
        top_k (int): The number of results to return.
    """
    query: str
    search_type: str = "any"  # "any" or "all"
    top_k: int = 5  # Number of results to return


def normalize_text(text):
    """
    Normalize a string by converting it to lowercase and stripping extra spaces.

    Args:
        text (str): The input text.

    Returns:
        str: The normalized text.
    """
    return text.strip().lower()


def partial_match(query, text_tokens, threshold=70):
    """
    Checks if a partial match exists between the query and tokenized text using fuzzy matching.

    Args:
        query (str): The search query.
        text_tokens (list): List of tokenized words from a document.
        threshold (int): Similarity threshold (default is 70).

    Returns:
        bool: True if a match is found, False otherwise.
    """
    query = normalize_text(query)
    for token in text_tokens:
        if fuzz.partial_ratio(query, normalize_text(token)) > threshold:
            return True
    return False


@app.get("/", response_class=HTMLResponse)
def home():
    """
    Home route that serves the user interface.

    Returns:
        str: The HTML content of the homepage.
    """
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.post("/search")
def search_endpoint(request: SearchRequest):
    """
    Endpoint for performing a search query and returning relevant results.

    Args:
        request (SearchRequest): The search request containing query parameters.

    Returns:
        dict: A dictionary containing the search results and metadata.
    """
    start_time = time.time()

    # Preprocess query
    query_tokens = process_query(request.query)
    expanded_query_tokens = expand_query_with_synonyms(query_tokens, data["origin_synonyms"])
    
    print(f"Searching for: {request.query} (tokens: {expanded_query_tokens})")

    # Filter documents
    filtered_documents = set()
    for product in data["products"]:
        title_tokens, variant_tokens = extract_title_and_variant(product.get("title", ""))
        description_tokens = tokenize(product.get("description", ""))

        match_title = any(partial_match(token, title_tokens) for token in expanded_query_tokens)
        match_variant = any(partial_match(token, variant_tokens) for token in expanded_query_tokens)
        match_description = any(partial_match(token, description_tokens) for token in expanded_query_tokens)

        if request.search_type == "any":
            if match_title or match_variant or match_description:
                filtered_documents.add(product["url"])
        elif request.search_type == "all":
            if all(partial_match(token, title_tokens) for token in expanded_query_tokens) or \
               all(partial_match(token, variant_tokens) for token in expanded_query_tokens) or \
               all(partial_match(token, description_tokens) for token in expanded_query_tokens):
                filtered_documents.add(product["url"])
        else:
            return {"error": "Invalid search_type. Use 'any' or 'all'."}

    # Rank documents
    ranked_documents = sorted(
        [doc for doc in data["products"] if doc["url"] in filtered_documents],
        key=lambda doc: linear_score(request.query, doc, data),
        reverse=True
    )

    # Execution time
    elapsed_time = time.time() - start_time

    # Return search results
    return {
        "query": request.query,
        "expanded_tokens": list(expanded_query_tokens),
        "execution_time": f"{elapsed_time:.4f} sec",
        "total_documents_in_index": len(data["products"]),
        "filtered_documents_count": len(filtered_documents),
        "results": [
            {
                "score": round(linear_score(request.query, doc, data), 2),
                "title": doc.get("title"),
                "url": doc.get("url"),
                "image": doc.get("image", "default-image.png"),
                "description": doc.get("description", "Description not available"),
                "reviews": {
                    "average_rating": round(
                        sum(review.get("rating", 0) for review in doc.get("product_reviews", [])) /
                        max(len(doc.get("product_reviews", [])), 1), 2
                    ) if doc.get("product_reviews") else None,
                    "total_reviews": len(doc.get("product_reviews", [])),
                    "review_details": doc.get("product_reviews", [])
                },
                "features": {
                    "made_in": doc.get("product_features", {}).get("made in", "Unknown origin"),
                    "brand": doc.get("product_features", {}).get("brand", "Brand not specified")
                }
            }
            for doc in ranked_documents[:request.top_k]
        ],
        "metadata": {
            "total_results_returned": len(ranked_documents[:request.top_k]),
            "execution_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "server_info": "Search Engine API v1.0",
            "filter_criteria": {
                "search_type": request.search_type,
                "top_k": request.top_k
            }
        }
    }


@app.get("/scrape-product/")
def scrape_product(url: str = Query(..., description="URL of the product page to scrape")):
    """
    Endpoint for dynamically extracting product details (origin and images) from a given URL.

    Args:
        url (str): The product page URL.

    Returns:
        dict: A dictionary containing extracted product details.
    """
    try:
        # Call scraping function
        product_details = scrape_product_details(url)
        
        return {
            "url": url,
            "title": product_details.get("title", "Title not available"),
            "description": product_details.get("description", "Description not available"),
            "features": {
                "made_in": product_details.get("features", {}).get("made in", "Unknown origin"),
                "brand": product_details.get("features", {}).get("brand", "Brand not specified"),
            },
            "images": product_details.get("images", []),
            "reviews": product_details.get("reviews", []),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during scraping: {str(e)}")
