"""Validate that the entire pipeline is set up correctly."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from data.loader import CodeDataLoader
from data.cleaner import CodeCleaner
from models.architecture import CodeModel


def validate():
    """Run validation checks on the entire pipeline."""
    print("=" * 60)
    print("AI Code Model - Setup Validation")
    print("=" * 60)

    # Load config
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        print("✓ Config loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load config: {e}")
        return False

    # Test data loading
    try:
        loader = CodeDataLoader(config["data"])
        dataset = loader._create_test_dataset()
        print(f"✓ Data loader created test dataset with {len(dataset)} samples")
    except Exception as e:
        print(f"✗ Data loader failed: {e}")
        return False

    # Test data cleaning
    try:
        cleaner = CodeCleaner(config["data"])
        cleaned = cleaner.clean(dataset)
        print(f"✓ Data cleaner filtered to {len(cleaned)} valid samples")
    except Exception as e:
        print(f"✗ Data cleaner failed: {e}")
        return False

    # Test model creation
    try:
        model = CodeModel(config["model"])
        params = model.num_parameters_millions()
        print(f"✓ Model created: {params:.1f}M parameters")
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False

    # Test model forward pass
    try:
        import torch

        model_obj = model.get_model()
        input_ids = torch.randint(0, config["model"]["vocab_size"], (2, 512))
        with torch.no_grad():
            output = model_obj(input_ids)
        print(f"✓ Model forward pass successful")
    except Exception as e:
        print(f"✗ Model forward pass failed: {e}")
        return False

    print("=" * 60)
    print("✅ All validation checks passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Create virtual environment: python -m venv code-model-env")
    print("2. Activate it: source code-model-env/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run tests: pytest tests/")
    print("5. Start training: python scripts/train.py")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
