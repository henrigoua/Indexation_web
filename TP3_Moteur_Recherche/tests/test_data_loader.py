import pytest
from utils.data_loader import load_all_data

def test_load_all_data_valid():
    """
    Test the `load_all_data` function with a valid data directory.

    - Calls `load_all_data` with a valid directory name.
    - Ensures that the returned data is a dictionary.
    """
    data = load_all_data("data")
    assert isinstance(data, dict), "The loaded data must be a dictionary."

def test_load_all_data_missing():
    """
    Test the `load_all_data` function when the directory does not exist.

    - Calls `load_all_data` with a non-existing directory.
    - Expects a `FileNotFoundError` to be raised.
    """
    with pytest.raises(FileNotFoundError):
        load_all_data("missing_folder")
