#!/usr/bin/env python3
"""
Code Model Inference Script
Generate code using trained models

Usage:
    python inference.py --model universal --prompt "function add"
"""

import sys
import torch
import argparse
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from data.tokenizer import CodeTokenizer


class CodeModelInference:
    """Inference engine for code generation."""

    def __init__(self, model_name="universal-model-v1.pt"):
        """Initialize inference engine."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.config = self._get_config()
        self._load_model()

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

    def _load_model(self):
        """Load trained model."""
        print(f"Loading {self.model_name}...")

        model_path = Path(f"outputs/models/{self.model_name}")

        if not model_path.exists():
            print(f"❌ Model not found: {model_path}")
            print(f"Available models:")
            models_dir = Path("outputs/models")
            if models_dir.exists():
                for model in models_dir.glob("*.pt"):
                    print(f"  - {model.name}")
            sys.exit(1)

        # Create model
        self.model = CodeModel(self.config["model"]).get_model()

        # Load weights
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()

        # Create tokenizer
        self.tokenizer = CodeTokenizer(self.config["model"])

        print(f"✅ Model loaded: {self.model_name}")
        print(f"   Device: {self.device}")
        print(f"   Parameters: {sum(p.numel() for p in self.model.parameters()):,}")

    def generate(self, prompt, max_length=100, temperature=0.7, top_k=50):
        """Generate code from prompt."""
        print(f"\n📝 Prompt: {prompt}")

        # Tokenize prompt
        tokens = self.tokenizer.encode(prompt)
        input_ids = torch.tensor([tokens[:self.config["model"]["n_positions"]]]).to(self.device)

        # Generate
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=min(max_length, self.config["model"]["n_positions"]),
                temperature=temperature,
                top_k=top_k,
                do_sample=True
            )

        # Decode
        generated_tokens = output[0].tolist()
        generated_code = self.tokenizer.decode(generated_tokens)

        print(f"\n✨ Generated Code:")
        print("=" * 70)
        print(generated_code)
        print("=" * 70)

        return generated_code

    def list_models(self):
        """List available models."""
        models_dir = Path("outputs/models")

        if not models_dir.exists():
            print("❌ No models directory found")
            return

        models = list(models_dir.glob("*.pt"))

        if not models:
            print("❌ No models found")
            return

        print("\n📦 Available Models:")
        print("=" * 70)

        model_info = {
            "foundation-model-v1.pt": "Foundation (JS + Python)",
            "frontend-model-v1.pt": "Frontend (+ HTML, CSS)",
            "fullstack-model-v1.pt": "Full-Stack (+ Frameworks)",
            "universal-model-v1.pt": "Universal (+ All Languages)"
        }

        for model in sorted(models):
            size_mb = model.stat().st_size / 1e6
            description = model_info.get(model.name, "Unknown")
            print(f"  {model.name:<30} {size_mb:>8.1f} MB  - {description}")

        print("=" * 70)


def main():
    """Main inference function."""
    parser = argparse.ArgumentParser(description="Code Model Inference")
    parser.add_argument("--model", default="universal-model-v1.pt",
                       help="Model to use (default: universal-model-v1.pt)")
    parser.add_argument("--prompt", default="function add",
                       help="Code prompt to generate from")
    parser.add_argument("--max-length", type=int, default=100,
                       help="Maximum generation length")
    parser.add_argument("--temperature", type=float, default=0.7,
                       help="Generation temperature")
    parser.add_argument("--list", action="store_true",
                       help="List available models")

    args = parser.parse_args()

    # Initialize inference engine
    inference = CodeModelInference(args.model)

    # List models if requested
    if args.list:
        inference.list_models()
        return

    # Generate code
    inference.generate(
        args.prompt,
        max_length=args.max_length,
        temperature=args.temperature
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
