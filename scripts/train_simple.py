"""Simple training script for code model."""
import sys
import os
import yaml
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data.loader import CodeDataLoader
from data.cleaner import CodeCleaner
from data.tokenizer import CodeTokenizer
from models.architecture import CodeModel


def main():
    """Simple training pipeline."""
    print("=" * 60)
    print("PHASE 2: SIMPLE TRAINING")
    print("=" * 60)

    # Load config
    print("\n1. Loading configuration...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    print("   ✓ Config loaded")

    # Create output directories
    print("\n2. Creating output directories...")
    for dir_name in ["checkpoints", "logs", "models"]:
        os.makedirs(f"outputs/{dir_name}", exist_ok=True)
    print("   ✓ Directories created")

    # Load data
    print("\n3. Loading data...")
    loader = CodeDataLoader(config["data"])
    dataset = loader._create_test_dataset()
    print(f"   ✓ Loaded {len(dataset)} samples")

    # Clean data
    print("\n4. Cleaning data...")
    cleaner = CodeCleaner(config["data"])
    dataset = cleaner.clean(dataset)
    print(f"   ✓ Cleaned to {len(dataset)} valid samples")

    if len(dataset) == 0:
        print("   ✗ No valid samples!")
        return False

    # Create model
    print("\n5. Creating model...")
    model = CodeModel(config["model"])
    model_obj = model.get_model()
    params = model.num_parameters_millions()
    print(f"   ✓ Model created: {params:.1f}M parameters")

    # Create tokenizer
    print("\n6. Creating tokenizer...")
    tokenizer = CodeTokenizer(config["model"])
    print("   ✓ Tokenizer ready")

    # Simple training loop
    print("\n7. Starting training...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_obj = model_obj.to(device)
    model_obj.train()

    optimizer = torch.optim.AdamW(model_obj.parameters(), lr=5e-4)
    num_epochs = 1

    for epoch in range(num_epochs):
        total_loss = 0
        num_batches = 0

        for idx, sample in enumerate(dataset):
            code = sample["content"]
            tokens = tokenizer.encode(code)

            # Truncate to max length
            max_len = 512
            if len(tokens) > max_len:
                tokens = tokens[:max_len]
            else:
                tokens = tokens + [0] * (max_len - len(tokens))

            # Convert to tensor
            input_ids = torch.tensor([tokens], dtype=torch.long).to(device)

            # Forward pass
            outputs = model_obj(input_ids, labels=input_ids)
            loss = outputs.loss

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

            print(f"   Batch {idx+1}/{len(dataset)} - Loss: {loss.item():.4f}")

        avg_loss = total_loss / num_batches
        print(f"\nEpoch {epoch+1} - Avg Loss: {avg_loss:.4f}")

    # Save model
    print("\n8. Saving model...")
    model_obj.save_pretrained("outputs/models/code-model-phase2")
    print("   ✓ Model saved")

    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
