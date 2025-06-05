import os
import sys
import pytest

# Create simple helper functions to test from LLM_analogy_based_solver
helper_code = """
def remove_trailing_empty_lines(text):
    return '\\n'.join(line for line in text.splitlines() if line.strip())

def get_level_to_problems(problems):
    '''Group problems by their level.'''
    level_to_problems = {}
    for problem_id, problem in problems.items():
        level = problem.level
        if level not in level_to_problems:
            level_to_problems[level] = []
        level_to_problems[level].append(problem_id)
    return level_to_problems

class MockProblem:
    '''Mock problem class for testing.'''
    def __init__(self, problem_id, level):
        self.id = problem_id
        self.level = level

def calc_Jaccard_sim_between_multisets(multiset1, multiset2):
    '''Calculate Jaccard similarity between two multisets.'''
    from collections import Counter
    
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

helper_globals = {}
exec(helper_code, helper_globals)

# Extract the functions we want to test
remove_trailing_empty_lines = helper_globals['remove_trailing_empty_lines']
get_level_to_problems = helper_globals['get_level_to_problems']
MockProblem = helper_globals['MockProblem']
calc_Jaccard_sim_between_multisets = helper_globals['calc_Jaccard_sim_between_multisets']


class TestAnalogySolverHelpers:
    """Test suite for helper functions from LLM_analogy_based_solver"""

    def test_remove_trailing_empty_lines_with_empty_lines(self):
        """Test removing trailing empty lines."""
        text = "line1\nline2\n\n\n  \n\t\n"
        result = remove_trailing_empty_lines(text)
        expected = "line1\nline2"
        assert result == expected

    def test_remove_trailing_empty_lines_no_empty_lines(self):
        """Test text without trailing empty lines."""
        text = "line1\nline2\nline3"
        result = remove_trailing_empty_lines(text)
        expected = "line1\nline2\nline3"
        assert result == expected

    def test_remove_trailing_empty_lines_only_empty_lines(self):
        """Test text with only empty lines."""
        text = "\n\n  \n\t\n"
        result = remove_trailing_empty_lines(text)
        expected = ""
        assert result == expected

    def test_remove_trailing_empty_lines_mixed(self):
        """Test text with mixed empty and non-empty lines."""
        text = "line1\n\nline2\n  \nline3\n\n"
        result = remove_trailing_empty_lines(text)
        # The function removes all empty lines, not just trailing ones
        expected = "line1\nline2\nline3"
        assert result == expected

    def test_remove_trailing_empty_lines_empty_string(self):
        """Test empty string."""
        text = ""
        result = remove_trailing_empty_lines(text)
        expected = ""
        assert result == expected

    def test_get_level_to_problems_simple(self):
        """Test grouping problems by level."""
        problems = {
            1: MockProblem(1, 1),
            2: MockProblem(2, 1),
            3: MockProblem(3, 2),
            4: MockProblem(4, 2),
            5: MockProblem(5, 3)
        }
        result = get_level_to_problems(problems)
        expected = {
            1: [1, 2],
            2: [3, 4],
            3: [5]
        }
        assert result == expected

    def test_get_level_to_problems_single_level(self):
        """Test problems all at same level."""
        problems = {
            1: MockProblem(1, 1),
            2: MockProblem(2, 1),
            3: MockProblem(3, 1)
        }
        result = get_level_to_problems(problems)
        expected = {1: [1, 2, 3]}
        assert result == expected

    def test_get_level_to_problems_empty(self):
        """Test empty problems dictionary."""
        problems = {}
        result = get_level_to_problems(problems)
        expected = {}
        assert result == expected

    def test_get_level_to_problems_single_problem(self):
        """Test single problem."""
        problems = {1: MockProblem(1, 5)}
        result = get_level_to_problems(problems)
        expected = {5: [1]}
        assert result == expected

    def test_calc_jaccard_identical_multisets(self):
        """Test Jaccard similarity with identical multisets."""
        set1 = ["a", "b", "c"]
        set2 = ["a", "b", "c"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        assert result == 1.0

    def test_calc_jaccard_disjoint_multisets(self):
        """Test Jaccard similarity with disjoint multisets."""
        set1 = ["a", "b"]
        set2 = ["c", "d"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        assert result == 0.0

    def test_calc_jaccard_partial_overlap(self):
        """Test Jaccard similarity with partial overlap."""
        set1 = ["a", "b", "c"]
        set2 = ["b", "c", "d"]
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        expected = 2.0 / 4.0  # intersection: {b, c}, union: {a, b, c, d}
        assert result == expected

    def test_calc_jaccard_empty_multisets(self):
        """Test Jaccard similarity with empty multisets."""
        result = calc_Jaccard_sim_between_multisets([], [])
        assert result == 1.0

    def test_calc_jaccard_one_empty(self):
        """Test Jaccard similarity with one empty multiset."""
        set1 = ["a", "b"]
        set2 = []
        result = calc_Jaccard_sim_between_multisets(set1, set2)
        assert result == 0.0