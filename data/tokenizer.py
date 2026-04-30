"""Tokenizer for code data."""
from tokenizers import ByteLevelBPETokenizer
import os


class CodeTokenizer:
    """Byte-level BPE tokenizer for code."""

    def __init__(self, config):
        self.config = config
        self.vocab_size = config.get("vocab_size", 32000)
        self.tokenizer = ByteLevelBPETokenizer()

    def train(self, files):
        """Train tokenizer on code files.

        Args:
            files: List of file paths to train on
        """
        self.tokenizer.train(
            files=files,
            vocab_size=self.vocab_size,
            min_frequency=2,
            special_tokens=[
                "<|endoftext|>",
                "<|padding|>",
                "<|fim_prefix|>",
                "<|fim_middle|>",
                "<|fim_suffix|>",
            ],
        )

    def encode(self, text):
        """Encode text to token IDs.

        Args:
            text: Text to encode

        Returns:
            List of token IDs
        """
        encoding = self.tokenizer.encode(text)
        return encoding.ids

    def decode(self, ids):
        """Decode token IDs to text.

        Args:
            ids: List of token IDs

        Returns:
            Decoded text
        """
        return self.tokenizer.decode(ids)

    def save(self, path):
        """Save tokenizer to disk.

        Args:
            path: Directory to save tokenizer
        """
        os.makedirs(path, exist_ok=True)
        self.tokenizer.save_model(path)

    def load(self, path):
        """Load tokenizer from disk.

        Args:
            path: Directory containing tokenizer files
        """
        self.tokenizer = ByteLevelBPETokenizer(
            f"{path}/vocab.json",
            f"{path}/merges.txt"
        )
