"""Tests for model architecture."""
import pytest
from models.architecture import CodeModel


def test_model_initialization():
    """Test that model initializes correctly."""
    config = {
        "vocab_size": 32000,
        "n_positions": 2048,
        "n_embd": 768,
        "n_layer": 12,
        "n_head": 12,
    }
    model = CodeModel(config)

    assert model is not None
    assert model.get_model() is not None


def test_model_parameter_count():
    """Test that model has expected parameter count."""
    config = {
        "vocab_size": 32000,
        "n_positions": 2048,
        "n_embd": 768,
        "n_layer": 12,
        "n_head": 12,
    }
    model = CodeModel(config)

    params = model.num_parameters()
    params_millions = model.num_parameters_millions()

    assert params > 0
    assert params_millions > 100  # Should be ~125M
    assert params_millions < 200


def test_model_config_preserved():
    """Test that model config is preserved."""
    config = {
        "vocab_size": 32000,
        "n_positions": 2048,
        "n_embd": 768,
        "n_layer": 12,
        "n_head": 12,
    }
    model = CodeModel(config)

    assert model.model_config.vocab_size == 32000
    assert model.model_config.n_positions == 2048
    assert model.model_config.n_embd == 768
    assert model.model_config.n_layer == 12
    assert model.model_config.n_head == 12
