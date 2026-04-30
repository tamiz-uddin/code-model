#!/usr/bin/env python3
"""
Model Loader Utility
Load and manage trained models

Usage:
    from model_loader import ModelLoader

    loader = ModelLoader()
    model = loader.load("universal-model-v1.pt")
    code = loader.generate("function add")
"""

import sys
import torch
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from data.tokenizer import CodeTokenizer


class ModelLoader:
    """Load and manage trained models."""

    def __init__(self):
        """Initialize model loader."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.config = self._get_config()

    def _get_config(self):
        """Get model configuration."""
        return {
            "model": {
                "vocab_size": 32000,
                "n_positions": 1024,
                "n_embd": 512,
                "n_layer": 8,
                "n_head": 8,
                "activation_function": "gelu_new"
            }
        }

    def load(self, model_name):
        """Load a model."""
        if model_name in self.models:
            return self.models[model_name]

        model_path = Path(f"outputs/models/{model_name}")

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        print(f"Loading {model_name}...")

        # Create model
        model = CodeModel(self.config["model"]).get_model()

        # Load weights
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model = model.to(self.device)
        model.eval()

        # Create tokenizer
        tokenizer = CodeTokenizer(self.config["model"])

        # Cache
        self.models[model_name] = {
            "model": model,
            "tokenizer": tokenizer
        }

        print(f"✅ Loaded: {model_name}")
        return self.models[model_name]

    def generate(self, prompt, model_name="universal-model-v1.pt", max_length=100):
        """Generate code."""
        model_data = self.load(model_name)
        model = model_data["model"]
        tokenizer = model_data["tokenizer"]

        # Tokenize
        tokens = tokenizer.encode(prompt)
        input_ids = torch.tensor([tokens]).to(self.device)

        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=max_length,
                temperature=0.7,
                top_k=50,
                do_sample=True
            )

        # Decode
        return tokenizer.decode(output[0].tolist())

    def complete(self, code, model_name="universal-model-v1.pt", max_length=50):
        """Complete code."""
        model_data = self.load(model_name)
        model = model_data["model"]
        tokenizer = model_data["tokenizer"]

        # Tokenize
        tokens = tokenizer.encode(code)
        input_ids = torch.tensor([tokens]).to(self.device)

        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=len(tokens) + max_length,
                do_sample=False
            )

        # Decode
        return tokenizer.decode(output[0].tolist())

    def list_models(self):
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

        return models

    def unload(self, model_name):
        """Unload a model from memory."""
        if model_name in self.models:
            del self.models[model_name]
            print(f"Unloaded: {model_name}")

    def unload_all(self):
        """Unload all models."""
        self.models.clear()
        print("Unloaded all models")


if __name__ == "__main__":
    # Example usage
    loader = ModelLoader()

    # List models
    print("\n📦 Available Models:")
    for model_info in loader.list_models():
        print(f"  {model_info['name']:<30} {model_info['size_mb']:>8.1f} MB")

    # Generate code
    print("\n✨ Generating code...")
    code = loader.generate("function add", max_length=100)
    print(f"\nGenerated:\n{code}")

    # Complete code
    print("\n✨ Completing code...")
    completed = loader.complete("def fibonacci", max_length=50)
    print(f"\nCompleted:\n{completed}")
