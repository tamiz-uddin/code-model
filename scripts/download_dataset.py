"""Download The Stack v2 dataset."""
import sys
from pathlib import Path
from datasets import load_dataset

sys.path.insert(0, str(Path(__file__).parent.parent))


def download_dataset():
    """Download Python code from The Stack v2."""
    print("=" * 60)
    print("PHASE 3: DOWNLOADING THE STACK V2")
    print("=" * 60)

    print("\n1. Loading dataset...")
    print("   Note: Using streaming mode for efficiency")
    print("   This will download samples on-the-fly")

    try:
        # Load dataset with streaming
        dataset = load_dataset(
            "bigcode/the-stack-v2",
            data_dir="data/python",
            split="train",
            streaming=True,
        )
        print("   ✓ Dataset loaded (streaming mode)")

        # Take first 10K samples
        print("\n2. Collecting samples...")
        samples = []
        for idx, sample in enumerate(dataset):
            if idx >= 10000:
                break
            samples.append(sample)
            if (idx + 1) % 1000 == 0:
                print(f"   Collected {idx + 1} samples...")

        print(f"   ✓ Collected {len(samples)} samples")

        # Save locally
        print("\n3. Saving dataset...")
        output_dir = Path("data/the-stack-python")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save as JSON lines
        import json
        output_file = output_dir / "data.jsonl"
        with open(output_file, "w") as f:
            for sample in samples:
                f.write(json.dumps(sample) + "\n")

        print(f"   ✓ Saved to {output_file}")
        print(f"   ✓ File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

        print("\n" + "=" * 60)
        print("✅ DOWNLOAD COMPLETE")
        print("=" * 60)
        print(f"\nDataset ready: {len(samples)} samples")
        print("Next: Run process_dataset.py to clean and filter")

        return True

    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("\nTroubleshooting:")
        print("- Check internet connection")
        print("- Ensure huggingface_hub is installed: pip install huggingface-hub")
        print("- Try again in a few moments")
        return False


if __name__ == "__main__":
    success = download_dataset()
    sys.exit(0 if success else 1)
