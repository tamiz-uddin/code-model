"""Tests for data loading and cleaning."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.cleaner import CodeCleaner
from data.loader import CodeDataLoader


def test_code_cleaner_valid_code():
    """Test that valid code passes."""
    config = {"min_file_size": 100, "max_file_size": 100000}
    cleaner = CodeCleaner(config)

    valid_code = """def fibonacci(n):
    \"\"\"Calculate fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
"""
    assert cleaner.is_valid_code(valid_code)


def test_code_cleaner_too_short():
    """Test that short code is filtered."""
    config = {"min_file_size": 100, "max_file_size": 100000}
    cleaner = CodeCleaner(config)

    short_code = "x = 1"
    assert not cleaner.is_valid_code(short_code)


def test_code_cleaner_auto_generated():
    """Test that auto-generated code is filtered."""
    config = {"min_file_size": 100, "max_file_size": 100000}
    cleaner = CodeCleaner(config)

    auto_gen = "# TODO: auto-generated\n" + "x = 1\n" * 50
    assert not cleaner.is_valid_code(auto_gen)


def test_code_cleaner_too_long():
    """Test that very long code is filtered."""
    config = {"min_file_size": 100, "max_file_size": 1000}
    cleaner = CodeCleaner(config)

    long_code = "x = 1\n" * 500
    assert not cleaner.is_valid_code(long_code)


def test_data_loader_creates_test_data():
    """Test that data loader can create test data."""
    config = {}
    loader = CodeDataLoader(config)
    dataset = loader._create_test_dataset()

    assert len(dataset) > 0
    assert "content" in dataset.column_names


if __name__ == "__main__":
    test_code_cleaner_valid_code()
    test_code_cleaner_too_short()
    test_code_cleaner_auto_generated()
    test_code_cleaner_too_long()
    test_data_loader_creates_test_data()
    print("✓ All data tests passed!")
