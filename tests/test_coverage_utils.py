import os
import sys
import pytest
import tempfile
import json

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now try to actually import and test the real modules to get coverage data
try:
    # For coverage purposes, try to import the actual modules
    from formalgeo.tools.utils import (
        load_json, save_json, safe_save_json, debug_print, 
        rough_equal, get_user_input
    )
    UTILS_AVAILABLE = True
except ImportError:
    # Fall back to direct execution for functionality
    utils_path = os.path.join(os.path.dirname(__file__), '../src/formalgeo/tools/utils.py')
    utils_globals = {}
    with open(utils_path, 'r') as f:
        exec(f.read(), utils_globals)
    
    load_json = utils_globals['load_json']
    save_json = utils_globals['save_json']
    safe_save_json = utils_globals['safe_save_json']
    debug_print = utils_globals['debug_print']
    rough_equal = utils_globals['rough_equal']
    get_user_input = utils_globals['get_user_input']
    UTILS_AVAILABLE = False


@pytest.mark.skipif(not UTILS_AVAILABLE, reason="Module import failed due to dependencies")
class TestUtilsForCoverage:
    """Test actual formalgeo.tools.utils module for coverage analysis"""

    def test_load_json_for_coverage(self, temp_json_file, sample_json_data):
        """Test load_json for coverage."""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_json_data, f)
        
        result = load_json(temp_json_file)
        assert result == sample_json_data

    def test_save_json_for_coverage(self, temp_json_file, sample_json_data):
        """Test save_json for coverage."""
        save_json(sample_json_data, temp_json_file)
        
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data

    def test_safe_save_json_for_coverage(self, temp_json_file, sample_json_data):
        """Test safe_save_json for coverage."""
        safe_save_json(sample_json_data, temp_json_file)
        
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data

    def test_debug_print_for_coverage(self, capsys):
        """Test debug_print for coverage."""
        debug_print(True, "test message")
        captured = capsys.readouterr()
        assert "test message" in captured.out

    def test_rough_equal_for_coverage(self):
        """Test rough_equal for coverage."""
        assert rough_equal(1.0, 1.0) is True
        assert rough_equal(1.0, 2.0) is False

    def test_get_user_input_for_coverage(self, monkeypatch):
        """Test get_user_input for coverage."""
        monkeypatch.setattr('builtins.input', lambda x: 'y')
        result = get_user_input("Test question")
        assert result == 'y'


# Fallback tests that will always run
class TestUtilsFallback:
    """Fallback tests that use exec'd functions"""

    def test_load_json_fallback(self, temp_json_file, sample_json_data):
        """Test load_json fallback for coverage."""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_json_data, f)
        
        result = load_json(temp_json_file)
        assert result == sample_json_data

    def test_save_json_fallback(self, temp_json_file, sample_json_data):
        """Test save_json fallback for coverage."""
        save_json(sample_json_data, temp_json_file)
        
        assert os.path.exists(temp_json_file)
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == sample_json_data