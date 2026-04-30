"""Training utilities for code model."""
import torch
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
from tqdm import tqdm
import json
from pathlib import Path


class CodeDataset(Dataset):
    """PyTorch dataset for code samples."""

    def __init__(self, dataset, tokenizer, max_length=512):
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        code = self.dataset[idx]["content"]
        tokens = self.tokenizer.encode(code)

        # Truncate or pad
        if len(tokens) > self.max_length:
            tokens = tokens[:self.max_length]
        else:
            tokens = tokens + [0] * (self.max_length - len(tokens))

        return {
            "input_ids": torch.tensor(tokens, dtype=torch.long),
            "labels": torch.tensor(tokens, dtype=torch.long),
        }


class CodeModelTrainer:
    """Trainer for code model."""

    def __init__(self, model, config, dataset, output_dir="outputs"):
        self.model = model
        self.config = config
        self.dataset = dataset
        self.output_dir = output_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

        # Get learning rate and ensure it's a float
        lr = config["training"].get("learning_rate", 5e-4)
        if isinstance(lr, str):
            lr = float(lr)

        self.optimizer = AdamW(
            self.model.parameters(),
            lr=lr
        )
        self.logs = []

    def train(self):
        """Train the model."""
        from data.tokenizer import CodeTokenizer

        num_epochs = self.config["training"].get("num_epochs", 1)
        batch_size = self.config["training"].get("batch_size", 8)
        max_length = self.config["model"].get("n_positions", 512)

        # Create tokenizer
        tokenizer = CodeTokenizer(self.config["model"])

        # Create PyTorch dataset
        torch_dataset = CodeDataset(
            self.dataset,
            tokenizer=tokenizer,
            max_length=max_length
        )

        # Create dataloader
        dataloader = DataLoader(
            torch_dataset,
            batch_size=batch_size,
            shuffle=True
        )

        # Training loop
        self.model.train()
        for epoch in range(num_epochs):
            total_loss = 0
            progress_bar = tqdm(dataloader, desc=f"Epoch {epoch+1}/{num_epochs}")

            for batch in progress_bar:
                input_ids = batch["input_ids"].to(self.device)
                labels = batch["labels"].to(self.device)

                # Forward pass
                outputs = self.model(input_ids, labels=labels)
                loss = outputs.loss

                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                progress_bar.set_postfix({"loss": loss.item()})

            avg_loss = total_loss / len(dataloader)
            self.logs.append({
                "epoch": epoch + 1,
                "avg_loss": avg_loss
            })

            print(f"Epoch {epoch+1} - Avg Loss: {avg_loss:.4f}")

        # Save logs
        self.save_logs()

    def save_logs(self):
        """Save training logs."""
        log_path = f"{self.output_dir}/logs/training.json"
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(self.logs, f, indent=2)
