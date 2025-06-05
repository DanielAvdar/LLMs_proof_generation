import os
import sys
import pytest

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Try to import the actual parsing module for coverage
try:
    from formalgeo.parse.basic import parse_geo_predicate, parse_equal_predicate, parse_equal_to_tree
    PARSE_AVAILABLE = True
except ImportError:
    # Fall back to direct execution
    basic_parse_path = os.path.join(os.path.dirname(__file__), '../src/formalgeo/parse/basic.py')
    parse_globals = {}
    with open(basic_parse_path, 'r') as f:
        exec(f.read(), parse_globals)
    
    parse_geo_predicate = parse_globals['parse_geo_predicate']
    parse_equal_predicate = parse_globals['parse_equal_predicate']
    parse_equal_to_tree = parse_globals['parse_equal_to_tree']
    PARSE_AVAILABLE = False


@pytest.mark.skipif(not PARSE_AVAILABLE, reason="Module import failed due to dependencies")
class TestParsingForCoverage:
    """Test actual formalgeo.parse.basic module for coverage analysis"""

    def test_parse_geo_predicate_for_coverage(self):
        """Test parse_geo_predicate for coverage."""
        result = parse_geo_predicate('Predicate(ABC)')
        expected = ('Predicate', ['A', 'B', 'C'], [3])
        assert result == expected

    def test_parse_geo_predicate_with_vars_for_coverage(self):
        """Test parse_geo_predicate with make_vars for coverage."""
        result = parse_geo_predicate('Triangle(ABC)', make_vars=True)
        expected = ('Triangle', ['a', 'b', 'c'], [3])
        assert result == expected

    def test_parse_equal_predicate_for_coverage(self):
        """Test parse_equal_predicate for coverage."""
        result = parse_equal_predicate('Equal(LengthOfLine(AB),LengthOfLine(CD))')
        tree, attrs = result
        expected_tree = ('Equal', (('LengthOfLine', ('A', 'B')), ('LengthOfLine', ('C', 'D'))))
        assert tree == expected_tree

    def test_parse_equal_to_tree_for_coverage(self):
        """Test parse_equal_to_tree for coverage."""
        result = parse_equal_to_tree('LengthOfLine(AB)')
        tree, attrs = result
        expected_tree = ('LengthOfLine', ('A', 'B'))
        assert tree == expected_tree

    def test_parse_error_handling_for_coverage(self):
        """Test error handling in parsing for coverage."""
        with pytest.raises(Exception):
            parse_equal_predicate('Equal(LengthOfLine(AB,LengthOfLine(CD))')


class TestParsingFallback:
    """Fallback tests that use exec'd functions"""

    def test_parse_geo_predicate_fallback(self):
        """Test parse_geo_predicate fallback."""
        result = parse_geo_predicate('Predicate(ABC)')
        expected = ('Predicate', ['A', 'B', 'C'], [3])
        assert result == expected

    def test_parse_equal_predicate_fallback(self):
        """Test parse_equal_predicate fallback."""
        result = parse_equal_predicate('Equal(LengthOfLine(AB),LengthOfLine(CD))')
        tree, attrs = result
        expected_tree = ('Equal', (('LengthOfLine', ('A', 'B')), ('LengthOfLine', ('C', 'D'))))
        assert tree == expected_tree