"""Benchmark data pipeline."""
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def benchmark():
    """Benchmark data loading."""
    print("=" * 60)
    print("PHASE 3: BENCHMARKING DATA PIPELINE")
    print("=" * 60)

    print("\n1. Loading dataset...")
    input_file = Path("data/processed/data.jsonl")

    if not input_file.exists():
        print(f"   ✗ Dataset not found at {input_file}")
        print("   Run process_dataset.py first")
        return False

    start = time.time()
    samples = []
    with open(input_file) as f:
        for line in f:
            samples.append(json.loads(line))
    load_time = time.time() - start

    print(f"   ✓ Loaded in {load_time:.2f}s")

    print("\n2. Computing statistics...")
    num_samples = len(samples)
    throughput = num_samples / load_time if load_time > 0 else 0

    # Compute content statistics
    total_chars = sum(len(s.get("content", "")) for s in samples)
    avg_chars = total_chars / num_samples if num_samples > 0 else 0

    print(f"   Samples: {num_samples:,}")
    print(f"   Load time: {load_time:.2f}s")
    print(f"   Throughput: {throughput:,.0f} samples/sec")
    print(f"   Total chars: {total_chars:,}")
    print(f"   Avg chars/sample: {avg_chars:,.0f}")

    print("\n3. File statistics...")
    file_size_mb = input_file.stat().st_size / 1024 / 1024
    print(f"   File size: {file_size_mb:.1f} MB")
    print(f"   Avg size/sample: {file_size_mb * 1024 / num_samples:.1f} KB")

    print("\n" + "=" * 60)
    print("✅ BENCHMARK COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = benchmark()
    sys.exit(0 if success else 1)
