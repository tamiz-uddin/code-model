# Training Scripts - Phase 3A-3D

## Overview

Four standalone Python scripts for training each phase:

1. **train_phase3a.py** - Foundation (JS + Python)
2. **train_phase3b.py** - Frontend (HTML + CSS)
3. **train_phase3c.py** - Full-Stack (Frameworks)
4. **train_phase3d.py** - Extended Languages (TypeScript, Java, Go, Rust, C#, SQL)

---

## Usage

### Phase 3A: Foundation Training

```bash
# Local machine
python train_phase3a.py

# Google Colab
!python train_phase3a.py
```

**Output:** `outputs/models/foundation-model-v1.pt`

### Phase 3B: Frontend Fine-tuning

```bash
# Local machine
python train_phase3b.py

# Google Colab
!python train_phase3b.py
```

**Output:** `outputs/models/frontend-model-v1.pt`

### Phase 3C: Full-Stack Fine-tuning

```bash
# Local machine
python train_phase3c.py

# Google Colab
!python train_phase3c.py
```

**Output:** `outputs/models/fullstack-model-v1.pt`

### Phase 3D: Extended Languages Fine-tuning

```bash
# Local machine
python train_phase3d.py

# Google Colab
!python train_phase3d.py
```

**Output:** `outputs/models/universal-model-v1.pt`

---

## Google Colab Setup

### Step 1: Clone Repository
```python
!git clone https://github.com/YOUR_USERNAME/code-model.git
%cd code-model
!pip install -q torch transformers datasets tokenizers accelerate pyyaml
```

### Step 2: Run Training Script
```python
!python train_phase3a.py
```

### Step 3: Download Model
```python
from google.colab import files
files.download("outputs/models/foundation-model-v1.pt")
```

---

## Script Features

### Automatic GPU Detection
```python
print(f"GPU Available: {torch.cuda.is_available()}")
print(f"GPU Name: {torch.cuda.get_device_name(0)}")
```

### Config Loading
- Loads `config.yaml` if available
- Falls back to defaults if not found
- Optimizes settings for training

### Dataset Creation
- Creates synthetic dataset for each phase
- Repeats samples to reach target size
- Includes code samples from multiple languages

### Model Training
- Loads previous checkpoint for fine-tuning
- Trains with optimized hyperparameters
- Saves model to `outputs/models/`

### Error Handling
- Catches and reports errors
- Provides helpful error messages
- Graceful interruption handling

---

## Expected Output

### Phase 3A
```
======================================================================
PHASE 3A: FOUNDATION MODEL TRAINING
======================================================================

1. Checking GPU...
   GPU Available: True
   GPU Name: NVIDIA Tesla T4
   GPU Memory: 16.0 GB

2. Loading configuration...
   Batch size: 16
   Learning rate: 0.0005
   Epochs: 1

3. Creating model...
   ✓ Model created
   Parameters: 111,200,000

4. Creating synthetic dataset...
   ✓ Created 80 samples
   Languages: JavaScript (40), Python (40)

5. Starting training...
   This may take 30-60 minutes on GPU...
   Epoch 1/1
   Loss: 8.234 → 7.891 → ... → 2.123

6. Saving model...
   ✓ Saved to outputs/models/foundation-model-v1.pt
   Size: 445.2 MB

======================================================================
✅ PHASE 3A TRAINING COMPLETE
======================================================================

Model: outputs/models/foundation-model-v1.pt
Size: 445.2 MB
Parameters: 111,200,000

Next steps:
1. Download foundation-model-v1.pt
2. Create Phase 3B notebook
3. Upload model to Phase 3B
4. Run Phase 3B training (HTML + CSS)
```

---

## Training Timeline

| Phase | Script | Time | Output |
|-------|--------|------|--------|
| 3A | train_phase3a.py | 30-60 min | foundation-model-v1.pt |
| 3B | train_phase3b.py | 30-45 min | frontend-model-v1.pt |
| 3C | train_phase3c.py | 30-45 min | fullstack-model-v1.pt |
| 3D | train_phase3d.py | 1-2 hours | universal-model-v1.pt |

**Total: 2-4 hours on GPU**

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'models'"
Make sure you're in the correct directory:
```bash
cd code-model
python train_phase3a.py
```

### "CUDA out of memory"
The scripts automatically use batch size 16. If still out of memory:
1. Edit the script
2. Change `config["training"]["batch_size"] = 8`
3. Run again

### "Model not found"
For Phase 3B, 3C, 3D:
- Make sure Phase 3A, 3B, 3C completed successfully
- Check that model files exist in `outputs/models/`
- Run previous phases first

### "GPU not available"
- Check GPU is available: `nvidia-smi`
- In Colab: Runtime → Change runtime type → GPU (T4)
- Scripts will fall back to CPU (slower)

---

## File Structure

```
code-model/
├── train_phase3a.py
├── train_phase3b.py
├── train_phase3c.py
├── train_phase3d.py
├── config.yaml
├── models/
│   └── architecture.py
├── training/
│   └── trainer.py
├── outputs/
│   └── models/
│       ├── foundation-model-v1.pt
│       ├── frontend-model-v1.pt
│       ├── fullstack-model-v1.pt
│       └── universal-model-v1.pt
└── TRAINING_SCRIPTS.md
```

---

## Advanced Usage

### Custom Model Path
```bash
python train_phase3b.py --model custom/path/to/model.pt
```

### Batch Processing
```bash
# Run all phases sequentially
python train_phase3a.py && python train_phase3b.py && python train_phase3c.py && python train_phase3d.py
```

### Monitor Training
```bash
# In another terminal
watch -n 1 nvidia-smi
```

---

## Next Steps

1. **Phase 3A:** Run `python train_phase3a.py`
2. **Phase 3B:** Run `python train_phase3b.py`
3. **Phase 3C:** Run `python train_phase3c.py`
4. **Phase 3D:** Run `python train_phase3d.py`
5. **Phase 4:** Evaluation and deployment

---

**Ready to train? Run `python train_phase3a.py` to start! 🚀**
