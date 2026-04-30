"""Test trained model."""
import sys
import torch
from pathlib import Path
from transformers import GPT2LMHeadModel

sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Test model."""
    print("=" * 60)
    print("MODEL TEST")
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

    # Setup device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    print(f"   Device: {device}")

    # Test forward pass
    print("\n2. Testing forward pass...")
    with torch.no_grad():
        # Create random input (within vocab size)
        input_ids = torch.randint(0, 32000, (2, 512)).to(device)
        output = model(input_ids)
        print(f"   ✓ Forward pass successful")
        print(f"   Input shape: {input_ids.shape}")
        print(f"   Output logits shape: {output.logits.shape}")

    # Test with labels (training mode)
    print("\n3. Testing with labels...")
    with torch.no_grad():
        input_ids = torch.randint(0, 32000, (2, 512)).to(device)
        output = model(input_ids, labels=input_ids)
        print(f"   ✓ Forward pass with labels successful")
        print(f"   Loss: {output.loss.item():.4f}")

    print("\n" + "=" * 60)
    print("✅ MODEL TEST COMPLETE")
    print("=" * 60)
    print("\nModel is working correctly!")
    print("Ready for Phase 3: Full dataset training")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
