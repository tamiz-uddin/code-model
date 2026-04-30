#!/usr/bin/env python3
"""
Code Model API Server
REST API for code generation

Usage:
    python api_server.py

Then access:
    http://localhost:5000/generate?prompt=function%20add
"""

import sys
import torch
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from data.tokenizer import CodeTokenizer


app = Flask(__name__)
CORS(app)

# Global model instance
model = None
tokenizer = None
device = None
config = None


def load_model(model_name="universal-model-v1.pt"):
    """Load model on startup."""
    global model, tokenizer, device, config

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

    # Create and load model
    model = CodeModel(config["model"]).get_model()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    # Create tokenizer
    tokenizer = CodeTokenizer(config["model"])

    print(f"✅ Model loaded: {model_name}")
    print(f"   Device: {device}")
    print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")


@app.route("/", methods=["GET"])
def home():
    """Home endpoint."""
    return jsonify({
        "name": "Code Model API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This help message",
            "GET /health": "Health check",
            "GET /models": "List available models",
            "POST /generate": "Generate code",
            "POST /complete": "Complete code snippet"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "device": device,
        "model_loaded": model is not None
    })


@app.route("/models", methods=["GET"])
def list_models():
    """List available models."""
    models_dir = Path("outputs/models")
    models = []

    if models_dir.exists():
        for model_file in sorted(models_dir.glob("*.pt")):
            size_mb = model_file.stat().st_size / 1e6
            models.append({
                "name": model_file.name,
                "size_mb": round(size_mb, 1)
            })

    return jsonify({"models": models})


@app.route("/generate", methods=["POST", "GET"])
def generate():
    """Generate code from prompt."""
    try:
        # Get parameters
        if request.method == "POST":
            data = request.get_json()
            prompt = data.get("prompt", "function add")
            max_length = data.get("max_length", 100)
            temperature = data.get("temperature", 0.7)
        else:
            prompt = request.args.get("prompt", "function add")
            max_length = int(request.args.get("max_length", 100))
            temperature = float(request.args.get("temperature", 0.7))

        # Validate parameters
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        if max_length < 1 or max_length > 500:
            return jsonify({"error": "max_length must be between 1 and 500"}), 400

        if temperature < 0.0 or temperature > 1.0:
            return jsonify({"error": "temperature must be between 0.0 and 1.0"}), 400

        # Tokenize prompt
        tokens = tokenizer.encode(prompt)
        input_ids = torch.tensor([tokens[:config["model"]["n_positions"]]]).to(device)

        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=min(max_length, config["model"]["n_positions"]),
                temperature=temperature,
                top_k=50,
                do_sample=True
            )

        # Decode
        generated_tokens = output[0].tolist()
        generated_code = tokenizer.decode(generated_tokens)

        return jsonify({
            "prompt": prompt,
            "generated": generated_code,
            "length": len(generated_code),
            "device": device
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/complete", methods=["POST", "GET"])
def complete():
    """Complete a code snippet."""
    try:
        # Get parameters
        if request.method == "POST":
            data = request.get_json()
            code = data.get("code", "function add")
            max_length = data.get("max_length", 50)
        else:
            code = request.args.get("code", "function add")
            max_length = int(request.args.get("max_length", 50))

        # Validate parameters
        if not code:
            return jsonify({"error": "Code is required"}), 400

        # Tokenize code
        tokens = tokenizer.encode(code)
        input_ids = torch.tensor([tokens[:config["model"]["n_positions"]]]).to(device)

        # Generate completion
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=min(len(tokens) + max_length, config["model"]["n_positions"]),
                do_sample=False
            )

        # Decode
        completed_tokens = output[0].tolist()
        completed_code = tokenizer.decode(completed_tokens)

        return jsonify({
            "input": code,
            "completed": completed_code,
            "length": len(completed_code),
            "device": device
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 70)
    print("CODE MODEL API SERVER")
    print("=" * 70)

    try:
        # Load model
        load_model("universal-model-v1.pt")

        # Start server
        print("\n🚀 Starting API server...")
        print("   URL: http://localhost:5000")
        print("   Docs: http://localhost:5000/")
        print("\n" + "=" * 70)

        app.run(debug=False, host="0.0.0.0", port=5000)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
