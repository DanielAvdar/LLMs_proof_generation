import os
import json
import tempfile
import pytest
import sys

# Import utility functions by direct execution to avoid package dependency issues
utils_path = os.path.join(os.path.dirname(__file__), '../src/formalgeo/tools/utils.py')
utils_globals = {}
with open(utils_path, 'r') as f:
    exec(f.read(), utils_globals)

# Extract the functions we want to test
load_json = utils_globals['load_json']
save_json = utils_globals['save_json']
safe_save_json = utils_globals['safe_save_json']
debug_print = utils_globals['debug_print']
rough_equal = utils_globals['rough_equal']
get_user_input = utils_globals['get_user_input']


class TestUtilityFunctions:
    """Test suite for utility functions in formalgeo.tools.utils"""

    def test_load_json_success(self, temp_json_file, sample_json_data):
        """Test successful JSON loading."""
        # Save test data first
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_json_data, f)
        
        # Test loading
        result = load_json(temp_json_file)
        assert result == sample_json_data

    def test_load_json_file_not_found(self):
        """Test loading non-existent file raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            load_json('/non/existent/file.json')

    def test_save_json_success(self, temp_json_file, sample_json_data):
        """Test successful JSON saving."""
        save_json(sample_json_data, temp_json_file)
        
        # Verify file was created and has correct content
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data

    def test_safe_save_json_success(self, temp_json_file, sample_json_data):
        """Test safe JSON saving functionality."""
        safe_save_json(sample_json_data, temp_json_file)
        
        # Verify file was created and has correct content
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data
        
        # Verify backup file was cleaned up
        backup_path = temp_json_file + ".bk"
        assert not os.path.exists(backup_path)

    def test_safe_save_json_overwrites_existing(self, temp_json_file, sample_json_data):
        """Test safe JSON saving overwrites existing files correctly."""
        # Create initial file
        initial_data = {"initial": "data"}
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f)
        
        # Use safe_save_json to overwrite
        safe_save_json(sample_json_data, temp_json_file)
        
        # Verify file was overwritten with new data
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data
        assert result != initial_data

    def test_debug_print_enabled(self, capsys):
        """Test debug_print when debug is True."""
        test_message = "Test debug message"
        debug_print(True, test_message)
        
        captured = capsys.readouterr()
        assert test_message in captured.out

    def test_debug_print_disabled(self, capsys):
        """Test debug_print when debug is False."""
        test_message = "Test debug message"
        debug_print(False, test_message)
        
        captured = capsys.readouterr()
        assert test_message not in captured.out

    def test_rough_equal_true_cases(self):
        """Test rough_equal returns True for values within tolerance."""
        # Exactly equal
        assert rough_equal(1.0, 1.0) is True
        
        # Within tolerance (0.001)
        assert rough_equal(1.0, 1.0009) is True
        assert rough_equal(1.0, 0.9991) is True
        
        # Just under tolerance boundary
        assert rough_equal(1.0, 1.0009) is True
        assert rough_equal(1.0, 0.9991) is True

    def test_rough_equal_false_cases(self):
        """Test rough_equal returns False for values outside tolerance."""
        # Clearly outside tolerance boundary
        assert rough_equal(1.0, 1.002) is False
        assert rough_equal(1.0, 0.998) is False
        
        # Significantly different
        assert rough_equal(1.0, 2.0) is False
        assert rough_equal(0.0, 1.0) is False

    def test_rough_equal_negative_numbers(self):
        """Test rough_equal works correctly with negative numbers."""
        assert rough_equal(-1.0, -1.0009) is True
        assert rough_equal(-1.0, -0.9991) is True
        assert rough_equal(-1.0, -1.002) is False

    def test_get_user_input_default_choices(self, monkeypatch):
        """Test get_user_input with default choices."""
        # Mock user input
        monkeypatch.setattr('builtins.input', lambda x: 'y')
        
        result = get_user_input("Test question")
        assert result == 'y'

    def test_get_user_input_custom_choices(self, monkeypatch):
        """Test get_user_input with custom choices."""
        # Mock user input
        monkeypatch.setattr('builtins.input', lambda x: 'option1')
        
        result = get_user_input("Test question", ["option1", "option2"])
        assert result == 'option1'

    def test_get_user_input_invalid_then_valid(self, monkeypatch):
        """Test get_user_input handles invalid input then valid input."""
        inputs = iter(['invalid', 'y'])
        monkeypatch.setattr('builtins.input', lambda x: next(inputs))
        
        result = get_user_input("Test question")
        assert result == 'y'