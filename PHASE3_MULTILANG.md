# Phase 3: Multi-Language Dataset Preparation

## Overview

Phase 3 builds a universal coding model through incremental training on multiple languages and frameworks. Instead of training all at once, we use **transfer learning** to progressively add knowledge.

**Timeline:** 5-6 weeks | **GPU Hours:** 60-90 | **Samples:** ~200K

---

## Phase 3A: Foundation Model (JavaScript + Python)

### Duration
1-2 weeks

### Dataset
- **JavaScript:** 40K samples
  - Core JS (functions, classes, async/await, promises)
  - React (components, hooks, state management)
  - Node.js/Express (backend patterns)
  
- **Python:** 30K samples
  - Data science (pandas, numpy, scikit-learn)
  - Web frameworks (Django, Flask)
  - Utilities and scripts

- **Total:** 70K samples, ~500MB

### Training
```bash
# Google Colab
1. Create new notebook
2. Change runtime to GPU (T4)
3. Upload Phase 3A notebook
4. Run all cells
5. Download foundation-model-v1.pt
```

### Configuration
- **Batch size:** 16
- **Learning rate:** 5e-4
- **Epochs:** 2
- **Time:** 20-30 GPU hours

### Expected Results
- Initial loss: ~8-9
- Final loss: ~2-3
- Model size: 445 MB
- Knowledge: JavaScript + Python

### Output
`outputs/models/foundation-model-v1.pt`

---

## Phase 3B: Frontend Stack (HTML + CSS)

### Duration
1 week

### Dataset
- **HTML:** 15K samples
  - Semantic markup
  - Forms and accessibility
  - Components and patterns
  
- **CSS:** 15K samples
  - Flexbox and Grid
  - Responsive design
  - Animations and transitions

- **Total:** 30K samples, ~200MB

### Training
```bash
# Google Colab
1. Create new notebook
2. Upload Phase 3B notebook
3. Upload foundation-model-v1.pt from Phase 3A
4. Run all cells
5. Download frontend-model-v1.pt
```

### Configuration
- **Batch size:** 16
- **Learning rate:** 1e-5 (lower for fine-tuning)
- **Epochs:** 1
- **Time:** 10-15 GPU hours

### Expected Results
- Initial loss: ~3.5 (from Phase 3A)
- Final loss: ~1.5-2.0
- Model size: 445 MB
- Knowledge: JS + Python + HTML + CSS

### Output
`outputs/models/frontend-model-v1.pt`

---

## Phase 3C: Full-Stack Integration

### Duration
1 week

### Dataset
- **React/Vue/Angular:** 10K samples
- **Backend Frameworks:** 10K samples (Express, Django, Flask)
- **Databases:** 5K samples (SQL, MongoDB)
- **APIs & Integration:** 5K samples (REST, GraphQL, JWT)

- **Total:** 30K samples, ~200MB

### Training
```bash
# Google Colab
1. Create new notebook
2. Upload Phase 3C notebook
3. Upload frontend-model-v1.pt from Phase 3B
4. Run all cells
5. Download fullstack-model-v1.pt
```

### Configuration
- **Batch size:** 16
- **Learning rate:** 5e-6 (very low for fine-tuning)
- **Epochs:** 1
- **Time:** 10-15 GPU hours

### Expected Results
- Initial loss: ~2.0 (from Phase 3B)
- Final loss: ~1.0-1.5
- Model size: 445 MB
- Knowledge: JS + Python + HTML + CSS + Frameworks + Databases + APIs

### Output
`outputs/models/fullstack-model-v1.pt`

---

## Phase 3D: Extended Languages

### Duration
2 weeks

### Dataset
- **TypeScript:** 30K samples
- **Java:** 30K samples
- **Go:** 25K samples
- **Rust:** 25K samples
- **C#:** 20K samples
- **SQL:** 30K samples

- **Total:** 160K samples, ~1GB

### Training
```bash
# Google Colab
1. Create new notebook
2. Upload Phase 3D notebook
3. Upload fullstack-model-v1.pt from Phase 3C
4. Run all cells
5. Download universal-model-v1.pt
```

### Configuration
- **Batch size:** 16
- **Learning rate:** 1e-6 (extremely low for fine-tuning)
- **Epochs:** 1
- **Time:** 20-30 GPU hours

### Expected Results
- Initial loss: ~1.5 (from Phase 3C)
- Final loss: ~0.8-1.2
- Model size: 445 MB
- Knowledge: All languages and frameworks

### Output
`outputs/models/universal-model-v1.pt`

---

## Learning Rate Progression

Lower learning rates preserve prior knowledge while learning new patterns:

| Phase | LR | Purpose |
|-------|-----|---------|
| 3A | 5e-4 | Foundation training |
| 3B | 1e-5 | Fine-tune (add HTML+CSS) |
| 3C | 5e-6 | Fine-tune (add frameworks) |
| 3D | 1e-6 | Fine-tune (add languages) |

---

## Colab Notebooks

### Phase 3A: Foundation
- **File:** `notebooks/phase3a_foundation.ipynb`
- **Dataset:** JavaScript + Python
- **Checkpoint:** None (training from scratch)
- **Output:** `foundation-model-v1.pt`

### Phase 3B: Frontend
- **File:** `notebooks/phase3b_frontend.ipynb`
- **Dataset:** HTML + CSS
- **Checkpoint:** `foundation-model-v1.pt`
- **Output:** `frontend-model-v1.pt`

