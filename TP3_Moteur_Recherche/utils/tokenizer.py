import re
import unicodedata
from config import STOPWORDS

def normalize_text(text):
    """
    Normalize text by removing accents, converting to lowercase, 
    and stripping unnecessary spaces.

    Args:
        text (str): The input text.

    Returns:
        str: The normalized text.
    """
    text = text.lower()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
    return text.strip()

def tokenize(text):
    """
    Tokenizes text by converting it to lowercase, removing non-alphanumeric characters, 
    and splitting into words. Also handles variants separated by a hyphen.

    Args:
        text (str): The input text.

    Returns:
        list: A list of tokens, including the variant if present.
    """
    text = text.lower()
    
    # Check if the text contains a hyphen "-" and extract the variant if present
    main_part, variant = text.split(" - ", 1) if " - " in text else (text, None)

    # Clean the main part by removing non-alphanumeric characters
    main_part = re.sub(r'[^a-z0-9\s]', '', main_part)
    
    tokens = main_part.split()

    # Add the variant as a distinct token if it exists
    if variant:
        variant = re.sub(r'[^a-z0-9\s]', '', variant)  # Clean the variant
        tokens.append(variant)  # Add the variant to the tokens

    return tokens

def normalize_tokens(tokens):
    """
    Removes stopwords from a list of tokens.

    Args:
        tokens (list): A list of tokenized words.

    Returns:
        list: A list of tokens without stopwords.
    """
    return [token for token in tokens if token not in STOPWORDS]

def process_query(query):
    """
    Processes a search query by tokenizing and normalizing it.

    Args:
        query (str): The search query.

    Returns:
        list: A list of processed tokens.
    """
    tokens = tokenize(query)
    return normalize_tokens(tokens)

def extract_title_and_variant(title):
    """
    Splits the main title and the variant if separated by a hyphen.

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

if __name__ == '__main__':
    # Example tests
    text1 = "Nike Air Max - Rouge"
    text2 = "Montre de luxe - Édition limitée"
    text3 = "Smartphone Android - 128Go"

    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    tokens3 = tokenize(text3)

    print(f"Tokens 1: {tokens1}")  # ['nike', 'air', 'max', 'rouge']
    print(f"Tokens 2: {tokens2}")  # ['montre', 'de', 'luxe', 'édition', 'limitée']
    print(f"Tokens 3: {tokens3}")  # ['smartphone', 'android', '128go']
