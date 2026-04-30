# Code Model - Usage Guide

## 📦 Models Available

All 4 trained models are in `outputs/models/`:

| Model | File | Size | Supports |
|-------|------|------|----------|
| Foundation | foundation-model-v1.pt | 160 MB | JavaScript, Python |
| Frontend | frontend-model-v1.pt | 160 MB | + HTML, CSS |
| Full-Stack | fullstack-model-v1.pt | 160 MB | + React, Express, Django, Flask, SQL |
| Universal | universal-model-v1.pt | 160 MB | + TypeScript, Java, Go, Rust, C#, GraphQL |

---

## 🚀 Quick Start

### 1. Generate Code (Command Line)

```bash
# Generate code using universal model
python inference.py --prompt "function add"

# Generate with specific model
python inference.py --model foundation-model-v1.pt --prompt "def fibonacci"

# Adjust generation parameters
python inference.py --prompt "class User" --max-length 200 --temperature 0.5
```

### 2. Use Model Loader (Python)

```python
from model_loader import ModelLoader

# Initialize loader
loader = ModelLoader()

# Generate code
code = loader.generate("function add")
print(code)

# Complete code
completed = loader.complete("def fibonacci")
print(completed)

# List available models
models = loader.list_models()
for model in models:
    print(f"{model['name']}: {model['size_mb']} MB")
```

### 3. Start API Server

```bash
# Start server
python api_server.py

# Server runs on http://localhost:5000
```

---

## 📝 Usage Examples

### Example 1: Generate JavaScript Code

```bash
python inference.py --model universal-model-v1.pt --prompt "function add(a, b)"
```

Output:
```javascript
function add(a, b) {
    return a + b;
}
```

### Example 2: Generate Python Code

```bash
python inference.py --prompt "def fibonacci(n):"
```

Output:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Example 3: Complete HTML

```bash
python inference.py --model frontend-model-v1.pt --prompt "<div class='container'>"
```

### Example 4: Generate SQL

```bash
python inference.py --model universal-model-v1.pt --prompt "SELECT * FROM users"
```

---

## 🔌 API Server Usage

### Start Server

```bash
python api_server.py
```

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "device": "cuda",
  "model_loaded": true
}
```

#### 2. List Models
```bash
curl http://localhost:5000/models
```

Response:
```json
{
  "models": [
    {"name": "foundation-model-v1.pt", "size_mb": 160.0},
    {"name": "frontend-model-v1.pt", "size_mb": 160.0},
    {"name": "fullstack-model-v1.pt", "size_mb": 160.0},
    {"name": "universal-model-v1.pt", "size_mb": 160.0}
  ]
}
```

#### 3. Generate Code
```bash
# GET request
curl "http://localhost:5000/generate?prompt=function%20add&max_length=100"

# POST request
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "function add",
    "max_length": 100,
    "temperature": 0.7
  }'
```

Response:
```json
{
  "prompt": "function add",
  "generated": "function add(a, b) { return a + b; }",
  "length": 35,
  "device": "cuda"
}
```

#### 4. Complete Code
```bash
curl -X POST http://localhost:5000/complete \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci",
    "max_length": 50
  }'
```

Response:
```json
{
  "input": "def fibonacci",
  "completed": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "length": 85,
  "device": "cuda"
}
```

---

## 🐍 Python Integration

### Load and Use Model

```python
import torch
from models.architecture import CodeModel
from data.tokenizer import CodeTokenizer

# Configuration
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

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CodeModel(config["model"]).get_model()
model.load_state_dict(torch.load("outputs/models/universal-model-v1.pt", map_location=device))
model = model.to(device)
model.eval()

# Create tokenizer
tokenizer = CodeTokenizer(config["model"])

# Generate code
prompt = "function add"
tokens = tokenizer.encode(prompt)
input_ids = torch.tensor([tokens]).to(device)

with torch.no_grad():
    output = model.generate(input_ids, max_length=100)

generated_code = tokenizer.decode(output[0].tolist())
print(generated_code)
```

### Fine-tune on Custom Data

```python
from training.trainer import CodeModelTrainer

# Load model
model = CodeModel(config["model"]).get_model()
model.load_state_dict(torch.load("outputs/models/universal-model-v1.pt"))

# Your custom dataset
custom_samples = [
    {"content": "your code sample 1"},
    {"content": "your code sample 2"},
    {"content": "your code sample 3"},
]