### Phase 3C: Full-Stack
- **File:** `notebooks/phase3c_fullstack.ipynb`
- **Dataset:** React, Express, Django, Flask, Databases, APIs
- **Checkpoint:** `frontend-model-v1.pt`
- **Output:** `fullstack-model-v1.pt`

### Phase 3D: Extended Languages
- **File:** `notebooks/phase3d_extended_languages.ipynb`
- **Dataset:** TypeScript, Java, Go, Rust, C#, SQL
- **Checkpoint:** `fullstack-model-v1.pt`
- **Output:** `universal-model-v1.pt`

---

## Configuration Files

Each phase has its own configuration:

- `config-phase3a.yaml` - Foundation (LR: 5e-4)
- `config-phase3b.yaml` - Frontend (LR: 1e-5)
- `config-phase3c.yaml` - Full-Stack (LR: 5e-6)
- `config-phase3d.yaml` - Extended (LR: 1e-6)

---

## Resource Optimization

### For Google Colab (Free GPU)

**Colab Strategy:**
- 12-hour session limit → Save checkpoint every 2 hours
- Use gradient accumulation (4 steps) to simulate larger batch size
- Use mixed precision (fp16) to reduce memory
- Batch size: 16 (fits in 16GB T4 VRAM)

**Memory Optimization:**
```yaml
training:
  batch_size: 16
  gradient_accumulation_steps: 4  # Effective batch: 64
  fp16: true  # Mixed precision
  max_grad_norm: 1.0  # Gradient clipping
```

### For Kaggle Notebooks (Free GPU)

**Kaggle Strategy:**
- 30 hours/week GPU → Run 2-3 phases per week
- Larger batch size possible (32-64)
- More stable training (no session interruptions)

---

## Checkpoint Resumption

If training is interrupted:

```python
# Load checkpoint
model.load_state_dict(torch.load("outputs/models/foundation-model-v1.pt"))

# Resume training
trainer = CodeModelTrainer(model, config, samples)
trainer.train()
```

---

## Verification Checklist

### Phase 3A
- [ ] Synthetic dataset created (1K samples)
- [ ] Real dataset downloaded (70K samples)
- [ ] Data cleaned and filtered (60K valid)
- [ ] Training runs without errors
- [ ] Loss decreases over epochs
- [ ] Model checkpoint saved
- [ ] Can load and run inference

### Phase 3B
- [ ] Load Phase 3A checkpoint
- [ ] Fine-tune on HTML+CSS
- [ ] Loss decreases (lower than Phase 3A)
- [ ] Model checkpoint saved
- [ ] Can generate HTML+CSS code

### Phase 3C
- [ ] Load Phase 3B checkpoint
- [ ] Fine-tune on frameworks
- [ ] Loss decreases
- [ ] Model checkpoint saved
- [ ] Can generate React/Express code

### Phase 3D
- [ ] Load Phase 3C checkpoint
- [ ] Fine-tune on extended languages
- [ ] Loss decreases
- [ ] Model checkpoint saved
- [ ] Can generate code in all languages

---

## Success Criteria

### Phase 3A (Foundation)
- Loss: 2.0-3.0 (after 2 epochs)
- Perplexity: 7-20
- Can generate valid JS and Python code

### Phase 3B (Frontend)
- Loss: 1.5-2.5 (after 1 epoch)
- Perplexity: 5-12
- Can generate valid HTML and CSS

### Phase 3C (Full-Stack)
- Loss: 1.0-2.0 (after 1 epoch)
- Perplexity: 3-8
- Can generate React components and Express routes

### Phase 3D (Universal)
- Loss: 0.8-1.5 (after 1 epoch)
- Perplexity: 2-5
- Can generate code in all supported languages

---

## Troubleshooting

### "CUDA out of memory"
```yaml
training:
  batch_size: 8  # Reduce from 16
  gradient_accumulation_steps: 8  # Increase accumulation
```

### "Training is slow"
- Check GPU utilization: `nvidia-smi`
- Increase batch size if GPU not saturated
- Use mixed precision (fp16: true)

### "Model not improving"
- Check learning rate (may be too high)
- Verify data quality
- Check for data leakage

### "Checkpoint not found"
- Verify file path is correct
- Check outputs/models/ directory exists
- Ensure previous phase completed successfully

---

## Next Steps

After Phase 3D completes:

1. **Phase 4: Cloud GPU Training (Optional)**
   - Use AWS/GCP/Azure for faster training
   - Train on 500K+ samples
   - Implement distributed training

2. **Phase 5: Evaluation**
   - Benchmark on code completion tasks
   - Compare with baselines
   - Analyze errors

3. **Phase 6: Deployment**
   - Export to ONNX format
   - Create inference API
   - Deploy to production

---

## Summary

| Phase | Duration | GPU Hours | Samples | Output |
|-------|----------|-----------|---------|--------|
| 3A | 1-2 weeks | 20-30 | 70K | foundation-model-v1.pt |
| 3B | 1 week | 10-15 | 30K | frontend-model-v1.pt |
| 3C | 1 week | 10-15 | 30K | fullstack-model-v1.pt |
| 3D | 2 weeks | 20-30 | 160K | universal-model-v1.pt |
| **Total** | **5-6 weeks** | **60-90** | **~200K** | **Universal Model** |

---

**Status:** Phase 3 - Multi-Language Dataset Preparation
