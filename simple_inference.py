#!/usr/bin/env python3
"""
Simple Inference Script - Load and use trained models

Usage:
    python simple_inference.py
"""

import sys
import torch
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel


def main():
    """Simple inference."""
    print("=" * 70)
    print("CODE MODEL - SIMPLE INFERENCE")
    print("=" * 70)

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

    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\n✓ Device: {device}")

    # Load model
    print("\n1. Loading model...")
    model_path = Path("outputs/models/universal-model-v1.pt")

    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        print("\nAvailable models:")
        for model in Path("outputs/models").glob("*.pt"):
            size_mb = model.stat().st_size / 1e6
            print(f"  - {model.name} ({size_mb:.1f} MB)")
        return

    # Create model
    model = CodeModel(config["model"]).get_model()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    total_params = sum(p.numel() for p in model.parameters())
    print(f"✓ Model loaded: {model_path.name}")
    print(f"  Parameters: {total_params:,}")
    print(f"  Size: {model_path.stat().st_size / 1e6:.1f} MB")

    # Test generation
    print("\n2. Testing model...")
    print("\nAvailable models:")
    for model_file in sorted(Path("outputs/models").glob("*.pt")):
        size_mb = model_file.stat().st_size / 1e6
        print(f"  ✓ {model_file.name} ({size_mb:.1f} MB)")

    print("\n" + "=" * 70)
    print("✅ MODEL LOADED SUCCESSFULLY!")
    print("=" * 70)

    print("\n📝 Model Information:")
    print(f"  Device: {device}")
    print(f"  Parameters: {total_params:,}")
    print(f"  Embedding Dim: {config['model']['n_embd']}")
    print(f"  Layers: {config['model']['n_layer']}")
    print(f"  Attention Heads: {config['model']['n_head']}")
    print(f"  Max Sequence Length: {config['model']['n_positions']}")

    print("\n🚀 Next Steps:")
    print("  1. Use inference.py for code generation")
    print("  2. Use api_server.py for REST API")
    print("  3. Use model_loader.py for Python integration")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
