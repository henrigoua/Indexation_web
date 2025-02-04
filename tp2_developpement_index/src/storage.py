import json
import os

def save_index(index, filename):
    """
    Saves an index as a JSON file.

    Args:
        index (dict): The index dictionary to save.
        filename (str): File path where the index will be saved.

    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    if not index:
        print(f"Warning: Attempted to save an empty index to {filename}. Skipping.")
        return False

    try:
        # Assurer que le répertoire cible existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Sauvegarder en JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=4, ensure_ascii=False)

        print(f"Index successfully saved to {filename} ({len(index)} words).")
        return True

    except (OSError, IOError) as e:
        print(f"Error: Unable to save index to {filename}. OS error: {e}")
    except TypeError as e:
        print(f"Error: Data format issue while saving {filename}: {e}")
    except Exception as e:
        print(f"Unexpected error while saving {filename}: {e}")

    return False

def load_index(filename):
    """
    Loads an index from a JSON file.

    Args:
        filename (str): File path of the index.

    Returns:
        dict: The loaded index, or an empty dictionary if an error occurs.
    """
    if not os.path.exists(filename):
        print(f"Warning: File {filename} not found. Returning an empty index.")
        return {}

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                print(f"Error: {filename} does not contain a valid dictionary.")
                return {}
            return data

    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted or not a valid JSON file.")
    except (OSError, IOError) as e:
        print(f"Error: Unable to read file {filename}. OS error: {e}")
    except Exception as e:
        print(f"Unexpected error while loading {filename}: {e}")

    return {}
