"""Process and clean dataset."""
import sys
import json
from pathlib import Path
from data.cleaner import CodeCleaner
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))


def process_dataset():
    """Process dataset."""
    print("=" * 60)
    print("PHASE 3: PROCESSING DATASET")
    print("=" * 60)

    # Load config
    print("\n1. Loading config...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    print("   ✓ Config loaded")

    # Load dataset
    print("\n2. Loading dataset...")
    input_file = Path("data/the-stack-python/data.jsonl")

    if not input_file.exists():
        print(f"   ✗ Dataset not found at {input_file}")
        print("   Run download_dataset.py first")
        return False

    samples = []
    with open(input_file) as f:
        for line in f:
            samples.append(json.loads(line))

    print(f"   ✓ Loaded {len(samples)} samples")

    # Clean
    print("\n3. Cleaning dataset...")
    cleaner = CodeCleaner(config["data"])
    from datasets import Dataset
    dataset = Dataset.from_dict({"content": [s.get("content", "") for s in samples]})
    cleaned = cleaner.clean(dataset)
    print(f"   ✓ Cleaned to {len(cleaned)} valid samples")

    # Save
    print("\n4. Saving processed dataset...")
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "data.jsonl"
    with open(output_file, "w") as f:
        for sample in cleaned:
            f.write(json.dumps({"content": sample["content"]}) + "\n")

    print(f"   ✓ Saved to {output_file}")
    print(f"   ✓ File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

    print("\n" + "=" * 60)
    print("✅ PROCESSING COMPLETE")
    print("=" * 60)
    print(f"\nProcessed dataset: {len(cleaned)} samples")
    print("Next: Run benchmark_pipeline.py to test performance")

    return True


if __name__ == "__main__":
    success = process_dataset()
    sys.exit(0 if success else 1)
