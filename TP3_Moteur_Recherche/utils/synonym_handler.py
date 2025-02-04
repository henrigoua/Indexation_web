

def expand_query_with_synonyms(query_tokens, origin_synonyms):
    """
    Expands the query tokens with synonyms for origins if they exist in the provided dictionary.

    This function takes a list of query tokens and checks if any of them have synonyms
    in the `origin_synonyms` dictionary. If a match is found, it adds the original 
    term and its synonyms to the expanded query token set.

    Args:
        query_tokens (list): A list of words representing the search query.
        origin_synonyms (dict): A dictionary mapping origin names to their synonyms.

    Returns:
        list: A list of expanded query tokens, including original terms and matched synonyms.
    """
    print(f"Original query tokens: {query_tokens}")  # Debugging statement

    expanded_tokens = set(query_tokens)  # Initialize with the original query tokens

    for token in query_tokens:
        for origin, synonyms in origin_synonyms.items():
            if token in synonyms:
                expanded_tokens.add(origin)  # Add the origin itself
                expanded_tokens.update(synonyms)  # Add all synonyms

    print(f"Expanded query tokens: {expanded_tokens}")  # Debugging statement

    return list(expanded_tokens)

if __name__ == '__main__':
    # Example usage with predefined synonyms
    origin_synonyms = {
        "usa": ["united states", "united states of america", "america"],
        "france": ["fr"],
        "spain": ["spanish"],
        "germany": ["deutschland"],
        "south korea": ["korea"],
        "switzerland": ["swiss"],
        "netherlands": ["dutch"]
    }

    query_tokens = ["united", "states", "swiss", "sneakers"]
    
    expanded_tokens = expand_query_with_synonyms(query_tokens, origin_synonyms)

    print(f"Expanded tokens: {expanded_tokens}")
