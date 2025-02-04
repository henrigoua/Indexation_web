from core.filter import filter_documents_any, filter_documents_all

def test_filter_documents_any():
    """
    Test the `filter_documents_any` function.

    - Checks if at least one word from the query exists in the tokens list.
    - Expects the function to return `True` when at least one match is found.
    """
    tokens = ["chocolate", "bar"]
    query = {"chocolate"}
    assert filter_documents_any(tokens, query), "The 'any' filter should return True when at least one match is found."

def test_filter_documents_all():
    """
    Test the `filter_documents_all` function.

    - Ensures that all words in the query exist in the tokens list.
    - Expects the function to return `True` only if all query words are present.
    """
    tokens = ["chocolate", "bar"]
    query = {"chocolate", "bar"}
    assert filter_documents_all(tokens, query), "The 'all' filter should return True only when all words are present."
