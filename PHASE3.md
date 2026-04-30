# Phase 3: Full Dataset Preparation

## Overview

Phase 3 prepares the full dataset (100K+ Python code samples) for large-scale training.

**Goals:**
1. Download The Stack v2 dataset
2. Clean and filter code samples
3. Optimize data pipeline
4. Benchmark performance

## Quick Start

### 1. Download Dataset

```bash
python scripts/download_dataset.py
```

### 2. Process Dataset

```bash
python scripts/process_dataset.py
```

### 3. Benchmark Pipeline

```bash
python scripts/benchmark_pipeline.py
```

## Implementation

### Download Script

Create `scripts/download_dataset.py`:

```python
"""Download The Stack v2 dataset."""
from datasets import load_dataset
from pathlib import Path
import os

def download_dataset():
    """Download Python code from The Stack v2."""
    print("=" * 60)
    print("DOWNLOADING THE STACK V2")
    print("=" * 60)
    
    output_dir = Path("data/the-stack-v2")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n1. Loading dataset...")
    try:
        # Load dataset (Python only)
        dataset = load_dataset(
            "bigcode/the-stack-v2",
            data_dir="data/python",
            split="train",
            streaming=False,
            cache_dir="data/cache",
        )
        print(f"   ✓ Loaded {len(dataset)} samples")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n2. Saving dataset...")
    try:
        dataset.save_to_disk(str(output_dir))
        print(f"   ✓ Saved to {output_dir}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ DOWNLOAD COMPLETE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    import sys
    success = download_dataset()
    sys.exit(0 if success else 1)
```

### Process Script

Create `scripts/process_dataset.py`:

```python
"""Process and clean dataset."""
from datasets import load_from_disk
from data.cleaner import CodeCleaner
import yaml
import sys

def process_dataset():
    """Process dataset."""
    print("=" * 60)
    print("PROCESSING DATASET")
    print("=" * 60)
    
    # Load config
    print("\n1. Loading config...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    print("   ✓ Config loaded")
    
    # Load dataset
    print("\n2. Loading dataset...")
    try:
        dataset = load_from_disk("data/the-stack-v2")
        print(f"   ✓ Loaded {len(dataset)} samples")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Clean
    print("\n3. Cleaning dataset...")
    cleaner = CodeCleaner(config["data"])
    dataset = cleaner.clean(dataset)
    print(f"   ✓ Cleaned to {len(dataset)} valid samples")
    
    # Save
    print("\n4. Saving processed dataset...")
    try:
        dataset.save_to_disk("data/processed")
        print(f"   ✓ Saved to data/processed/")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ PROCESSING COMPLETE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = process_dataset()
    sys.exit(0 if success else 1)
```

### Benchmark Script

Create `scripts/benchmark_pipeline.py`:

```python
"""Benchmark data pipeline."""
import time
from datasets import load_from_disk
import sys

def benchmark():
    """Benchmark data loading."""
    print("=" * 60)
    print("BENCHMARKING DATA PIPELINE")
    print("=" * 60)
    
    print("\n1. Loading dataset...")
    start = time.time()
    try:
        dataset = load_from_disk("data/processed")
        load_time = time.time() - start
        print(f"   ✓ Loaded in {load_time:.1f}s")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n2. Computing statistics...")
    num_samples = len(dataset)
    throughput = num_samples / load_time
    
    print(f"   Samples: {num_samples:,}")
    print(f"   Load time: {load_time:.1f}s")
    print(f"   Throughput: {throughput:,.0f} samples/sec")
    
    print("\n" + "=" * 60)
    print("✅ BENCHMARK COMPLETE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = benchmark()
    sys.exit(0 if success else 1)
```

## Configuration

Update `config.yaml`:

```yaml
data:
  min_file_size: 100
  max_file_size: 100000
  min_lines: 5
  max_lines: 1000
  
training:
  batch_size: 32
  learning_rate: 5e-4
  num_epochs: 3
  num_samples: 100000
```

## Expected Results

### Dataset Statistics
- **Total Samples:** 100,000+
- **After Cleaning:** 85,000-90,000
- **Average File Size:** 2-5 KB
- **Average Lines:** 50-100

### Performance
- **Download Time:** 30-60 minutes
- **Processing Time:** 10-20 minutes
- **Storage:** 500 MB - 1 GB
- **Load Time:** 2-5 seconds

## Troubleshooting

### Out of Disk Space
Ensure you have:
- 2 GB for raw dataset
- 1 GB for processed dataset
- 2 GB for model checkpoints

### Slow Download
Use streaming mode:
```python
dataset = load_dataset(
    "bigcode/the-stack-v2",
    streaming=True,
)
```

### Memory Issues
Process in batches:
```python
for batch in dataset.iter(batch_size=1000):
    # Process batch
    pass
```

## Next Steps

1. **Verify Dataset**
   ```bash
   python scripts/verify_dataset.py
   ```

2. **Move to Phase 4**
   - Set up cloud GPU
   - Configure distributed training
   - Start full-scale training

3. **Monitor Training**
   - Track loss metrics
   - Monitor GPU utilization
   - Save checkpoints

---

**Status:** Phase 3 - Full Dataset Preparation
