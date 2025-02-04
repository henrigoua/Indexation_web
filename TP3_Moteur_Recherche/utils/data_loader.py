
import json
import jsonlines

def load_json(filepath):
    """
    Load a JSON file and return its content as a dictionary.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_jsonl(filepath):
    """
    Load a JSONL (JSON Lines) file and return its content as a list of dictionaries.

    Args:
        filepath (str): Path to the JSONL file.

    Returns:
        list: List of parsed JSON objects.
    """
    data = []
    with jsonlines.open(filepath) as reader:
        for obj in reader:
            data.append(obj)
    return data

def load_all_data(data_dir):
    """
    Load multiple JSON and JSONL files from a specified directory.

    This function loads various data files including brand indices, 
    product information, reviews, and synonyms.

    Args:
        data_dir (str): Path to the directory containing data files.

    Returns:
        dict: A dictionary where keys are dataset names and values are the loaded data.
    """
    return {
        "brand_index": load_json(f"{data_dir}/brand_index.json"),
        "description_index": load_json(f"{data_dir}/description_index.json"),
        "domain_index": load_json(f"{data_dir}/domain_index.json"),
        "origin_index": load_json(f"{data_dir}/origin_index.json"),
        "origin_synonyms": load_json(f"{data_dir}/origin_synonyms.json"),
        "products": load_jsonl(f"{data_dir}/products (1).jsonl"),
        "rearranged_products": load_jsonl(f"{data_dir}/rearranged_products.jsonl"),
        "reviews_index": load_json(f"{data_dir}/reviews_index.json"),
        "title_index": load_json(f"{data_dir}/title_index.json"),
    }

if __name__ == '__main__':
    # Example usage: Load data from the specified directory.
    data_directory = 'data'  # Replace with the actual path to your data directory.
    
    data = load_all_data(data_directory)
    
    print("Data loading successful")
    print(data.keys())  # Print the loaded dataset keys.
    print(f"Number of products: {len(data['products'])}")
    print(f"Number of rearranged products: {len(data['rearranged_products'])}")