# Fine-tune
config["training"]["batch_size"] = 4
config["training"]["num_epochs"] = 1
config["training"]["learning_rate"] = 1e-6

trainer = CodeModelTrainer(model, config, custom_samples)
trainer.train()

# Save fine-tuned model
torch.save(model.state_dict(), "outputs/models/custom-model.pt")
```

---

## 📊 Model Comparison

### Foundation Model
- **Best for:** Learning basic code patterns
- **Supports:** JavaScript, Python
- **Use case:** Code generation for basic tasks

```bash
python inference.py --model foundation-model-v1.pt --prompt "function"
```

### Frontend Model
- **Best for:** Web development
- **Supports:** + HTML, CSS
- **Use case:** Frontend code generation

```bash
python inference.py --model frontend-model-v1.pt --prompt "<div"
```

### Full-Stack Model
- **Best for:** Complete web applications
- **Supports:** + React, Express, Django, Flask, SQL
- **Use case:** Full-stack development

```bash
python inference.py --model fullstack-model-v1.pt --prompt "app.get"
```

### Universal Model
- **Best for:** All programming tasks
- **Supports:** All languages and frameworks
- **Use case:** General-purpose code generation

```bash
python inference.py --model universal-model-v1.pt --prompt "class"
```

---

## ⚙️ Configuration

### Generation Parameters

```python
# Temperature (0.0-1.0)
# Lower = more deterministic, Higher = more creative
temperature = 0.7

# Top-k sampling
# Only sample from top k most likely tokens
top_k = 50

# Max length
# Maximum tokens to generate
max_length = 100

# Do sample
# Use sampling instead of greedy decoding
do_sample = True
```

### Model Parameters

```python
config = {
    "model": {
        "vocab_size": 32000,      # Vocabulary size
        "n_positions": 1024,      # Max sequence length
        "n_embd": 512,            # Embedding dimension
        "n_layer": 8,             # Number of layers
        "n_head": 8,              # Number of attention heads
        "activation_function": "gelu_new"
    }
}
```

---

## 🔧 Troubleshooting

### Model Not Found

```
FileNotFoundError: Model not found: outputs/models/universal-model-v1.pt
```

**Solution:** Make sure all 4 model files are in `outputs/models/`:
```bash
ls -la outputs/models/
```

### Out of Memory

```
torch.OutOfMemoryError: CUDA out of memory
```

**Solution:** Reduce max_length or use CPU:
```python
device = "cpu"  # Use CPU instead of GPU
```

### Slow Generation

**Solution:** Use a smaller model or reduce max_length:
```bash
python inference.py --model foundation-model-v1.pt --max-length 50
```

### API Server Not Starting

```
Address already in use
```

**Solution:** Use a different port:
```python
app.run(port=5001)
```

---

## 📚 Advanced Usage

### Batch Generation

```python
from model_loader import ModelLoader

loader = ModelLoader()

prompts = [
    "function add",
    "def fibonacci",
    "class User",
    "SELECT * FROM"
]

for prompt in prompts:
    code = loader.generate(prompt)
    print(f"Prompt: {prompt}")
    print(f"Generated: {code}\n")
```

### Model Ensemble

```python
# Use different models for different tasks
loader = ModelLoader()

# JavaScript
js_code = loader.generate("function", model_name="foundation-model-v1.pt")

# HTML
html_code = loader.generate("<div", model_name="frontend-model-v1.pt")

# SQL
sql_code = loader.generate("SELECT", model_name="fullstack-model-v1.pt")
```

### Custom Tokenizer

```python
from data.tokenizer import CodeTokenizer

tokenizer = CodeTokenizer(config["model"])

# Encode
tokens = tokenizer.encode("function add(a, b) { return a + b; }")
print(tokens)

# Decode
code = tokenizer.decode(tokens)
print(code)
```

---

## 📖 Documentation

- **inference.py** - Command-line code generation
- **api_server.py** - REST API server
- **model_loader.py** - Python model loader
- **GPU_MEMORY_OPTIMIZATION.md** - Memory optimization guide
- **TRAINING_FIX.md** - Training dataset format fix

---

## 🎯 Next Steps

1. **Try inference:** `python inference.py --prompt "function add"`
2. **Start API:** `python api_server.py`
3. **Use in Python:** `from model_loader import ModelLoader`
4. **Fine-tune:** Train on your own code samples
5. **Deploy:** Use API server in production

---

**Ready to generate code! 🚀**
