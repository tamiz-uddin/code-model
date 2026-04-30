"""Inference script for code model."""
import sys
import os
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models.architecture import CodeModel
from data.tokenizer import CodeTokenizer
import yaml


def main():
    """Run inference on code model."""
    print("=" * 60)
    print("CODE MODEL INFERENCE")
    print("=" * 60)

    # Load config
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Load model
    print("\n1. Loading model...")
    model_path = "outputs/models/code-model-phase2"

    if Path(model_path).exists():
        from transformers import GPT2LMHeadModel
        model = GPT2LMHeadModel.from_pretrained(model_path)
        print(f"   ✓ Model loaded from {model_path}")
    else:
        print(f"   ⚠ Model not found at {model_path}")
        print("   Using untrained model for demo")
        model = CodeModel(config["model"]).get_model()

    # Initialize tokenizer
    print("\n2. Initializing tokenizer...")
    tokenizer = CodeTokenizer(config["model"])
    print("   ✓ Tokenizer ready")

    # Test prompts
    prompts = [
        "def fibonacci",
        "class DataProcessor",
        "import numpy",
    ]

    print("\n3. Running inference...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()

    for prompt in prompts:
        print(f"\n   Prompt: {prompt}")
        tokens = tokenizer.encode(prompt)
        input_ids = torch.tensor([tokens], dtype=torch.long).to(device)

        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
            )

        generated = tokenizer.decode(output[0].tolist())
        print(f"   Generated: {generated[:100]}...")

    print("\n" + "=" * 60)
    print("✅ INFERENCE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
