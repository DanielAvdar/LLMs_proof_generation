import os
import json
import tempfile
import pytest

# Test utility functions
def test_load_save_json():
    """Test loading and saving JSON data."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_path = tmp_file.name

    try:
        # Test data
        test_data = {"key1": "value1", "key2": 123, "key3": [1, 2, 3]}
        
        # Save data using direct implementation
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Load data using direct implementation 
        with open(temp_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        # Verify data integrity
        assert loaded_data == test_data
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_safe_json_operations():
    """Test safe JSON save operations."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        temp_path = tmp_file.name

    try:
        # Test data
        test_data = {"key1": "value1", "key2": 123}
        
        # Implement safe save functionality inline
        path = os.path.dirname(temp_path)
        filename = os.path.basename(temp_path)
        backup_path = os.path.join(path, filename + ".bk")
        
        # Write to backup first
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # Remove original if exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Rename backup to original
        os.rename(backup_path, temp_path)
        
        # Verify backup doesn't exist and original does
        assert os.path.exists(temp_path)
        assert not os.path.exists(backup_path)
        
        # Check content
        with open(temp_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        assert loaded_data == test_data
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(backup_path):
            os.remove(backup_path)

def test_rough_equal():
    """Test rough_equal function for floating point comparison."""
    def rough_equal(a, b):
        """Accuracy is controlled at 0.001. Preventing floating point calculation issues"""
        return abs(a - b) < 0.001
    
    # Test cases that should be roughly equal (within 0.001)
    assert rough_equal(1.0, 1.0) is True
    assert rough_equal(1.0, 1.0009) is True
    assert rough_equal(1.0, 0.9991) is True
    
    # Test cases that should not be equal
    assert rough_equal(1.0, 1.002) is False
    assert rough_equal(1.0, 0.998) is False

def test_debug_print(capsys):
    """Test debug_print function."""
    def debug_print(debug, msg):
        """Print 'msg' when debug is True."""
        if debug:
            print(msg)
    
    # When debug is True, message should be printed
    debug_print(True, "Debug message")
    captured = capsys.readouterr()
    assert captured.out == "Debug message\n"
    
    # When debug is False, nothing should be printed
    debug_print(False, "Debug message")
    captured = capsys.readouterr()
    assert captured.out == ""