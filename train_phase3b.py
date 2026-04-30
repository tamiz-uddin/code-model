#!/usr/bin/env python3
"""
Phase 3B: Frontend Stack Training
Fine-tune on HTML + CSS

Usage:
    python train_phase3b.py

Or in Google Colab:
    !python train_phase3b.py
"""

import sys
import torch
import yaml
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer


def main():
    """Train Phase 3B model."""
    print("=" * 70)
    print("PHASE 3B: FRONTEND STACK TRAINING")
    print("=" * 70)

    # Check GPU
    print("\n1. Checking GPU...")
    print(f"   GPU Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   GPU Name: {torch.cuda.get_device_name(0)}")

    # Load config
    print("\n2. Loading configuration...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    config["training"]["batch_size"] = 16
    config["training"]["num_epochs"] = 1
    config["training"]["learning_rate"] = 1e-5  # Lower for fine-tuning

    print(f"   Learning rate: {config['training']['learning_rate']} (fine-tuning)")

    # Load Phase 3A model
    print("\n3. Loading Phase 3A checkpoint...")
    model = CodeModel(config["model"]).get_model()
    model_path = Path("outputs/models/foundation-model-v1.pt")

    if not model_path.exists():
        print(f"   ⚠ Model not found: {model_path}")
        print("   Run Phase 3A first!")
        return False

    model.load_state_dict(torch.load(model_path))
    print(f"   ✓ Loaded {model_path}")

    # Create dataset
    print("\n4. Creating HTML + CSS dataset...")
    samples = [
        # HTML samples
        "<!DOCTYPE html>\n<html>\n<head><title>Page</title></head>\n<body><h1>Hello</h1></body>\n</html>",
        "<div class='container'>\n  <header>\n    <nav><a href='/'>Home</a></nav>\n  </header>\n</div>",
        "<form>\n  <input type='text' placeholder='Name'>\n  <button type='submit'>Submit</button>\n</form>",
        "<table>\n  <tr><th>Name</th><th>Age</th></tr>\n  <tr><td>John</td><td>30</td></tr>\n</table>",
        "<img src='image.jpg' alt='Description'>",
        "<video controls>\n  <source src='video.mp4' type='video/mp4'>\n</video>",
        "<section>\n  <article>\n    <h2>Title</h2>\n    <p>Content</p>\n  </article>\n</section>",

        # CSS samples
        ".container { max-width: 1200px; margin: 0 auto; }",
        ".flex { display: flex; justify-content: space-between; align-items: center; }",
        ".grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }",
        "@media (max-width: 768px) { .container { padding: 10px; } }",
        ".button { background: #007bff; color: white; padding: 10px 20px; border-radius: 5px; }",
        ".card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; padding: 20px; }",
        "@keyframes slide { from { transform: translateX(0); } to { transform: translateX(100px); } }",
    ]

    samples = samples * 5  # 70 samples

    print(f"   ✓ Created {len(samples)} samples")
    print(f"   HTML: 35, CSS: 35")

    # Train
    print("\n5. Starting fine-tuning...")
    trainer = CodeModelTrainer(model, config, samples)
    trainer.train()

    # Save model
    print("\n6. Saving model...")
    output_dir = Path("outputs/models")
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "frontend-model-v1.pt"
    torch.save(model.state_dict(), model_path)

    file_size = model_path.stat().st_size / 1e6
    print(f"   ✓ Saved to {model_path}")
    print(f"   Size: {file_size:.1f} MB")

    # Summary
    print("\n" + "=" * 70)
    print("✅ PHASE 3B TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nModel: {model_path}")
    print(f"Size: {file_size:.1f} MB")
    print("\nNext steps:")
    print("1. Download frontend-model-v1.pt")
    print("2. Create Phase 3C notebook")
    print("3. Upload model to Phase 3C")
    print("4. Run Phase 3C training (Frameworks)")
    print("\n" + "=" * 70)

    return True


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
