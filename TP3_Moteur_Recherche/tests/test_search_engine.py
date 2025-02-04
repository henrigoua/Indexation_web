from core.search_engine import search

def test_search_results():
    """
    Test the `search` function.

    - Ensures that the search function returns relevant results for a given query.
    - Expects at least one result when searching for a term present in the dataset.
    """
    data = {
        "products": [
            {"title": "Chocolate Bar", "url": "http://example.com"}
        ]
    }
    query = "Chocolate"

    results = search(query, data)
    
    assert len(results) > 0, "The search should return results when a matching product is found."
