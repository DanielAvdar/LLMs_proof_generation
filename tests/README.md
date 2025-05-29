# Test Suite Documentation

This directory contains tests for the `LLMs_proof_generation` repository.

## Overview

The test suite provides basic coverage of key functionality in the repository, focusing on:

1. **Utility Functions**: Testing basic I/O operations, mathematical utilities, and user interactions
2. **Parsing Functions**: Testing the parsing capabilities for geometric predicates and expressions
3. **Core Operations**: Testing fundamental data structures and operations used throughout the codebase

## Test Structure

- `test_direct.py` - Tests for utility functions like JSON loading/saving and mathematical operations
- `test_parsing.py` - Tests for parsing functionality for geometric predicates and expressions
- `test_core.py` - Tests for core data structures and operations (sets, dictionaries)
- `conftest.py` - Common fixtures for use across tests

## Running Tests

From the root directory:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run tests for specific module
pytest tests/test_direct.py

# Generate coverage report
pytest --cov=src
```

## Coverage and Limitations

Current test coverage is intentionally minimal to provide a foundation for future expansion.

### Limitations

1. **Test Isolation**: Tests are standalone and don't interact with the main codebase directly to avoid dependency issues with the `formalgeo` package.
2. **Limited Coverage**: Tests focus on foundational functionality rather than complex geometric reasoning or proofs.
3. **No Integration Tests**: Current tests are unit tests only; integration testing would be a future enhancement.

### Future Improvements

1. Expand test coverage to include more components of the codebase
2. Add integration tests for end-to-end proof generation workflows
3. Implement property-based testing for mathematical operations and parsers