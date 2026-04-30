#!/usr/bin/env python3
"""
Phase 3D: Extended Languages Training Script
Fine-tune on TypeScript, Java, Go, Rust, C#, SQL

Usage:
    python train_phase3d.py --model outputs/models/fullstack-model-v1.pt
"""

import sys
import torch
import yaml
import argparse
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer


def create_dataset():
    """Create extended languages dataset for Phase 3D."""
    print("Creating extended languages dataset...")

    samples = [
        # TypeScript
        "interface User { id: number; name: string; email: string; }",
        "type Status = 'active' | 'inactive' | 'pending';",
        "function add<T extends number>(a: T, b: T): T { return (a + b) as T; }",
        "class UserService { constructor(private http: HttpClient) {} }",
        "async function fetchUser(id: number): Promise<User> { return await fetch(`/api/users/${id}`).then(r => r.json()); }",

        # Java
        "public class User { private int id; private String name; public User(int id, String name) { this.id = id; this.name = name; } }",
        "public interface UserRepository extends JpaRepository<User, Integer> { List<User> findByName(String name); }",
        "Stream<User> users = userList.stream().filter(u -> u.getAge() > 18).map(u -> u);",
        "@RestController @RequestMapping('/api/users') public class UserController { }",
        "public synchronized void updateUser(User user) { users.put(user.getId(), user); }",

        # Go
        "func Add(a, b int) int { return a + b }",
        "type User struct { ID int; Name string; Email string }",
        "func (u *User) String() string { return fmt.Sprintf('User: %s', u.Name) }",
        "go func() { fmt.Println('Running in goroutine') }()",
        "ch := make(chan int); go func() { ch <- 42 }(); value := <-ch",

        # Rust
        "fn add(a: i32, b: i32) -> i32 { a + b }",
        "struct User { id: u32, name: String, email: String }",
        "impl User { fn new(id: u32, name: String) -> User { User { id, name, email: String::new() } } }",
        "trait Drawable { fn draw(&self); }",
        "fn main() { let s = String::from('hello'); println!('{:?}', s); }",

        # C#
        "public class User { public int Id { get; set; } public string Name { get; set; } }",
        "public async Task<User> GetUserAsync(int id) { return await _userService.GetUserAsync(id); }",
        "var users = userList.Where(u => u.Age > 18).Select(u => u.Name).ToList();",
        "public delegate void UserEventHandler(User user);",
        "[HttpGet('{id}')] public ActionResult<User> GetUser(int id) { return Ok(user); }",

        # SQL Advanced
        "SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id HAVING COUNT(o.id) > 5;",
        "WITH user_orders AS (SELECT user_id, COUNT(*) as count FROM orders GROUP BY user_id) SELECT * FROM user_orders WHERE count > 10;",
        "SELECT ROW_NUMBER() OVER (ORDER BY age DESC) as rank, name, age FROM users;",
        "CREATE INDEX idx_user_email ON users(email);",
        "SELECT * FROM users WHERE name LIKE 'J%' AND age BETWEEN 20 AND 30;",
    ]

    samples = samples * 3  # 105 samples
    print(f"✓ Created {len(samples)} samples")
    return samples


def train_phase3d(model_path):
    """Train Phase 3D model."""
    print("=" * 60)
    print("PHASE 3D: EXTENDED LANGUAGES TRAINING")
    print("=" * 60)

    # Check GPU
    print("\n1. Checking GPU...")
    print(f"   GPU Available: {torch.cuda.is_available()}")

    # Load config
    print("\n2. Loading config...")
    try:
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {
            "model": {
                "vocab_size": 32000,
                "n_positions": 2048,
                "n_embd": 768,
                "n_layer": 12,
                "n_head": 12,
                "activation_function": "gelu_new"
            },
            "training": {
                "batch_size": 16,
                "learning_rate": 1e-6,
                "num_epochs": 1,
                "warmup_steps": 5,
                "weight_decay": 0.1,
                "fp16": True,
                "device": "cuda" if torch.cuda.is_available() else "cpu"
            }
        }

    config["training"]["batch_size"] = 16
    config["training"]["num_epochs"] = 1
    config["training"]["learning_rate"] = 1e-6  # Extremely low for fine-tuning

    print(f"   Batch size: {config['training']['batch_size']}")
    print(f"   Learning rate: {config['training']['learning_rate']} (fine-tuning)")
    print(f"   Epochs: {config['training']['num_epochs']}")

    # Create model
    print("\n3. Creating model...")
    model = CodeModel(config["model"]).get_model()
    print(f"   ✓ Model created")

    # Load Phase 3C checkpoint
    print("\n4. Loading Phase 3C checkpoint...")
    if Path(model_path).exists():
        model.load_state_dict(torch.load(model_path))
        print(f"   ✓ Loaded: {model_path}")
    else:
        print(f"   ⚠ Model not found: {model_path}")

    # Create dataset
    print("\n5. Creating dataset...")
    samples = create_dataset()
    print(f"   ✓ Dataset ready: {len(samples)} samples")

    # Train
    print("\n6. Starting fine-tuning...")
    trainer = CodeModelTrainer(model, config, samples)
    trainer.train()

    # Save model
    print("\n7. Saving model...")
    output_dir = Path("outputs/models")
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "universal-model-v1.pt"
    torch.save(model.state_dict(), model_path)
    print(f"   ✓ Saved to {model_path}")
    print(f"   Size: {model_path.stat().st_size / 1e6:.1f} MB")

    print("\n" + "=" * 60)
    print("✅ PHASE 3D TRAINING COMPLETE")
    print("=" * 60)
    print(f"\nUniversal Model ready: {model_path}")
    print("Next: Phase 4 (Evaluation)")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 3D: Extended Languages Training")
    parser.add_argument(
        "--model",
        type=str,
        default="outputs/models/fullstack-model-v1.pt",
        help="Path to Phase 3C model checkpoint"
    )
    args = parser.parse_args()

    try:
        success = train_phase3d(args.model)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
