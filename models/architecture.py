"""Model architecture definition."""
from transformers import GPT2Config, GPT2LMHeadModel


class CodeModel:
    """GPT-2 style code generation model."""

    def __init__(self, config):
        """Initialize model with config.

        Args:
            config: Model configuration dict
        """
        self.config = config
        self.model_config = GPT2Config(
            vocab_size=config.get("vocab_size", 32000),
            n_positions=config.get("n_positions", 2048),
            n_embd=config.get("n_embd", 768),
            n_layer=config.get("n_layer", 12),
            n_head=config.get("n_head", 12),
            activation_function=config.get("activation_function", "gelu_new"),
        )
        self.model = GPT2LMHeadModel(self.model_config)

    def get_model(self):
        """Get the underlying model."""
        return self.model

    def num_parameters(self):
        """Get total number of parameters."""
        return sum(p.numel() for p in self.model.parameters())

    def num_parameters_millions(self):
        """Get total parameters in millions."""
        return self.num_parameters() / 1e6
