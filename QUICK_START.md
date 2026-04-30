# Quick Start Guide

## ✅ Setup Complete!

All 4 trained models are ready in `outputs/models/`:

```
outputs/models/
├── foundation-model-v1.pt    (160 MB)
├── frontend-model-v1.pt      (160 MB)
├── fullstack-model-v1.pt     (160 MB)
└── universal-model-v1.pt     (160 MB)
```

---

## 🚀 3 Ways to Use

### Option 1: Command Line (Easiest)

```bash
# Generate code
python inference.py --prompt "function add"

# List models
python inference.py --list

# Use specific model
python inference.py --model universal-model-v1.pt --prompt "def fibonacci"
```

### Option 2: Python Script

```python
from model_loader import ModelLoader

loader = ModelLoader()
code = loader.generate("function add")
print(code)
```

### Option 3: API Server

```bash
# Terminal 1: Start server
python api_server.py

# Terminal 2: Make requests
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "function add"}'
```

---

## 📝 Examples

### Generate JavaScript
```bash
python inference.py --prompt "function fibonacci"
```

### Generate Python
```bash
python inference.py --prompt "def merge_sort"
```

### Generate SQL
```bash
python inference.py --prompt "SELECT * FROM users"
```

### Generate TypeScript
```bash
python inference.py --prompt "interface User"
```

### Generate Java
```bash
python inference.py --prompt "public class"
```

### Generate Go
```bash
python inference.py --prompt "func main"
```

### Generate Rust
```bash
python inference.py --prompt "fn main"
```

### Generate C#
```bash
python inference.py --prompt "public class"
```

### Generate HTML
```bash
python inference.py --model frontend-model-v1.pt --prompt "<div"
```

### Generate React
```bash
python inference.py --model fullstack-model-v1.pt --prompt "function Counter"
```

---

## 📊 Model Selection

| Task | Model | Command |
|------|-------|---------|
| JavaScript/Python | foundation | `--model foundation-model-v1.pt` |
| HTML/CSS | frontend | `--model frontend-model-v1.pt` |
| React/Express/Django | fullstack | `--model fullstack-model-v1.pt` |
| All languages | universal | `--model universal-model-v1.pt` (default) |

---

## 🔧 Advanced Options

```bash
# Adjust creativity (0.0-1.0, default 0.7)
python inference.py --prompt "function" --temperature 0.5

# Longer output (default 100)
python inference.py --prompt "function" --max-length 200

# Shorter output
python inference.py --prompt "function" --max-length 50
```

---

## 📚 Full Documentation

- **USAGE_GUIDE.md** - Complete usage guide
- **GPU_MEMORY_OPTIMIZATION.md** - Memory optimization
- **TRAINING_FIX.md** - Training dataset format

---

## 🎯 Next Steps

1. **Try it now:**
   ```bash
   python inference.py --prompt "function add"
   ```

2. **Start API server:**
   ```bash
   python api_server.py
   ```

3. **Use in Python:**
   ```python
   from model_loader import ModelLoader
   loader = ModelLoader()
   code = loader.generate("function add")
   ```

4. **Fine-tune on your data:**
   - Prepare your code samples
   - Update training script
   - Run training

---

## ✨ Features

✅ 4 trained models (Foundation, Frontend, Full-Stack, Universal)
✅ Command-line inference
✅ REST API server
✅ Python model loader
✅ Support for 10+ programming languages
✅ GPU acceleration (CUDA)
✅ CPU fallback support
✅ Model caching
✅ Batch generation
✅ Production-ready

---

## 🚀 Ready to Generate Code!

```bash
python inference.py --prompt "function add"
```

**That's it! Start generating code now! 🎉**
