"""Create synthetic dataset for Phase 3 testing."""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def create_synthetic_dataset():
    """Create synthetic Python code dataset."""
    print("=" * 60)
    print("PHASE 3: CREATING SYNTHETIC DATASET")
    print("=" * 60)

    print("\n1. Generating synthetic code samples...")

    # Synthetic Python code samples
    code_samples = [
        # Functions
        "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
        "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
        "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",
        "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",

        # Classes
        "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0",
        "class Queue:\n    def __init__(self):\n        self.items = []\n    def enqueue(self, item):\n        self.items.insert(0, item)\n    def dequeue(self):\n        return self.items.pop()\n    def is_empty(self):\n        return len(self.items) == 0",
        "class LinkedList:\n    def __init__(self):\n        self.head = None\n    def append(self, data):\n        if not self.head:\n            self.head = Node(data)\n        else:\n            current = self.head\n            while current.next:\n                current = current.next\n            current.next = Node(data)",
        "class BinaryTree:\n    def __init__(self, value):\n        self.value = value\n        self.left = None\n        self.right = None\n    def insert(self, value):\n        if value < self.value:\n            if self.left is None:\n                self.left = BinaryTree(value)\n            else:\n                self.left.insert(value)\n        else:\n            if self.right is None:\n                self.right = BinaryTree(value)\n            else:\n                self.right.insert(value)",
        "class Graph:\n    def __init__(self):\n        self.graph = {}\n    def add_edge(self, u, v):\n        if u not in self.graph:\n            self.graph[u] = []\n        self.graph[u].append(v)\n    def dfs(self, node, visited=None):\n        if visited is None:\n            visited = set()\n        visited.add(node)\n        for neighbor in self.graph.get(node, []):\n            if neighbor not in visited:\n                self.dfs(neighbor, visited)\n        return visited",

        # Data processing
        "import pandas as pd\ndef load_data(filepath):\n    df = pd.read_csv(filepath)\n    return df\ndef clean_data(df):\n    df = df.dropna()\n    df = df.drop_duplicates()\n    return df",
        "import numpy as np\ndef calculate_statistics(data):\n    mean = np.mean(data)\n    std = np.std(data)\n    median = np.median(data)\n    return {'mean': mean, 'std': std, 'median': median}",
        "def normalize_data(data):\n    min_val = min(data)\n    max_val = max(data)\n    return [(x - min_val) / (max_val - min_val) for x in data]",

        # Web/API
        "import requests\ndef fetch_data(url):\n    response = requests.get(url)\n    if response.status_code == 200:\n        return response.json()\n    else:\n        return None",
        "from flask import Flask, jsonify\napp = Flask(__name__)\n@app.route('/api/data')\ndef get_data():\n    data = {'message': 'Hello, World!'}\n    return jsonify(data)",

        # File operations
        "def read_file(filepath):\n    with open(filepath, 'r') as f:\n        content = f.read()\n    return content\ndef write_file(filepath, content):\n    with open(filepath, 'w') as f:\n        f.write(content)",

        # String operations
        "def reverse_string(s):\n    return s[::-1]\ndef is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]\ndef count_vowels(s):\n    vowels = 'aeiouAEIOU'\n    return sum(1 for c in s if c in vowels)",

        # List operations
        "def remove_duplicates(lst):\n    return list(set(lst))\ndef flatten_list(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten_list(item))\n        else:\n            result.append(item)\n    return result",

        # Dictionary operations
        "def merge_dicts(d1, d2):\n    result = d1.copy()\n    result.update(d2)\n    return result\ndef invert_dict(d):\n    return {v: k for k, v in d.items()}",

        # Decorators
        "def timer(func):\n    import time\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        end = time.time()\n        print(f'Execution time: {end - start}')\n        return result\n    return wrapper",

        # Context managers
        "class FileManager:\n    def __init__(self, filename, mode):\n        self.filename = filename\n        self.mode = mode\n        self.file = None\n    def __enter__(self):\n        self.file = open(self.filename, self.mode)\n        return self.file\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if self.file:\n            self.file.close()",

        # Generators
        "def fibonacci_generator(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b",

        # List comprehensions
        "squares = [x**2 for x in range(10)]\neven_squares = [x**2 for x in range(10) if x % 2 == 0]\nmatrix = [[i*j for j in range(3)] for i in range(3)]",

        # Lambda functions
        "add = lambda x, y: x + y\nmultiply = lambda x, y: x * y\nsquare = lambda x: x**2",

        # Exception handling
        "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nfinally:\n    print('Cleanup')",

        # Type hints
        "def add_numbers(a: int, b: int) -> int:\n    return a + b\ndef process_data(data: list) -> dict:\n    return {'count': len(data), 'sum': sum(data)}",

        # Async/await
        "import asyncio\nasync def fetch_data(url):\n    await asyncio.sleep(1)\n    return {'data': 'example'}\nasync def main():\n    result = await fetch_data('http://example.com')\n    print(result)",

        # Testing
        "import unittest\nclass TestMath(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(2 + 2, 4)\n    def test_subtract(self):\n        self.assertEqual(5 - 3, 2)",

        # Logging
        "import logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\nlogger.info('Application started')\nlogger.error('An error occurred')",

        # Configuration
        "import configparser\nconfig = configparser.ConfigParser()\nconfig.read('config.ini')\ndb_host = config.get('database', 'host')\ndb_port = config.getint('database', 'port')",
    ]

    # Create output directory
    output_dir = Path("data/the-stack-python")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as JSONL
    output_file = output_dir / "data.jsonl"
    with open(output_file, "w") as f:
        for code in code_samples:
            f.write(json.dumps({"content": code}) + "\n")

    print(f"   ✓ Generated {len(code_samples)} samples")
    print(f"   ✓ Saved to {output_file}")

    print("\n" + "=" * 60)
    print("✅ SYNTHETIC DATASET CREATED")
    print("=" * 60)
    print(f"\nDataset ready: {len(code_samples)} samples")
    print("Next: Run process_dataset.py to clean and filter")

    return True


if __name__ == "__main__":
    success = create_synthetic_dataset()
    sys.exit(0 if success else 1)
