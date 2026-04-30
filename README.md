# AI Code Model - Phase 1 Setup Complete ✅

## Project Structure

```
code-model/
├── config.yaml              # All hyperparameters
├── requirements.txt         # Dependencies
├── README.md               # This file
│
├── data/
│   ├── loader.py           # Load datasets
│   ├── cleaner.py          # Filter/clean code
│   └── tokenizer.py        # Tokenization
│
├── models/
│   └── architecture.py     # Model definition
│
├── tests/
│   ├── test_data.py        # Data tests
│   ├── test_cleaner.py     # Cleaner tests
│   └── test_model.py       # Model tests
│
├── scripts/
│   └── validate_setup.py   # Validation script
│
└── outputs/
    ├── checkpoints/        # Model checkpoints
    ├── logs/              # Training logs
    └── models/            # Final models
```

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv code-model-env
source code-model-env/bin/activate  # Linux/Mac
# or
code-model-env\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Validate Setup

```bash
python scripts/validate_setup.py
```

You should see:
```
✓ Config loaded successfully
✓ Data loader created test dataset with 5 samples
✓ Data cleaner filtered to 5 valid samples
✓ Model created: 125.3M parameters
✓ Model forward pass successful
✅ All validation checks passed!
```

### 4. Run Tests

```bash
pytest tests/ -v
```

## Configuration

Edit `config.yaml` to adjust:
- Model size (vocab_size, n_embd, n_layer, etc.)
- Training parameters (batch_size, learning_rate, num_epochs)
- Data settings (min/max file size)

## Components

### Data Loader (`data/loader.py`)
- Loads Python code from The Stack v2 dataset
- Falls back to test data if dataset unavailable
- Single responsibility: loading only

### Data Cleaner (`data/cleaner.py`)
- Filters low-quality code
- Removes auto-generated code
- Removes minified code
- Single responsibility: cleaning only

### Tokenizer (`data/tokenizer.py`)
- Byte-level BPE tokenizer
- Trains on code corpus
- Encodes/decodes text
- Single responsibility: tokenization only

### Model (`models/architecture.py`)
- GPT-2 style decoder-only transformer
- 125M parameters (configurable)
- Single responsibility: model definition only

## Next Steps

After validation passes:

1. **Phase 2:** Small-scale training on 10K samples
   - Run: `python scripts/train.py`
   - Expected time: 30-60 minutes on CPU

2. **Phase 3:** Prepare full dataset (100K+ samples)

3. **Phase 4:** Cloud GPU training

4. **Phase 5:** Evaluation and export

5. **Phase 6:** Local deployment

## Engineering Principles

This project follows:
- **YAGNI:** Only what's needed now
- **KISS:** Simple, clear code
- **SOLID:** Single responsibility, dependency injection
- **DRY:** Configuration as source of truth
- **Fail Fast:** Validate early, test continuously

## Troubleshooting

**ImportError: No module named 'torch'**
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

**CUDA not available**
- That's OK! CPU training works, just slower
- For GPU training, use cloud (Phase 4)

**Dataset download fails**
- The script falls back to test data
- For full training, you'll need internet on cloud GPU

## Resources

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PyTorch Docs](https://pytorch.org/docs/)
- [The Stack Dataset](https://huggingface.co/datasets/bigcode/the-stack-v2)

---

**Status:** Phase 1 ✅ Setup & Validation Complete
