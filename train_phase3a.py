#!/usr/bin/env python3
"""
Phase 3A: Foundation Model Training (Optimized for GPU Memory)
Train on JavaScript + Python

Usage:
    python train_phase3a.py
"""

import sys
import torch
import yaml
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer


def main():
    """Train Phase 3A model."""
    print("=" * 70)
    print("PHASE 3A: FOUNDATION MODEL TRAINING (OPTIMIZED)")
    print("=" * 70)

    # Check GPU
    print("\n1. Checking GPU...")
    print(f"   GPU Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    # Load config
    print("\n2. Loading configuration...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Optimize for GPU memory
    config["training"]["batch_size"] = 4  # Reduced from 16
    config["training"]["num_epochs"] = 1
    config["training"]["learning_rate"] = 5e-4

    # Reduce model size for GPU memory
    config["model"]["n_embd"] = 512  # Reduced from 768
    config["model"]["n_layer"] = 8   # Reduced from 12
    config["model"]["n_head"] = 8    # Reduced from 12
    config["model"]["n_positions"] = 1024  # Reduced from 2048

    print(f"   Batch size: {config['training']['batch_size']}")
    print(f"   Learning rate: {config['training']['learning_rate']}")
    print(f"   Model size: {config['model']['n_embd']} emb, {config['model']['n_layer']} layers")

    # Create model
    print("\n3. Creating model...")
    model = CodeModel(config["model"]).get_model()
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   ✓ Model created")
    print(f"   Parameters: {total_params:,}")

    # Create synthetic dataset
    print("\n4. Creating synthetic dataset...")
    code_samples = [
        # JavaScript samples
        "function add(a, b) { return a + b; }",
        "const greet = (name) => `Hello, ${name}!`;",
        "async function fetchData(url) { const res = await fetch(url); return res.json(); }",
        "class Stack { constructor() { this.items = []; } push(item) { this.items.push(item); } }",
        "const map = (arr, fn) => arr.map(fn);",
        "const filter = (arr, fn) => arr.filter(fn);",
        "const reduce = (arr, fn, init) => arr.reduce(fn, init);",
        "function* generator() { yield 1; yield 2; yield 3; }",

        # Python samples
        "def add(a, b):\n    return a + b",
        "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
        "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        return self.items.pop()",
        "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",
        "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
    ]

    # Repeat to get more samples
    code_samples = code_samples * 5  # 80 samples total

    # Convert to dataset format (list of dicts with "content" key)
    samples = [{"content": code} for code in code_samples]

    print(f"   ✓ Created {len(samples)} samples")
    print(f"   Languages: JavaScript (40), Python (40)")

    # Train
    print("\n5. Starting training...")
    print("   This may take 15-30 minutes on GPU...")
    trainer = CodeModelTrainer(model, config, samples)
    trainer.train()

    # Save model
    print("\n6. Saving model...")
    output_dir = Path("outputs/models")
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "foundation-model-v1.pt"
    torch.save(model.state_dict(), model_path)

    file_size = model_path.stat().st_size / 1e6
    print(f"   ✓ Saved to {model_path}")
    print(f"   Size: {file_size:.1f} MB")

    # Summary
    print("\n" + "=" * 70)
    print("✅ PHASE 3A TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nModel: {model_path}")
    print(f"Size: {file_size:.1f} MB")
    print(f"Parameters: {total_params:,}")
    print("\nNext steps:")
    print("1. Download foundation-model-v1.pt")
    print("2. Create Phase 3B notebook")
    print("3. Upload model to Phase 3B")
    print("4. Run Phase 3B training (HTML + CSS)")
    print("\n" + "=" * 70)

    return True


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
