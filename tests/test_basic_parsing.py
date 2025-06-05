import os
import sys
import pytest

# Import parsing functions by direct execution to avoid package dependency issues
basic_parse_path = os.path.join(os.path.dirname(__file__), '../src/formalgeo/parse/basic.py')
parse_globals = {}
with open(basic_parse_path, 'r') as f:
    exec(f.read(), parse_globals)

# Extract the functions we want to test
parse_geo_predicate = parse_globals['parse_geo_predicate']
parse_equal_predicate = parse_globals['parse_equal_predicate']
parse_equal_to_tree = parse_globals['parse_equal_to_tree']


class TestParsingFunctions:
    """Test suite for parsing functions in formalgeo.parse.basic"""

    def test_parse_geo_predicate_simple(self):
        """Test parsing simple geometric predicates."""
        # Test simple predicate without comma
        result = parse_geo_predicate('Predicate(ABC)')
        expected = ('Predicate', ['A', 'B', 'C'], [3])
        assert result == expected

    def test_parse_geo_predicate_with_comma(self):
        """Test parsing predicates with comma separation."""
        result = parse_geo_predicate('Predicate(ABC,DE)')
        expected = ('Predicate', ['A', 'B', 'C', 'D', 'E'], [3, 2])
        assert result == expected

    def test_parse_geo_predicate_make_vars_false(self):
        """Test parsing with make_vars=False (default)."""
        result = parse_geo_predicate('Triangle(ABC)')
        expected = ('Triangle', ['A', 'B', 'C'], [3])
        assert result == expected

    def test_parse_geo_predicate_make_vars_true(self):
        """Test parsing with make_vars=True (converts to lowercase)."""
        result = parse_geo_predicate('Triangle(ABC)', make_vars=True)
        expected = ('Triangle', ['a', 'b', 'c'], [3])
        assert result == expected

    def test_parse_geo_predicate_complex_with_comma(self):
        """Test parsing complex predicate with multiple comma-separated groups."""
        result = parse_geo_predicate('Relation(AB,CD,EF)', make_vars=True)
        expected = ('Relation', ['a', 'b', 'c', 'd', 'e', 'f'], [2, 2, 2])
        assert result == expected

    def test_parse_equal_predicate_simple(self):
        """Test parsing simple equal predicates."""
        result = parse_equal_predicate('Equal(LengthOfLine(AB),LengthOfLine(CD))')
        expected_tree = ('Equal', (('LengthOfLine', ('A', 'B')), ('LengthOfLine', ('C', 'D'))))
        expected_attrs = [('LengthOfLine', ('A', 'B')), ('LengthOfLine', ('C', 'D'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_equal_predicate_make_vars_true(self):
        """Test parsing equal predicates with make_vars=True."""
        result = parse_equal_predicate('Equal(LengthOfLine(OA),LengthOfLine(OB))', make_vars=True)
        expected_tree = ('Equal', (('LengthOfLine', ('o', 'a')), ('LengthOfLine', ('o', 'b'))))
        expected_attrs = [('LengthOfLine', ('o', 'a')), ('LengthOfLine', ('o', 'b'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_equal_predicate_with_operation(self):
        """Test parsing equal predicates with mathematical operations."""
        result = parse_equal_predicate('Equal(Add(LengthOfLine(OA),x+1),y+2)', make_vars=True)
        expected_tree = ('Equal', (('Add', (('LengthOfLine', ('o', 'a')), 'x+1')), 'y+2'))
        expected_attrs = [('LengthOfLine', ('o', 'a'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_equal_predicate_invalid_parentheses(self):
        """Test that parsing handles invalid parentheses."""
        with pytest.raises(Exception) as exc_info:
            parse_equal_predicate('Equal(LengthOfLine(AB,LengthOfLine(CD))')
        
        assert "Sym stack not empty" in str(exc_info.value)
        assert "Miss ')'" in str(exc_info.value)

    def test_parse_equal_to_tree_simple(self):
        """Test parsing simple expressions to tree."""
        result = parse_equal_to_tree('LengthOfLine(AB)')
        expected_tree = ('LengthOfLine', ('A', 'B'))
        expected_attrs = [('LengthOfLine', ('A', 'B'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_equal_to_tree_make_vars_true(self):
        """Test parsing expressions to tree with make_vars=True."""
        result = parse_equal_to_tree('LengthOfLine(AB)', make_vars=True)
        expected_tree = ('LengthOfLine', ('a', 'b'))
        expected_attrs = [('LengthOfLine', ('a', 'b'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_equal_to_tree_with_operation(self):
        """Test parsing expressions with operations to tree."""
        result = parse_equal_to_tree('Add(LengthOfLine(OA),x+1)', make_vars=True)
        expected_tree = ('Add', (('LengthOfLine', ('o', 'a')), 'x+1'))
        expected_attrs = [('LengthOfLine', ('o', 'a'))]
        
        tree, attrs = result
        assert tree == expected_tree
        assert attrs == expected_attrs

    def test_parse_edge_cases(self):
        """Test edge cases for parsing functions."""
        # Single character predicate
        result = parse_geo_predicate('P(A)')
        expected = ('P', ['A'], [1])
        assert result == expected
        
        # Empty parameter case (should still work)
        result = parse_geo_predicate('Empty()')
        expected = ('Empty', [], [0])
        assert result == expected
        
        # Long parameter string
        result = parse_geo_predicate('LongPredicate(ABCDEFGHIJ)')
        expected = ('LongPredicate', list('ABCDEFGHIJ'), [10])
        assert result == expected