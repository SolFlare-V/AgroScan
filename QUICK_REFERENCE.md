# Quick Reference Card

## 🚀 Essential Commands

### Setup
```bash
pip install -r backend/requirements.txt
```

### Training (Choose One)

**Option 1: Automated (Recommended)**
```bash
python start_training.py
```

**Option 2: Manual**
```bash
python backend/verify_dataset.py    # Verify data
python backend/train_model.py       # Train model
python backend/test_model.py        # Test model
python backend/visualize_training.py # View results
```

### Running API
```bash
python backend/app.py
# or
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### Testing API
```bash
# Health check
curl http://localhost:8000/health

# Predict disease
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/image.jpg"

# Interactive docs
open http://localhost:8000/docs
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/train_model.py` | Train the model |
| `backend/app.py` | API server |
| `backend/test_model.py` | Test predictions |
| `backend/verify_dataset.py` | Check dataset |
| `start_training.py` | One-command training |

## 🎯 Training Parameters

Edit in `backend/train_model.py`:

```python
IMG_SIZE = 224        # Image size
BATCH_SIZE = 32       # Batch size (reduce if OOM)
EPOCHS = 50           # Max epochs
LEARNING_RATE = 0.0001 # Learning rate
```

## 📊 Expected Performance

- **Accuracy**: 92-96%
- **Training Time (GPU)**: 2-4 hours
- **Training Time (CPU)**: 8-12 hours
- **Model Size**: ~100MB
- **Inference**: <100ms

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Out of memory | Reduce `BATCH_SIZE` to 16 or 8 |
| Training too slow | Use GPU or reduce `EPOCHS` |
| Model not found | Run training first |
| Low accuracy | Train longer or increase augmentation |

## 📂 Output Files

After training:
```
backend/model/
├── plant_model.h5           # Trained model
├── classes.json             # Class mappings
├── training_history.json    # Metrics
└── training_plot.png        # Visualization
```

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check status |
| `/predict` | POST | Predict disease |
| `/docs` | GET | API documentation |

## 💡 Quick Tips

1. **Always verify dataset first**: `python backend/verify_dataset.py`
2. **Monitor training**: Watch accuracy and loss curves
3. **Use GPU**: 10-20x faster than CPU
4. **Test before deploying**: `python backend/test_model.py`
5. **Check model exists**: `ls backend/model/plant_model.h5`

## 🎓 Training Workflow

```
1. Verify Dataset → 2. Train Model → 3. Test Model → 4. Run API
```

## 📞 Need Help?

1. Check error messages
2. Read TRAINING_GUIDE.md
3. Review IMPLEMENTATION_SUMMARY.md
4. Check dataset structure
5. Verify dependencies installed

## ✅ Pre-Training Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Dataset extracted to `data/train/`
- [ ] At least 2GB free disk space
- [ ] 8GB+ RAM available

## 🎉 Success Indicators

After training, you should see:
- ✓ `backend/model/plant_model.h5` exists (~100MB)
- ✓ Validation accuracy > 90%
- ✓ API server starts without errors
- ✓ Predictions work on test images

---

**Ready to start?** Run: `python start_training.py`
