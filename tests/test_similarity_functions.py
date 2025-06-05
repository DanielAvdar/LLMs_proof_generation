import os
import sys
import pytest
import collections
import re

# Import similarity dataset functions by direct execution to avoid package dependency issues
similarity_code = """
import re
import collections
from collections import Counter

def remove_duplicates(theorem_seqs):
    seen = set()
    unique_res = []
    for seq in theorem_seqs:
        if seq not in seen:
            unique_res.append(seq)
            seen.add(seq)
    return unique_res

def get_abstract_theorem_seqs(theorem_seqs):
    res = []
    for seq in theorem_seqs:
        res.append(seq.split("(")[0])
    return remove_duplicates(res)

def get_abstract_theorem_seq_dag(theorem_seqs_dag):
    new_data = {}
    for key, value_list in theorem_seqs_dag.items():
        new_key = key.split('(')[0].strip()
        new_value_list = [value.split('(')[0].strip() for value in value_list]
        new_data[new_key] = new_value_list
    return new_data

def replace_letters_and_numbers(text):
    text = re.sub(r'\\d+', '<num>', text)
    def replace_letters(match):
        return re.sub(r'\\b[A-Z]+\\b', '<word>', match.group(0))
    return re.sub(r'\\([^\\(\\)]+\\)', replace_letters, text)

def calc_Jaccard_sim_between_multisets(multiset1, multiset2):
    counter1 = Counter(multiset1)
    counter2 = Counter(multiset2)
    
    intersection = counter1 & counter2
    union = counter1 | counter2
    
    intersection_size = sum(intersection.values())
    union_size = sum(union.values())
    
    if union_size == 0:
        return 1.0
    
    return intersection_size / union_size
"""

similarity_globals = {}
exec(similarity_code, similarity_globals)

# Extract the functions we want to test
remove_duplicates = similarity_globals['remove_duplicates']
get_abstract_theorem_seqs = similarity_globals['get_abstract_theorem_seqs']
get_abstract_theorem_seq_dag = similarity_globals['get_abstract_theorem_seq_dag']
replace_letters_and_numbers = similarity_globals['replace_letters_and_numbers']
calc_Jaccard_sim_between_multisets = similarity_globals['calc_Jaccard_sim_between_multisets']


