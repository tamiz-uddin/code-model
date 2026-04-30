# Quick Reference Guide

## Essential Commands

### Setup
```bash
cd code-model
python -m venv code-model-env
source code-model-env/Scripts/activate  # Linux/Mac
pip install -r requirements.txt
```

### Validate
```bash
python scripts/validate_setup.py
```

### Test
```bash
pytest tests/ -v
```

### Train
```bash
python scripts/train.py
```

### Inference
```bash
python scripts/inference.py
```

## File Locations

| File | Purpose |
|------|---------|
| `config.yaml` | All hyperparameters |
| `data/loader.py` | Load datasets |
| `data/cleaner.py` | Filter code |
| `data/tokenizer.py` | Tokenization |
| `models/architecture.py` | Model definition |
| `training/trainer.py` | Training utilities |
| `scripts/train.py` | Training script |
| `scripts/inference.py` | Inference script |
| `outputs/logs/training.json` | Training metrics |
| `outputs/checkpoints/` | Model checkpoints |

## Configuration Quick Edit

```yaml
# Reduce memory usage
training:
  batch_size: 2

# Faster training (smaller model)
model:
  n_layer: 6
  n_embd: 384

# More training
training:
  num_epochs: 3
```

## Common Issues

| Issue | Fix |
|-------|-----|
| ImportError | Activate venv: `source code-model-env/Scripts/activate` |
| Out of Memory | Reduce batch_size in config.yaml |
| Slow Training | Use GPU or reduce model size |
| Tests Fail | Run validation first: `python scripts/validate_setup.py` |

## Key Metrics

- **Loss** - Should decrease over epochs
- **Throughput** - Samples/second
- **Memory** - Peak memory usage

## Project Status

- Phase 1: ✅ Complete
- Phase 2: 🚀 Ready to run
- Phase 3: 📋 Planned
- Phase 4: 📋 Planned
- Phase 5: 📋 Planned
- Phase 6: 📋 Planned

## Next Steps

1. Run training: `python scripts/train.py`
2. Check logs: `cat outputs/logs/training.json`
3. Test inference: `python scripts/inference.py`
4. Move to Phase 3

## Documentation

- `README.md` - Quick start
- `PHASE2.md` - Training guide
- `PROJECT_SUMMARY.md` - Full overview
- `QUICK_REFERENCE.md` - This file

---

**Quick Reference - April 2026**
