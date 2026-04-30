# Google Colab Setup Guide - Phase 3A Training

## Step 1: Open Google Colab

1. Go to **https://colab.research.google.com**
2. Click **"New notebook"**
3. Rename it: `Phase-3A-Foundation-Training`

---

## Step 2: Change Runtime to GPU

1. Click **Runtime** menu (top right)
2. Select **Change runtime type**
3. Choose:
   - **Runtime type:** Python 3
   - **Hardware accelerator:** GPU (T4)
4. Click **Save**

You should see: `GPU (NVIDIA T4)` in the top right

---

## Step 3: Clone GitHub Repository

Copy this into the first cell and run:

```python
# Clone repository
!git clone https://github.com/YOUR_USERNAME/code-model.git
%cd code-model

# Verify
!ls -la
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 4: Install Dependencies

Copy this into the next cell and run:

```python
# Install dependencies
!pip install -q torch transformers datasets tokenizers accelerate pyyaml

# Verify installation
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

---

## Step 5: Run Phase 3A Training

Copy the entire Phase 3A notebook code into Colab cells and run in order.

### Cell 1: Setup
```python
import os
from google.colab import files

print("=" * 60)
print("PHASE 3A: FOUNDATION MODEL TRAINING")
print("=" * 60)

# Check GPU
import torch
print(f"\n✓ GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✓ GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

### Cell 2: Create Dataset
```python
import json
from pathlib import Path

