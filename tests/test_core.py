import pytest

def test_set_operations():
    """Test basic set operations similar to what might be used in the engine."""
    # Test set union
    set1 = {1, 2, 3}
    set2 = {3, 4, 5}
    assert set1 | set2 == {1, 2, 3, 4, 5}
    
    # Test set intersection
    assert set1 & set2 == {3}
    
    # Test set difference
    assert set1 - set2 == {1, 2}
    
    # Test subset relationship
    subset = {1, 2}
    assert subset.issubset(set1)
    assert not set1.issubset(subset)
    
    # Test set comprehension
    numbers = [1, 2, 2, 3, 4, 4, 5]
    unique_numbers = set(numbers)
    assert unique_numbers == {1, 2, 3, 4, 5}
    
    # Test converting back to list
    unique_list = list(unique_numbers)
    unique_list.sort()
    assert unique_list == [1, 2, 3, 4, 5]

def test_dict_operations():
    """Test dictionary operations similar to what might be used in the engine."""
    # Create a test dictionary
    sym_to_eqs = {}
    
    # Add items to dictionary
    sym_to_eqs['x'] = ['eq1', 'eq2']
    sym_to_eqs['y'] = ['eq2', 'eq3']
    
    # Test dictionary access
    assert sym_to_eqs['x'] == ['eq1', 'eq2']
    
    # Test checking if key exists
    assert 'x' in sym_to_eqs
    assert 'z' not in sym_to_eqs
    
    # Test dictionary update
    sym_to_eqs['x'].append('eq4')
    assert sym_to_eqs['x'] == ['eq1', 'eq2', 'eq4']
    
    # Test adding a new key
    sym_to_eqs['z'] = ['eq5']
    assert sym_to_eqs['z'] == ['eq5']
    
    # Test getting all keys and values
    keys = set(sym_to_eqs.keys())
    assert keys == {'x', 'y', 'z'}
    
    # Test iterating through dictionary
    all_eqs = []
    for eqs in sym_to_eqs.values():
        all_eqs.extend(eqs)
    
    assert set(all_eqs) == {'eq1', 'eq2', 'eq3', 'eq4', 'eq5'}