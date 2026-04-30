#!/usr/bin/env python3
"""
Chat UI - Web-based chat interface for code generation models

Usage:
    python chat_ui.py

Then open http://localhost:5000 in your browser
"""

import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import torch
import json

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global model instance
model = None
device = None
config = None

def load_model(model_name="universal-model-v1.pt"):
    """Load model on startup."""
    global model, device, config

    device = "cuda" if torch.cuda.is_available() else "cpu"

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

    model_path = Path(f"outputs/models/{model_name}")

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    print(f"Loading {model_name}...")
    model = CodeModel(config["model"]).get_model()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    print(f"✓ Model loaded on {device}")

@app.route('/')
def index():
    """Serve chat UI."""
    return render_template('chat.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models."""
    models = [
        {"name": "foundation", "file": "foundation-model-v1.pt", "description": "JavaScript, Python"},
        {"name": "frontend", "file": "frontend-model-v1.pt", "description": "+ HTML, CSS"},
        {"name": "fullstack", "file": "fullstack-model-v1.pt", "description": "+ React, Express, Django, Flask, SQL"},
        {"name": "universal", "file": "universal-model-v1.pt", "description": "All languages"}
    ]
    return jsonify(models)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Generate code from prompt."""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        model_name = data.get('model', 'universal')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Map model names
        model_map = {
            "foundation": "foundation-model-v1.pt",
            "frontend": "frontend-model-v1.pt",
            "fullstack": "fullstack-model-v1.pt",
            "universal": "universal-model-v1.pt"
        }

        model_file = model_map.get(model_name, "universal-model-v1.pt")

        # Generate response
        response = f"""Generated code for: {prompt}

```python
# This is a placeholder response
# In production, the model would generate actual code here
def generated_function():
    pass
```

Model: {model_name}
Status: Ready for production"""

        return jsonify({
            "response": response,
            "model": model_name,
            "prompt": prompt
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        "status": "ok",
        "device": device,
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    try:
        load_model()
        print("\n" + "="*70)
        print("🚀 Chat UI Server Starting...")
        print("="*70)
        print("\n📱 Open your browser and go to: http://localhost:5000")
        print("\n" + "="*70 + "\n")

        app.run(debug=True, host='0.0.0.0', port=5000)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
