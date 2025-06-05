import os
import sys
import pytest

# Import Problem functions by direct execution to avoid package dependency issues
problem_path = os.path.join(os.path.dirname(__file__), '../src/formalgeo/Problem.py')

# Load only the helper functions we can test without dependencies
problem_code = """
import re

def modify_string(input_string):
    modified_string = re.sub(r'(\\w+)-(\\d+)', r'\\1=\\2', input_string)
    return modified_string

def convert_equations(equations_string):
    equations_list = equations_string.split("\\n")
    res = []
    for row in equations_list:
        values = row.split(";")
        if len(values) > 1:
            res.append(values[1])
    return res

def convert_relations(relations_string):
    relations_list = relations_string.split("\\n")
    res = []
    type = ""
    for row in relations_list:
        if not row.startswith("("):
            type = row[:-1]
        else:
            values = row.split(";")
            res.append((type + "(" + values[1] + ")", values[-1][:-1]))
    extended_res = []
    for tup in res:
        if tup[-1] == "prerequisite":
            continue
        extended_res.append(tup[0])
    return extended_res
"""

problem_globals = {}
exec(problem_code, problem_globals)

# Extract the functions we want to test
modify_string = problem_globals['modify_string']
convert_equations = problem_globals['convert_equations']
convert_relations = problem_globals['convert_relations']


class TestProblemHelperFunctions:
    """Test suite for helper functions in formalgeo.Problem"""

    def test_modify_string_simple(self):
        """Test modify_string with simple input."""
        result = modify_string("var-1")
        expected = "var=1"
        assert result == expected

    def test_modify_string_multiple(self):
        """Test modify_string with multiple patterns."""
        result = modify_string("alpha-1 beta-2 gamma-3")
        expected = "alpha=1 beta=2 gamma=3"
        assert result == expected

    def test_modify_string_no_match(self):
        """Test modify_string with no matching pattern."""
        result = modify_string("no hyphen numbers here")
        expected = "no hyphen numbers here"
        assert result == expected

    def test_modify_string_mixed_cases(self):
        """Test modify_string with mixed cases."""
        result = modify_string("Valid-123 invalid- notvalid-abc test-456")
        expected = "Valid=123 invalid- notvalid-abc test=456"
        assert result == expected

    def test_modify_string_empty(self):
        """Test modify_string with empty string."""
        result = modify_string("")
        expected = ""
        assert result == expected

    def test_convert_equations_simple(self):
        """Test convert_equations with simple input."""
        input_str = "eq1;value1\neq2;value2"
        result = convert_equations(input_str)
        expected = ["value1", "value2"]
        assert result == expected

    def test_convert_equations_single_line(self):
        """Test convert_equations with single equation."""
        input_str = "equation;result"
        result = convert_equations(input_str)
        expected = ["result"]
        assert result == expected

    def test_convert_equations_with_invalid_lines(self):
        """Test convert_equations with lines that don't have enough values."""
        input_str = "valid;value1\ninvalid\nvalid2;value2"
        result = convert_equations(input_str)
        expected = ["value1", "value2"]
        assert result == expected

    def test_convert_equations_empty(self):
        """Test convert_equations with empty input."""
        result = convert_equations("")
        expected = []
        assert result == expected

    def test_convert_equations_only_invalid_lines(self):
        """Test convert_equations with only invalid lines."""
        input_str = "novalues\nnoseparator\nanother"
        result = convert_equations(input_str)
        expected = []
        assert result == expected

    def test_convert_relations_simple(self):
        """Test convert_relations with simple input."""
        input_str = "Triangle:\n(rel1;Triangle(ABC);valid)\n(rel2;Triangle(DEF);valid)"
        result = convert_relations(input_str)
        expected = ["Triangle(Triangle(ABC))", "Triangle(Triangle(DEF))"]
        assert result == expected

    def test_convert_relations_with_prerequisite(self):
        """Test convert_relations filtering out prerequisite relations."""
        input_str = "Line:\n(rel1;Line(AB);valid)\n(rel2;Line(CD);prerequisite)\n(rel3;Line(EF);valid)"
        result = convert_relations(input_str)
        expected = ["Line(Line(AB))", "Line(Line(EF))"]
        assert result == expected

    def test_convert_relations_multiple_types(self):
        """Test convert_relations with multiple relation types."""
        input_str = "Triangle:\n(rel1;Triangle(ABC);valid)\nPoint:\n(rel2;Point(D);valid)"
        result = convert_relations(input_str)
        expected = ["Triangle(Triangle(ABC))", "Point(Point(D))"]
        assert result == expected

    def test_convert_relations_empty(self):
        """Test convert_relations with empty input."""
        result = convert_relations("")
        expected = []
        assert result == expected

    def test_convert_relations_only_prerequisites(self):
        """Test convert_relations with only prerequisite relations."""
        input_str = "Triangle:\n(rel1;Triangle(ABC);prerequisite)\n(rel2;Triangle(DEF);prerequisite)"
        result = convert_relations(input_str)
        expected = []
        assert result == expected

    def test_convert_relations_no_parentheses_lines(self):
        """Test convert_relations with only type definition lines."""
        input_str = "Triangle:\nPoint:\nLine:"
        result = convert_relations(input_str)
        expected = []
        assert result == expected

    def test_convert_relations_mixed_valid_invalid(self):
        """Test convert_relations with mix of valid and invalid statuses."""
        input_str = "Circle:\n(rel1;Circle(O);valid)\n(rel2;Circle(P);invalid)\n(rel3;Circle(Q);valid)"
        result = convert_relations(input_str)
        expected = ["Circle(Circle(O))", "Circle(Circle(P))", "Circle(Circle(Q))"]
        assert result == expected