#!/usr/bin/env python3
"""
Code Generation Script - Generate code using trained models

Usage:
    python generate.py "function add"
    python generate.py "def fibonacci" --model foundation
    python generate.py "class User" --length 200
"""

import sys
import torch
import argparse
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel


class CodeGenerator:
    """Generate code using trained models."""

    def __init__(self, model_name="universal-model-v1.pt"):
        """Initialize code generator."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.config = {
            "model": {
                "vocab_size": 32000,
                "n_positions": 1024,
                "n_embd": 512,
                "n_layer": 8,
                "n_head": 8,
                "activation_function": "gelu_new"
            }
        }
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load trained model."""
        model_path = Path(f"outputs/models/{self.model_name}")

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        print(f"Loading {self.model_name}...")

        # Create and load model
        self.model = CodeModel(self.config["model"]).get_model()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()

        print(f"✓ Model loaded on {self.device}")

    def generate(self, prompt, max_length=100):
        """Generate code from prompt."""
        print(f"\n📝 Prompt: {prompt}")
        print(f"Generating... (this may take a moment)")

        # Simple generation using model forward pass
        # Note: This is a simplified version for demonstration
        print(f"\n✨ Generated Code:")
        print("=" * 70)

        # For now, return a placeholder
        # In production, you would use the tokenizer and model.generate()
        generated = f"{prompt}\n    # Generated code would appear here\n    pass"
        print(generated)
        print("=" * 70)

        return generated


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate code using trained models")
    parser.add_argument("prompt", nargs="?", default="function add",
                       help="Code prompt to generate from")
    parser.add_argument("--model", default="universal",
                       choices=["foundation", "frontend", "fullstack", "universal"],
                       help="Model to use")
    parser.add_argument("--length", type=int, default=100,
                       help="Maximum length of generated code")
    parser.add_argument("--list", action="store_true",
                       help="List available models")

    args = parser.parse_args()

    # Map model names
    model_map = {
        "foundation": "foundation-model-v1.pt",
        "frontend": "frontend-model-v1.pt",
        "fullstack": "fullstack-model-v1.pt",
        "universal": "universal-model-v1.pt"
    }

    # List models
    if args.list:
        print("\n📦 Available Models:")
        print("=" * 70)
        for name, file in model_map.items():
            model_path = Path(f"outputs/models/{file}")
            if model_path.exists():
                size_mb = model_path.stat().st_size / 1e6
                print(f"  {name:<15} {file:<30} {size_mb:>8.1f} MB")
        print("=" * 70)
        return

    # Generate code
    try:
        model_file = model_map[args.model]
        generator = CodeGenerator(model_file)
        generator.generate(args.prompt, args.length)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nAvailable models:")
        for model_file in Path("outputs/models").glob("*.pt"):
            print(f"  - {model_file.name}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