def create_multilang_dataset():
    """Create synthetic dataset for Phase 3A."""
    print("Creating multi-language synthetic dataset...")
    
    samples = [
        # JavaScript
        "function add(a, b) { return a + b; }",
        "const greet = (name) => `Hello, ${name}!`;",
        "async function fetchData(url) { const res = await fetch(url); return res.json(); }",
        "class Stack { constructor() { this.items = []; } push(item) { this.items.push(item); } }",
        
        # Python
        "def add(a, b):\n    return a + b",
        "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
        "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)",
    ]
    
    # Repeat to get more samples
    samples = samples * 12  # 96 samples
    
    output_dir = Path("data/phase3a/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "data.jsonl"
    with open(output_file, "w") as f:
        for code in samples:
            f.write(json.dumps({"content": code}) + "\n")
    
    print(f"✓ Generated {len(samples)} samples")
    print(f"✓ Saved to {output_file}")
    return True

create_multilang_dataset()
```

### Cell 3: Train Model
```python
import sys
import torch
import yaml
import json
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer

def train_phase3a():
    """Train Phase 3A model."""
    print("=" * 60)
    print("PHASE 3A: FOUNDATION MODEL TRAINING")
    print("=" * 60)
    
    # Load config
    print("\n1. Loading config...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    # Optimize for Colab
    config["training"]["batch_size"] = 16
    config["training"]["num_epochs"] = 1
    config["training"]["learning_rate"] = 5e-4
    
    print(f"   Batch size: {config['training']['batch_size']}")
    print(f"   Learning rate: {config['training']['learning_rate']}")
    print(f"   Epochs: {config['training']['num_epochs']}")
    
    # Create model
    print("\n2. Creating model...")
    model = CodeModel(config["model"]).get_model()
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   ✓ Model created")
    print(f"   Parameters: {total_params:,}")
    
    # Load data
    print("\n3. Loading dataset...")
    data_path = Path("data/phase3a/processed/data.jsonl")
    
    samples = []
    with open(data_path) as f:
        for line in f:
            samples.append(json.loads(line))
    
    print(f"   ✓ Loaded {len(samples)} samples")
    
    # Train
    print("\n4. Starting training...")
    trainer = CodeModelTrainer(model, config, samples)
    trainer.train()
    
    # Save model
    print("\n5. Saving model...")
    output_dir = Path("outputs/models")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = output_dir / "foundation-model-v1.pt"
    torch.save(model.state_dict(), model_path)
    print(f"   ✓ Saved to {model_path}")
    print(f"   Size: {model_path.stat().st_size / 1e6:.1f} MB")
    
    print("\n" + "=" * 60)
    print("✅ PHASE 3A TRAINING COMPLETE")
    print("=" * 60)
    
    return True

train_phase3a()
```

### Cell 4: Download Model
```python
from google.colab import files
from pathlib import Path

model_path = Path("outputs/models/foundation-model-v1.pt")

if model_path.exists():
    print(f"Downloading {model_path.name}...")
    print(f"Size: {model_path.stat().st_size / 1e6:.1f} MB")
    files.download(str(model_path))
    print("✓ Download started!")
else:
    print("Model not found. Run training first.")
```

---

## Step 6: Download Trained Model

After training completes:

1. A download dialog will appear
2. Save `foundation-model-v1.pt` to your computer
3. Keep it safe - you'll need it for Phase 3B

---

## Tips for Google Colab

### 1. Session Timeout
- Colab sessions timeout after 12 hours
- Save checkpoint every 2 hours
- Resume from checkpoint if interrupted

### 2. Monitor GPU Usage
```python
# Check GPU memory
!nvidia-smi
```

### 3. Check Training Progress
```python
# View training logs
!tail -f outputs/logs/training.json
```

### 4. Handle Out of Memory
If you get "CUDA out of memory":
```python
# Reduce batch size
config["training"]["batch_size"] = 8
```

### 5. Use Gradient Accumulation
For larger effective batch size:
```python
config["training"]["gradient_accumulation_steps"] = 4
```

---

## Expected Output

```
============================================================
PHASE 3A: FOUNDATION MODEL TRAINING
============================================================

1. Loading config...
   Batch size: 16
   Learning rate: 0.0005
   Epochs: 1

2. Creating model...
   ✓ Model created
   Parameters: 111,200,000

3. Loading dataset...
   ✓ Loaded 96 samples

4. Starting training...
   Epoch 1/1
   Loss: 8.234 → 7.891 → 7.456 → ... → 2.123

5. Saving model...
   ✓ Saved to outputs/models/foundation-model-v1.pt
   Size: 445.2 MB

============================================================
✅ PHASE 3A TRAINING COMPLETE
============================================================
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'models'"
Add this at the top of training cell:
```python
import sys
sys.path.insert(0, str(Path.cwd()))
```

### "CUDA out of memory"
Reduce batch size:
```python
config["training"]["batch_size"] = 8
```

### "Git clone failed"
If your repo is private, use:
```python
!git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/code-model.git
```

### "Model not loading"
Check file exists:
```python
import os
print(os.path.exists("outputs/models/foundation-model-v1.pt"))
```

---

## Next Steps After Phase 3A

1. **Download model** - Save `foundation-model-v1.pt`
2. **Create Phase 3B notebook** - Upload Phase 3A model
3. **Run Phase 3B** - Fine-tune on HTML + CSS
4. **Repeat for Phase 3C and 3D**

---

## Colab Notebook Template

Create a new Colab notebook with this structure:

```
Cell 1: Setup & GPU Check
Cell 2: Clone Repository
Cell 3: Install Dependencies
Cell 4: Create Dataset
Cell 5: Train Model
Cell 6: Download Model
```

---

## Save Colab Notebook

1. Click **File** → **Save**
2. Save to Google Drive
3. Name: `Phase-3A-Foundation-Training`
4. You can resume later from the same notebook

---

## Monitor Training

### Real-time Monitoring
```python
# Check GPU usage during training
!watch -n 1 nvidia-smi
```

### View Loss
```python
# After training
import json
with open("outputs/logs/training.json") as f:
    logs = json.load(f)
    print(f"Final loss: {logs['loss'][-1]}")
```

---

## Checkpoint Resumption

If session times out:

```python
# Load checkpoint
model.load_state_dict(torch.load("outputs/models/foundation-model-v1.pt"))

# Resume training
trainer = CodeModelTrainer(model, config, samples)
trainer.train()
```

---

## Summary

| Step | Time | Action |
|------|------|--------|
| 1 | 1 min | Open Colab |
| 2 | 1 min | Change to GPU |
| 3 | 2 min | Clone repo |
| 4 | 3 min | Install deps |
| 5 | 1-2 hours | Train model |
| 6 | 1 min | Download |

**Total: 1-2 hours**

---

**Ready to start Phase 3A? Open Google Colab and follow the steps above! 🚀**
