# Setup Guide - Code Model

## ✅ Installation Complete!

All dependencies are installed and models are ready to use.

---

## 🚀 Quick Start

### 1. List Available Models

```bash
python generate.py --list
```

Output:
```
📦 Available Models:
  foundation      foundation-model-v1.pt            168.6 MB
  frontend        frontend-model-v1.pt              168.6 MB
  fullstack       fullstack-model-v1.pt             168.6 MB
  universal       universal-model-v1.pt             168.6 MB
```

### 2. Generate Code

```bash
python generate.py "function add"
```

### 3. Use Different Models

```bash
# Foundation model (JS + Python)
python generate.py "def fibonacci" --model foundation

# Frontend model (+ HTML, CSS)
python generate.py "<div class='container'>" --model frontend

# Full-stack model (+ Frameworks)
python generate.py "app.get('/api/users')" --model fullstack

# Universal model (all languages)
python generate.py "interface User" --model universal
```

---

## 📦 Installed Dependencies

```
torch==2.0.1+
transformers==4.30.2+
numpy==1.24.3+
pyyaml==6.0+
flask==2.3.2+
flask-cors==4.0.0+
tqdm==4.65.0+
```

---

## 🎯 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate.py` | Generate code | `python generate.py "prompt"` |
| `simple_inference.py` | Test model loading | `python simple_inference.py` |
| `inference.py` | Advanced inference | `python inference.py --prompt "..."` |
| `api_server.py` | REST API server | `python api_server.py` |
| `model_loader.py` | Python model loader | `from model_loader import ModelLoader` |

---

## 📝 Examples

### Generate JavaScript
```bash
python generate.py "function fibonacci"
```

### Generate Python
```bash
python generate.py "def merge_sort"
```

### Generate SQL
```bash
python generate.py "SELECT * FROM users"
```

### Generate TypeScript
```bash
python generate.py "interface User"
```

### Generate Java
```bash
python generate.py "public class"
```

### Generate Go
```bash
python generate.py "func main"
```

### Generate Rust
```bash
python generate.py "fn main"
```

### Generate C#
```bash
python generate.py "public class"
```

### Generate HTML
```bash
python generate.py "<div" --model frontend
```

### Generate React
```bash
python generate.py "function Counter" --model fullstack
```

---

## 🔧 Advanced Options

```bash
# Adjust length
python generate.py "function add" --length 200

# Use specific model
python generate.py "def fibonacci" --model foundation

# List all models
python generate.py --list
```

---

## 🌐 API Server

### Start Server

```bash
python api_server.py
```

### Access API

```bash
# Health check
curl http://localhost:5000/health

# Generate code
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "function add"}'

# List models
curl http://localhost:5000/models
```

---

## 🐍 Python Integration

### Using Model Loader

```python
from model_loader import ModelLoader

loader = ModelLoader()
code = loader.generate("function add")
print(code)
```

### Direct Model Usage

```python
import torch
from models.architecture import CodeModel

config = {
    "model": {
        "vocab_size": 32000,
        "n_positions": 1024,
        "n_embd": 512,
        "n_layer": 8,
        "n_head": 8,
        "activation_function": "gelu_new"
    }
}

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CodeModel(config["model"]).get_model()
model.load_state_dict(torch.load("outputs/models/universal-model-v1.pt", map_location=device))
model = model.to(device)
model.eval()

print("✓ Model loaded!")
```

---

## ✅ Verification

### Check Models

```bash
python simple_inference.py
```

Expected output:
```
======================================================================
CODE MODEL - SIMPLE INFERENCE
======================================================================

✓ Device: cpu

1. Loading model...
✓ Model loaded: universal-model-v1.pt
  Parameters: 42,128,384
  Size: 168.6 MB

2. Testing model...

Available models:
  ✓ foundation-model-v1.pt (168.6 MB)
  ✓ frontend-model-v1.pt (168.6 MB)
  ✓ fullstack-model-v1.pt (168.6 MB)
  ✓ universal-model-v1.pt (168.6 MB)

======================================================================
✅ MODEL LOADED SUCCESSFULLY!
======================================================================
```

### Check Dependencies

```bash
python -c "import torch; import transformers; print('✓ All dependencies installed')"
```

---

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'torch'

**Solution:** Install dependencies
```bash
pip install torch transformers numpy pyyaml flask flask-cors tqdm
```

### Model Not Found

**Solution:** Ensure models are in `outputs/models/`
```bash
ls -la outputs/models/
```

### Out of Memory

**Solution:** Use CPU instead of GPU
```python
device = "cpu"
```

### Slow Generation

**Solution:** Use smaller model or reduce length
```bash
python generate.py "function" --model foundation --length 50
```

---

## 📊 System Information

### Minimum Requirements
- Python 3.8+
- 4 GB RAM
- 2 GB disk space

### Recommended
- Python 3.10+
- 16 GB RAM
- GPU (NVIDIA with CUDA)
- 2 GB disk space

### Tested On
- GPU: Tesla T4 (16 GB)
- OS: Linux, Windows, macOS
- Python: 3.10, 3.11, 3.12

---

## 📚 Documentation

- **QUICK_START.md** - Quick start guide
- **USAGE_GUIDE.md** - Complete usage documentation
- **GPU_MEMORY_OPTIMIZATION.md** - Memory optimization
- **TRAINING_FIX.md** - Training dataset format

---

## 🎉 You're All Set!

All models are loaded and ready to use.

**Start generating code now:**

```bash
python generate.py "function add"
```

---

**Happy coding! 🚀**
