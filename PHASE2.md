# Phase 2: Small-Scale Training

## Overview

Phase 2 trains the model on a small dataset (5-100 samples) to validate the training pipeline before scaling to full data.

**Goal:** Verify training works end-to-end with minimal resources.

## Quick Start

### 1. Activate Environment

```bash
source code-model-env/Scripts/activate  # Linux/Mac
# or
code-model-env\Scripts\activate         # Windows
```

### 2. Run Training

```bash
python scripts/train.py
```

Expected output:
```
============================================================
PHASE 2: SMALL-SCALE TRAINING
============================================================

1. Loading configuration...
   ✓ Config loaded

2. Creating output directories...
   ✓ Directories created

3. Loading data...
   ✓ Loaded 5 samples

4. Cleaning data...
   ✓ Cleaned to 5 valid samples

5. Creating model...
   ✓ Model created: 111.2M parameters

6. Setting up trainer...
   ✓ Trainer ready

7. Starting training...
   (This may take a few minutes on CPU)
   Epoch 1/1 - Avg Loss: 8.2341

============================================================
✅ TRAINING COMPLETE!
============================================================
```

### 3. Check Results

```bash
# View training logs
cat outputs/logs/training.json

# List checkpoints
ls -la outputs/checkpoints/

# List saved models
ls -la outputs/models/
```

## Configuration

Edit `config.yaml` to adjust training:

```yaml
training:
  batch_size: 4          # Smaller = less memory
  learning_rate: 5e-4    # Standard for transformers
  num_epochs: 1          # Start with 1 epoch
  num_samples: 100       # Use 100 samples for Phase 2
```

## What's Happening

1. **Data Loading** - Loads Python code samples
2. **Data Cleaning** - Filters low-quality code
3. **Tokenization** - Converts code to tokens
4. **Model Creation** - Initializes 111M parameter model
5. **Training Loop** - Trains on batches with causal language modeling
6. **Checkpointing** - Saves model after each epoch
7. **Logging** - Records loss metrics

## Expected Performance

- **CPU Training Time:** 5-30 minutes (depends on sample count)
- **GPU Training Time:** 1-5 minutes
- **Initial Loss:** 8-10 (high, model is untrained)
- **Final Loss:** 6-8 (should decrease)

## Troubleshooting

### Out of Memory

Reduce batch size in `config.yaml`:
```yaml
training:
  batch_size: 2  # Smaller batches
```

### Training is Very Slow

This is normal on CPU. Options:
1. Use fewer samples: `num_samples: 10`
2. Use GPU (Phase 4)
3. Wait (CPU training is slow but works)

### Model Not Saving

Check that `outputs/` directory exists:
```bash
mkdir -p outputs/checkpoints outputs/logs outputs/models
```

## Next Steps

After Phase 2 completes:

1. **Review Logs** - Check `outputs/logs/training.json` for loss trends
2. **Test Inference** - Run `python scripts/inference.py`
3. **Phase 3** - Prepare full dataset (100K+ samples)
4. **Phase 4** - Cloud GPU training

## Files Generated

```
outputs/
├── checkpoints/
│   └── epoch_1.pt          # Model weights after epoch 1
├── logs/
│   └── training.json       # Training metrics
└── models/
    └── code-model-phase2/  # Final model
```

## Key Metrics

- **Loss** - Should decrease over epochs
- **Throughput** - Samples/second (CPU: 1-5, GPU: 50-200)
- **Memory** - Peak memory usage

## Engineering Notes

- Uses causal language modeling (next token prediction)
- Gradient accumulation not needed for small batches
- No distributed training (single GPU/CPU)
- Checkpoints saved after each epoch
- Logs saved in JSON for easy parsing

## Common Issues

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce batch_size to 2 |
| Training too slow | Use GPU or fewer samples |
| Model not found | Run validation first |
| Import errors | Activate virtual environment |

---

**Status:** Phase 2 - Small-Scale Training