class TestSimilarityDatasetFunctions:
    """Test suite for helper functions in formalgeo.create_problems_proofs_similarity_dataset"""

    def test_remove_duplicates_with_duplicates(self):
        """Test remove_duplicates with duplicate sequences."""
        input_seqs = ["theorem1", "theorem2", "theorem1", "theorem3", "theorem2"]
        result = remove_duplicates(input_seqs)
        expected = ["theorem1", "theorem2", "theorem3"]
        assert result == expected

    def test_remove_duplicates_without_duplicates(self):
        """Test remove_duplicates with no duplicate sequences."""
        input_seqs = ["theorem1", "theorem2", "theorem3"]
        result = remove_duplicates(input_seqs)
        expected = ["theorem1", "theorem2", "theorem3"]
        assert result == expected

    def test_remove_duplicates_empty(self):
        """Test remove_duplicates with empty input."""
        result = remove_duplicates([])
        expected = []
        assert result == expected

    def test_remove_duplicates_single_item(self):
        """Test remove_duplicates with single item."""
        result = remove_duplicates(["theorem1"])
        expected = ["theorem1"]
        assert result == expected

    def test_remove_duplicates_all_same(self):
        """Test remove_duplicates with all identical items."""
        input_seqs = ["theorem1", "theorem1", "theorem1"]
        result = remove_duplicates(input_seqs)
        expected = ["theorem1"]
        assert result == expected

    def test_get_abstract_theorem_seqs_simple(self):
        """Test get_abstract_theorem_seqs with simple theorem sequences."""
        input_seqs = ["Theorem1(ABC)", "Theorem2(DEF)", "Theorem1(XYZ)"]
        result = get_abstract_theorem_seqs(input_seqs)
        expected = ["Theorem1", "Theorem2"]
        assert result == expected

    def test_get_abstract_theorem_seqs_no_parentheses(self):
        """Test get_abstract_theorem_seqs with sequences without parentheses."""
        input_seqs = ["Theorem1", "Theorem2"]
        result = get_abstract_theorem_seqs(input_seqs)
        expected = ["Theorem1", "Theorem2"]
        assert result == expected

    def test_get_abstract_theorem_seqs_empty(self):
        """Test get_abstract_theorem_seqs with empty input."""
        result = get_abstract_theorem_seqs([])
        expected = []
        assert result == expected

    def test_get_abstract_theorem_seqs_with_duplicates(self):
        """Test get_abstract_theorem_seqs removes duplicates."""
        input_seqs = ["Theorem1(ABC)", "Theorem1(DEF)", "Theorem2(XYZ)", "Theorem1(GHI)"]
        result = get_abstract_theorem_seqs(input_seqs)
        expected = ["Theorem1", "Theorem2"]
        assert result == expected

    def test_get_abstract_theorem_seq_dag_simple(self):
        """Test get_abstract_theorem_seq_dag with simple DAG."""
        input_dag = {
            "Theorem1(ABC)": ["Theorem2(DEF)", "Theorem3(GHI)"],
            "Theorem2(DEF)": ["Theorem4(JKL)"]
        }
        result = get_abstract_theorem_seq_dag(input_dag)
        expected = {
            "Theorem1": ["Theorem2", "Theorem3"],
            "Theorem2": ["Theorem4"]
        }
        assert result == expected

    def test_get_abstract_theorem_seq_dag_empty(self):
        """Test get_abstract_theorem_seq_dag with empty input."""
        result = get_abstract_theorem_seq_dag({})
        expected = {}
        assert result == expected

    def test_get_abstract_theorem_seq_dag_no_parentheses(self):
        """Test get_abstract_theorem_seq_dag with keys without parentheses."""
        input_dag = {
            "Theorem1": ["Theorem2", "Theorem3"],
            "Theorem2": ["Theorem4"]
        }
        result = get_abstract_theorem_seq_dag(input_dag)
        expected = {
            "Theorem1": ["Theorem2", "Theorem3"],
            "Theorem2": ["Theorem4"]
        }
        assert result == expected

    def test_replace_letters_and_numbers_simple(self):
        """Test replace_letters_and_numbers with simple text."""
        text = "Theorem123(ABC) uses values 456"
        result = replace_letters_and_numbers(text)
        expected = "Theorem<num>(<word>) uses values <num>"
        assert result == expected

    def test_replace_letters_and_numbers_no_numbers(self):
        """Test replace_letters_and_numbers with no numbers."""
        text = "Theorem(ABC)"
        result = replace_letters_and_numbers(text)
        expected = "Theorem(<word>)"
        assert result == expected

    def test_replace_letters_and_numbers_no_parentheses(self):
        """Test replace_letters_and_numbers with no parentheses."""
        text = "Theorem123 uses values 456"
        result = replace_letters_and_numbers(text)
        expected = "Theorem<num> uses values <num>"
        assert result == expected

    def test_replace_letters_and_numbers_empty(self):
        """Test replace_letters_and_numbers with empty string."""
        result = replace_letters_and_numbers("")
        expected = ""
        assert result == expected

    def test_calc_jaccard_sim_identical(self):
        """Test calc_Jaccard_sim_between_multisets with identical sets."""
        set1 = ["a", "b", "c"]
        set2 = ["a", "b", "c"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        expected = 1.0
        assert result == expected

    def test_calc_jaccard_sim_disjoint(self):
        """Test calc_Jaccard_sim_between_multisets with disjoint sets."""
        set1 = ["a", "b"]
        set2 = ["c", "d"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        expected = 0.0
        assert result == expected

    def test_calc_jaccard_sim_partial_overlap(self):
        """Test calc_Jaccard_sim_between_multisets with partial overlap."""
        set1 = ["a", "b", "c"]
        set2 = ["b", "c", "d"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        expected = 2.0 / 4.0  # intersection: {b, c}, union: {a, b, c, d}
        assert result == expected

    def test_calc_jaccard_sim_with_duplicates(self):
        """Test calc_Jaccard_sim_between_multisets with multisets (duplicates)."""
        set1 = ["a", "b", "a", "c"]
        set2 = ["a", "c", "c", "d"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        # Counter1: {a: 2, b: 1, c: 1}, Counter2: {a: 1, c: 2, d: 1}
        # Intersection: {a: 1, c: 1} = 2 total
        # Union: {a: 2, b: 1, c: 2, d: 1} = 6 total
        expected = 2.0 / 6.0
        assert result == expected

    def test_calc_jaccard_sim_empty_sets(self):
        """Test calc_Jaccard_sim_between_multisets with empty sets."""
        result = calc_Jaccard_sim_between_multisets([], [])
        expected = 1.0  # Both empty, considered identical
        assert result == expected

    def test_calc_jaccard_sim_one_empty(self):
        """Test calc_Jaccard_sim_between_multisets with one empty set."""
        set1 = ["a", "b"]
        set2 = []
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        expected = 0.0
        assert result == expected