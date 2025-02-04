
from config import STOPWORDS
from utils.tokenizer import tokenize

def filter_documents_any(document_tokens, expanded_query_tokens):
    """
    Checks if *any* of the expanded query tokens are present in a document's tokens.

    Args:
        document_tokens (list): List of tokenized words from the document.
        expanded_query_tokens (list): List of tokenized words from the search query.

    Returns:
        bool: True if at least one query token is found in the document, False otherwise.
    """
    for token in expanded_query_tokens:
        if token in document_tokens:
            return True
    return False


def filter_documents_all(document_tokens, expanded_query_tokens, min_match=1):
    """
    Checks if *at least min_match* non-stopwords from the expanded query tokens 
    are present in a document's tokens.

    Args:
        document_tokens (list): List of tokenized words from the document.
        expanded_query_tokens (list): List of tokenized words from the search query.
        min_match (int): Minimum number of matches required for a document to be considered a match.

    Returns:
        bool: True if at least `min_match` non-stopword query tokens are found in the document, False otherwise.
    """
    matches = 0
    for token in expanded_query_tokens:
        if token in document_tokens and token not in STOPWORDS:
            matches += 1

    return matches >= min_match


if __name__ == '__main__':
    # Example usage for testing the filtering functions
    document_tokens = ["chocolate", "candy", "sweet", "treat"]
    
    # Query tokens for various test cases
    query_tokens_any_match = ["chocolate", "sour"]
    query_tokens_all_match = ["chocolate", "treat"]
    query_tokens_all_not_match = ["chocolate", "treat", "spicy"]
    query_tokens_all_not_match_with_stopword = ["chocolate", "treat", "a"]

    # Testing filter_documents_any function
    print(f"Any match (with match): {filter_documents_any(document_tokens, query_tokens_any_match)}")  # True
    print(f"Any match (no match): {filter_documents_any(document_tokens, ['sour', 'spicy'])}")  # False

    # Testing filter_documents_all function
    print(f"All match (with match): {filter_documents_all(document_tokens, query_tokens_all_match)}")  # True
    print(f"All match (no match): {filter_documents_all(document_tokens, query_tokens_all_not_match)}")  # False
    print(f"All match (with stopword, min_match=2): {filter_documents_all(document_tokens, query_tokens_all_not_match_with_stopword, min_match=2)}")  # True or False depending on stopword filtering
