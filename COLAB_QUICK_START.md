# Google Colab Quick Start - Phase 3A

## 🚀 5-Minute Setup

### 1. Open Colab
- Go to https://colab.research.google.com
- Click "New notebook"
- Rename: `Phase-3A-Training`

### 2. Change to GPU
- Runtime → Change runtime type
- Hardware accelerator: GPU (T4)
- Click Save

### 3. Clone Repository
```python
!git clone https://github.com/YOUR_USERNAME/code-model.git
%cd code-model
!pip install -q torch transformers datasets tokenizers accelerate pyyaml
```

### 4. Run Training
```python
import sys
import torch
import yaml
import json
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

config["training"]["batch_size"] = 16
config["training"]["num_epochs"] = 1

# Create model
model = CodeModel(config["model"]).get_model()

# Create dataset
samples = [
    "function add(a, b) { return a + b; }",
    "const greet = (name) => `Hello, ${name}!`;",
    "async function fetchData(url) { const res = await fetch(url); return res.json(); }",
    "class Stack { constructor() { this.items = []; } push(item) { this.items.push(item); } }",
    "def add(a, b):\n    return a + b",
    "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
    "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
    "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)",
]
samples = samples * 12

# Train
trainer = CodeModelTrainer(model, config, samples)
trainer.train()

# Save
from pathlib import Path
output_dir = Path("outputs/models")
output_dir.mkdir(parents=True, exist_ok=True)
model_path = output_dir / "foundation-model-v1.pt"
torch.save(model.state_dict(), model_path)
print(f"✓ Model saved: {model_path.stat().st_size / 1e6:.1f} MB")
```

### 5. Download Model
```python
from google.colab import files
files.download("outputs/models/foundation-model-v1.pt")
```

---

## ✅ Checklist

- [ ] Open Google Colab
- [ ] Change runtime to GPU (T4)
- [ ] Clone repository
- [ ] Install dependencies
- [ ] Create dataset
- [ ] Run training
- [ ] Download model
- [ ] Save locally

---

## 📊 Expected Results

- **Time:** 30-60 minutes
- **GPU:** NVIDIA T4 (16GB)
- **Model Size:** 445 MB
- **Loss:** 8-9 → 2-3
- **Output:** foundation-model-v1.pt

---

## 🔧 Troubleshooting

### GPU Not Available
```python
import torch
print(torch.cuda.is_available())  # Should be True
```

### Out of Memory
```python
config["training"]["batch_size"] = 8  # Reduce from 16
```

### Module Not Found
```python
import sys
sys.path.insert(0, str(Path.cwd()))
```

---

## 📝 Next Steps

1. Download `foundation-model-v1.pt`
2. Create Phase 3B notebook
3. Upload Phase 3A model
4. Run Phase 3B training
5. Repeat for Phase 3C and 3D

---

**Ready? Open Google Colab and start training! 🚀**
