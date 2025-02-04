from core.ranking import linear_score

def test_linear_score():
    """
    Test the `linear_score` function.

    - Evaluates the relevance score of a document based on a given query.
    - Expects a positive score when the document contains relevant terms.
    """
    query = "Chocolate"
    document = {"title": "Chocolate Bar", "description": "A sweet treat."}
    data = {"origin_synonyms": {}}  # Additional data, such as synonyms, if applicable.

    score = linear_score(query, document, data)
    
    assert score > 0, "The score should be positive for a relevant document."
