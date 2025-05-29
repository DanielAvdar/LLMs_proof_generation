import pytest
import os
import tempfile
import json
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_path = tmp_file.name
    
    yield temp_path
    
    # Clean up after test
    if os.path.exists(temp_path):
        os.remove(temp_path)
    if os.path.exists(temp_path + ".bk"):
        os.remove(temp_path + ".bk")

@pytest.fixture
def sample_json_data():
    """Provide sample JSON data for testing."""
    return {
        "key1": "value1",
        "key2": 123,
        "key3": [1, 2, 3],
        "key4": {
            "nested1": "nested_value",
            "nested2": [4, 5, 6]
        }
    }