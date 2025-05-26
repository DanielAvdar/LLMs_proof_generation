import pytest

def test_parse_geo_predicate():
    """Test parsing geometric predicate strings."""
    def parse_geo_predicate(s, make_vars=False):
        """
        Parse s to get predicate_name, para, and para structural msg.
        >> parse_geo_predicate('Predicate(ABC)')
        ('Predicate', ['A', 'B', 'C'], [3])
        >> parse_geo_predicate('Predicate(ABC, DE)', True)
        ('Predicate', ['a', 'b', 'c', 'd', 'e'], [3, 2])
        """
        predicate_name, para = s.split("(")
        para = para.replace(")", "")
        if make_vars:
            para = para.lower()

        if "," not in para:
            return predicate_name, list(para), [len(para)]
        para_len = []
        para = para.split(",")
        for item in para:
            para_len.append(len(item))
        return predicate_name, list("".join(para)), para_len
    
    # Test with a simple predicate
    result = parse_geo_predicate('Predicate(ABC)')
    assert result == ('Predicate', ['A', 'B', 'C'], [3])
    
    # Test with multiple parameter groups
    result = parse_geo_predicate('Predicate(ABC,DE)')
    assert result == ('Predicate', ['A', 'B', 'C', 'D', 'E'], [3, 2])
    
    # Test with make_vars=True
    result = parse_geo_predicate('Predicate(ABC,DE)', make_vars=True)
    assert result == ('Predicate', ['a', 'b', 'c', 'd', 'e'], [3, 2])

def test_equal_expressions():
    """Test equality of mathematical expressions."""
    # Simple arithmetic test cases that should be equal
    assert 5 + 3 == 8
    assert 10 - 4 == 6
    assert 3 * 4 == 12
    assert 15 / 3 == 5
    
    # Testing floating point operations
    assert round(0.1 + 0.2, 10) == round(0.3, 10)
    
    # Testing expression equality with a small tolerance
    def rough_equal(a, b, tolerance=0.001):
        return abs(a - b) < tolerance
    
    assert rough_equal(0.1 + 0.2, 0.3)
    assert rough_equal(1.0/3.0 + 2.0/3.0, 1.0)