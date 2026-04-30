# Phase 4: Cloud GPU Training

## Overview

Phase 4 scales training to cloud GPUs for full-dataset training (100K+ samples).

**Goals:**
1. Set up cloud GPU environment
2. Implement distributed training
3. Train on full dataset
4. Monitor and optimize

## Cloud Options

### AWS (Recommended)

**Setup:**
```bash
# Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type g4dn.xlarge \
  --key-name my-key

# Connect
ssh -i my-key.pem ec2-user@instance-ip
```

**Instance Types:**
- `g4dn.xlarge` - 1x NVIDIA T4 GPU (16GB VRAM)
- `g4dn.2xlarge` - 1x NVIDIA T4 GPU (16GB VRAM)
- `p3.2xlarge` - 1x NVIDIA V100 GPU (32GB VRAM)

### Google Cloud

**Setup:**
```bash
# Create VM with GPU
gcloud compute instances create code-model \
  --machine-type n1-standard-4 \
  --accelerator type=nvidia-tesla-t4,count=1 \
  --image-family pytorch-latest-gpu \
  --image-project deeplearning-platform-release

# Connect
gcloud compute ssh code-model
```

### Azure

**Setup:**
```bash
# Create VM with GPU
az vm create \
  --resource-group myResourceGroup \
  --name code-model \
  --image UbuntuLTS \
  --size Standard_NC6
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install CUDA (if not pre-installed)
sudo apt-get install -y cuda-toolkit-11-8

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Clone Repository

```bash
git clone <your-repo-url>
cd code-model
```

### 3. Download Dataset

```bash
# Download The Stack v2
python scripts/download_dataset.py

# Process dataset
python scripts/process_dataset.py
```

### 4. Start Training

```bash
# Single GPU training
python scripts/train_distributed.py

# Multi-GPU training (if available)
python -m torch.distributed.launch \
  --nproc_per_node=2 \
  scripts/train_distributed.py
```

## Distributed Training Script

Create `scripts/train_distributed.py`:

```python
"""Distributed training script."""
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from datasets import load_from_disk
from models.architecture import CodeModel
from training.trainer import CodeModelTrainer
import yaml
import sys

def setup_distributed():
    """Setup distributed training."""
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        dist.init_process_group("nccl")
        torch.cuda.set_device(rank)
        return rank, world_size
    return 0, 1

def main():
    """Distributed training pipeline."""
    print("=" * 60)
    print("PHASE 4: DISTRIBUTED TRAINING")
    print("=" * 60)
    
    # Setup distributed
    rank, world_size = setup_distributed()
    
    # Load config
    print("\n1. Loading configuration...")
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    print("   ✓ Config loaded")
    
    # Load dataset
    print("\n2. Loading dataset...")
    dataset = load_from_disk("data/processed")
    print(f"   ✓ Loaded {len(dataset)} samples")
    
    # Create model
    print("\n3. Creating model...")
    model = CodeModel(config["model"]).get_model()
    if world_size > 1:
        model = DDP(model)
    print(f"   ✓ Model created")
    
    # Train
    print("\n4. Starting training...")
    trainer = CodeModelTrainer(model, config, dataset)
    trainer.train()
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

## Monitoring

### Track Training

```bash
# Monitor GPU usage
watch -n 1 nvidia-smi

# Monitor training logs
tail -f outputs/logs/training.json

# Monitor disk usage
df -h
```

### Save Checkpoints

```bash
# Checkpoints saved automatically
ls -la outputs/checkpoints/

# Resume from checkpoint
python scripts/train_distributed.py --resume outputs/checkpoints/epoch_5.pt
```

## Performance Optimization

### Batch Size

```yaml
# Adjust for your GPU
training:
  batch_size: 64      # T4: 32-64
                      # V100: 64-128
                      # A100: 128-256
```

### Gradient Accumulation

```python
# For larger effective batch size
accumulation_steps = 4
for i, batch in enumerate(dataloader):
    loss = model(batch)
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### Mixed Precision

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for batch in dataloader:
    with autocast():
        loss = model(batch)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

## Expected Results

### Training Time
- **T4 GPU:** 2-4 hours per epoch (100K samples)
- **V100 GPU:** 1-2 hours per epoch
- **A100 GPU:** 30-60 minutes per epoch

### Loss Progression
- **Epoch 1:** Loss ~4-6
- **Epoch 2:** Loss ~3-4
- **Epoch 3:** Loss ~2-3

### Final Model
- **Size:** 111M parameters
- **Accuracy:** 70-80% on code completion
- **Inference Speed:** 50-100 tokens/sec

## Cost Estimation

### AWS
- **g4dn.xlarge:** $0.35/hour
- **Training (3 epochs):** ~$4-6
- **Storage:** ~$0.50/month

### Google Cloud
- **n1-standard-4 + T4:** ~$0.30/hour
- **Training (3 epochs):** ~$3-5
- **Storage:** ~$0.50/month

## Troubleshooting

### Out of Memory
```yaml
training:
  batch_size: 16  # Reduce batch size
```

### Slow Training
- Check GPU utilization: `nvidia-smi`
- Increase batch size if GPU not saturated
- Use mixed precision training

### Training Diverges
- Reduce learning rate: `learning_rate: 1e-4`
- Use gradient clipping
- Check data quality

## Next Steps

1. **Evaluate Model**
   - Run benchmarks
   - Compare with baselines
   - Analyze errors

2. **Phase 5: Evaluation**
   - Code completion tasks
   - Code generation tasks
   - Performance metrics

3. **Phase 6: Deployment**
   - Export model
   - Create API
   - Deploy to production

---

**Status:** Phase 4 - Cloud GPU Training
