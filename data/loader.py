"""Data loader for code datasets."""
from datasets import load_dataset


class CodeDataLoader:
    """Load Python code from The Stack v2 dataset."""

    def __init__(self, config):
        self.config = config

    def load_python_code(self, num_samples=1000):
        """Load Python code from The Stack.

        Args:
            num_samples: Number of samples to load

        Returns:
            Dataset with code samples
        """
        try:
            dataset = load_dataset(
                "bigcode/the-stack-v2",
                data_dir="data/python",
                split="train",
                streaming=True
            )
            return dataset.take(num_samples)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            print("Falling back to local test data...")
            return self._create_test_dataset()

    def _create_test_dataset(self):
        """Create a small test dataset for validation."""
        test_data = {
            "content": [
                """def fibonacci(n):
    \"\"\"Calculate fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
""",
                """class DataProcessor:
    \"\"\"Process and clean data.\"\"\"

    def __init__(self, data):
        self.data = data
        self.processed = None

    def clean(self):
        \"\"\"Remove null values.\"\"\"
        self.processed = [x for x in self.data if x is not None]
        return self.processed

    def transform(self):
        \"\"\"Apply transformations.\"\"\"
        return [x * 2 for x in self.processed]

    def get_stats(self):
        \"\"\"Calculate statistics.\"\"\"
        return {
            'mean': sum(self.processed) / len(self.processed),
            'max': max(self.processed),
            'min': min(self.processed)
        }
""",
                """import numpy as np
import pandas as pd

def load_data(filepath):
    \"\"\"Load data from CSV file.\"\"\"
    df = pd.read_csv(filepath)
    return df

def preprocess(df):
    \"\"\"Preprocess dataframe.\"\"\"
    df = df.dropna()
    df['normalized'] = (df['value'] - df['value'].mean()) / df['value'].std()
    return df

def analyze(df):
    \"\"\"Analyze data.\"\"\"
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing': df.isnull().sum().to_dict()
    }
""",
                """def quicksort(arr):
    \"\"\"Sort array using quicksort algorithm.\"\"\"
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)

def test_quicksort():
    \"\"\"Test quicksort implementation.\"\"\"
    test_cases = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        [1],
        [],
        [5, 5, 5, 5]
    ]

    for test in test_cases:
        result = quicksort(test)
        expected = sorted(test)
        assert result == expected, f"Failed: {test}"

    print("All tests passed!")
""",
                """class BinarySearchTree:
    \"\"\"Binary search tree implementation.\"\"\"

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        \"\"\"Insert value into tree.\"\"\"
        if value < self.value:
            if self.left is None:
                self.left = BinarySearchTree(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BinarySearchTree(value)
            else:
                self.right.insert(value)

    def search(self, value):
        \"\"\"Search for value in tree.\"\"\"
        if value == self.value:
            return True
        elif value < self.value:
            return self.left.search(value) if self.left else False
        else:
            return self.right.search(value) if self.right else False

    def inorder(self):
        \"\"\"Inorder traversal.\"\"\"
        result = []
        if self.left:
            result.extend(self.left.inorder())
        result.append(self.value)
        if self.right:
            result.extend(self.right.inorder())
        return result
""",
            ]
        }
        from datasets import Dataset
        return Dataset.from_dict(test_data)
