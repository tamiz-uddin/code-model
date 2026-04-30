#!/usr/bin/env python3
"""
Phase 3C: Full-Stack Integration Training
Fine-tune on React, Express, Django, Flask, Databases, APIs

Usage:
    python train_phase3c.py
"""

import sys
import torch
import yaml
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from models.architecture import CodeModel
from training.trainer import CodeModelTrainer


def main():
    """Train Phase 3C model."""
    print("=" * 70)
    print("PHASE 3C: FULL-STACK INTEGRATION TRAINING")
    print("=" * 70)

    # Check GPU
    print("\n1. Checking GPU...")
    print(f"   GPU Available: {torch.cuda.is_available()}")

    # Load config
    print("\n2. Loading configuration...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    config["training"]["batch_size"] = 16
    config["training"]["num_epochs"] = 1
    config["training"]["learning_rate"] = 5e-6  # Even lower for fine-tuning

    print(f"   Learning rate: {config['training']['learning_rate']} (fine-tuning)")

    # Load Phase 3B model
    print("\n3. Loading Phase 3B checkpoint...")
    model = CodeModel(config["model"]).get_model()
    model_path = Path("outputs/models/frontend-model-v1.pt")

    if not model_path.exists():
        print(f"   ⚠ Model not found: {model_path}")
        print("   Run Phase 3B first!")
        return False

    model.load_state_dict(torch.load(model_path))
    print(f"   ✓ Loaded {model_path}")

    # Create dataset
    print("\n4. Creating full-stack dataset...")
    code_samples = [
        # React
        "function Counter() { const [count, setCount] = useState(0); return <button onClick={() => setCount(count + 1)}>{count}</button>; }",
        "const TodoList = ({ todos }) => todos.map(todo => <li key={todo.id}>{todo.text}</li>);",
        "useEffect(() => { fetchData(); }, []);",
        "const [state, dispatch] = useReducer(reducer, initialState);",

        # Express
        "app.get('/api/users', (req, res) => { res.json(users); });",
        "app.post('/api/users', (req, res) => { const user = req.body; users.push(user); res.json(user); });",
        "app.use(express.json());",
        "app.use((err, req, res, next) => { res.status(500).json({ error: err.message }); });",

        # Django
        "class UserViewSet(viewsets.ModelViewSet): queryset = User.objects.all(); serializer_class = UserSerializer",
        "path('api/users/', views.user_list, name='user-list'),",
        "def user_detail(request, pk): user = get_object_or_404(User, pk=pk); return JsonResponse(model_to_dict(user))",
        "@api_view(['GET', 'POST']) def user_list(request): pass",

        # Flask
        "@app.route('/api/users', methods=['GET']) def get_users(): return jsonify(users)",
        "@app.route('/api/users', methods=['POST']) def create_user(): user = request.json; users.append(user); return jsonify(user)",
        "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'",
        "db = SQLAlchemy(app)",

        # SQL
        "SELECT * FROM users WHERE age > 18 ORDER BY name;",
        "INSERT INTO users (name, email, age) VALUES ('John', 'john@example.com', 30);",
        "UPDATE users SET age = 31 WHERE id = 1;",
        "DELETE FROM users WHERE id = 1;",

        # MongoDB
        "db.users.find({ age: { $gt: 18 } });",
        "db.users.insertOne({ name: 'John', email: 'john@example.com' });",
        "db.users.updateOne({ _id: 1 }, { $set: { age: 30 } });",
        "db.users.deleteOne({ _id: 1 });",

        # REST API
        "GET /api/users - Get all users",
        "POST /api/users - Create user",
        "GET /api/users/:id - Get user by ID",
        "PUT /api/users/:id - Update user",

        # GraphQL
        "query { users { id name email } }",
        "mutation { createUser(name: 'John', email: 'john@example.com') { id name } }",
        "subscription { userCreated { id name } }",

        # JWT
        "const token = jwt.sign({ userId: user.id }, 'secret', { expiresIn: '1h' });",
        "const decoded = jwt.verify(token, 'secret');",
    ]

    code_samples = code_samples * 2  # 60 samples

    # Convert to dataset format
    samples = [{"content": code} for code in code_samples]

    print(f"   ✓ Created {len(samples)} samples")
    print(f"   React, Express, Django, Flask, SQL, MongoDB, APIs")

    # Train
    print("\n5. Starting fine-tuning...")
    trainer = CodeModelTrainer(model, config, samples)
    trainer.train()

    # Save model
    print("\n6. Saving model...")
    output_dir = Path("outputs/models")
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = output_dir / "fullstack-model-v1.pt"
    torch.save(model.state_dict(), model_path)

    file_size = model_path.stat().st_size / 1e6
    print(f"   ✓ Saved to {model_path}")
    print(f"   Size: {file_size:.1f} MB")

    # Summary
    print("\n" + "=" * 70)
    print("✅ PHASE 3C TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nModel: {model_path}")
    print(f"Size: {file_size:.1f} MB")
    print("\nNext steps:")
    print("1. Download fullstack-model-v1.pt")
    print("2. Create Phase 3D notebook")
    print("3. Upload model to Phase 3D")
    print("4. Run Phase 3D training (Extended Languages)")
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
