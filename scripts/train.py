"""Training script for code model."""
import os
import sys
import yaml
import torch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from data.loader import CodeDataLoader
from data.cleaner import CodeCleaner
from data.tokenizer import CodeTokenizer
from models.architecture import CodeModel
from training.trainer import CodeModelTrainer


def main():
    """Main training pipeline."""
    print("=" * 60)
    print("PHASE 2: SMALL-SCALE TRAINING")
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
        print("   ✗ No valid samples after cleaning!")
        return False

    # Create model
    print("\n5. Creating model...")
    model = CodeModel(config["model"])
    params = model.num_parameters_millions()
    print(f"   ✓ Model created: {params:.1f}M parameters")

    # Create trainer
    print("\n6. Setting up trainer...")
    trainer = CodeModelTrainer(
        model=model.get_model(),
        config=config,
        dataset=dataset,
        output_dir="outputs"
    )
    print("   ✓ Trainer ready")

    # Train
    print("\n7. Starting training...")
    print("   (This may take a few minutes on CPU)")
    trainer.train()

    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check outputs/logs/ for training metrics")
    print("2. Review outputs/checkpoints/ for saved models")
    print("3. Phase 3: Prepare full dataset (100K+ samples)")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
