"""Simple inference script."""
import sys
import torch
from pathlib import Path
from transformers import GPT2LMHeadModel, GPT2Tokenizer

sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Run simple inference."""
    print("=" * 60)
    print("CODE MODEL INFERENCE (SIMPLE)")
    print("=" * 60)

    # Load model
    print("\n1. Loading model...")
    model_path = "outputs/models/code-model-phase2"

    if Path(model_path).exists():
        model = GPT2LMHeadModel.from_pretrained(model_path)
        print(f"   ✓ Model loaded from {model_path}")
    else:
        print(f"   ✗ Model not found at {model_path}")
        return False

    # Load tokenizer (use standard GPT2 tokenizer)
    print("\n2. Loading tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    print("   ✓ Tokenizer loaded")

    # Setup device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    print(f"   Device: {device}")

    # Test prompts
    prompts = [
        "def fibonacci",
        "class DataProcessor",
        "import numpy",
    ]

    print("\n3. Running inference...")
    for prompt in prompts:
        print(f"\n   Prompt: {prompt}")

        # Encode
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)

        # Generate
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=50,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95,
            )

        # Decode
        generated = tokenizer.decode(output[0], skip_special_tokens=True)
        print(f"   Generated: {generated}")

    print("\n" + "=" * 60)
    print("✅ INFERENCE COMPLETE")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
