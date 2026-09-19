# Complete Model Training Guide

This guide will walk you through training a complete plant disease classification model.

## Prerequisites

- Python 3.8 or higher
- 8GB+ RAM (16GB recommended)
- GPU with CUDA support (optional but recommended)
- Dataset extracted in `data/` folder

## Step-by-Step Training Process

### Step 1: Verify Your Environment

Check Python version:
```bash
python --version
```

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

If you have a GPU:
```bash
pip install tensorflow-gpu==2.13.0
```

### Step 3: Verify Dataset

Run the dataset verification script:
```bash
python backend/verify_dataset.py
```

This will:
- Check if dataset is properly structured
- Show class distribution
- Count total images
- Identify any issues

Expected output:
```
✓ Found 38 disease classes
✓ Total training images: 70,000+
✓ Dataset is reasonably balanced
```

### Step 4: Train the Model

Start training:
```bash
python backend/train_model.py
```

Training process:
1. Loads and prepares data with augmentation
2. Creates MobileNetV2 transfer learning model
3. Trains for up to 50 epochs (early stopping enabled)
4. Saves best model automatically
5. Generates training history

Expected output:
```
[1/5] Loading and preparing data...
✓ Found 38 disease classes
✓ Training samples: 56,000+
✓ Validation samples: 14,000+

[2/5] Building model architecture...
✓ Model created with 38 output classes

[3/5] Compiling model...
✓ Model compiled

[4/5] Training model for up to 50 epochs...
Epoch 1/50
1750/1750 [==============================] - 120s - loss: 0.5234 - accuracy: 0.8456
...

[5/5] Final evaluation...
✓ Validation Accuracy: 94.23%
✓ Top-3 Accuracy: 98.67%
✓ Validation Loss: 0.2145

Training Complete!
Model saved to: backend/model/plant_model.h5
```

### Step 5: Test the Model

Test on sample images:
```bash
python backend/test_model.py
```

This will:
- Load the trained model
- Test on images from `data/test/test/`
- Show top-3 predictions with confidence scores

### Step 6: Run the API Server

Start the FastAPI server:
```bash
python backend/app.py
```

Or with uvicorn:
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Test the API:
```bash
curl http://localhost:8000/health
```

### Step 7: Test Predictions

You can test predictions using curl:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/test/test/TomatoEarlyBlight1.JPG"
```

Or visit the interactive API docs:
```
http://localhost:8000/docs
```

## Training Time Estimates

| Hardware | Expected Time |
|----------|---------------|
| GPU (NVIDIA RTX 3060+) | 2-4 hours |
| GPU (NVIDIA GTX 1060) | 4-6 hours |
| CPU (Modern i7/i9) | 8-12 hours |
| CPU (Older/i5) | 12-24 hours |

## Expected Performance

After training, you should achieve:
- Validation Accuracy: 92-96%
- Top-3 Accuracy: 98-99%
- Inference Time: <100ms per image

## Troubleshooting

### Issue: Out of Memory

Solution: Reduce batch size in `backend/train_model.py`:
```python
BATCH_SIZE = 16  # or even 8
```

### Issue: Training Too Slow

Solutions:
1. Use a GPU (10-20x faster)
2. Reduce number of epochs
3. Use a smaller model (reduce Dense layer size)

### Issue: Low Accuracy

Solutions:
1. Train for more epochs
2. Increase data augmentation
3. Unfreeze some base model layers for fine-tuning

### Issue: Model File Not Found

Make sure training completed successfully:
```bash
ls -lh backend/model/
```

You should see:
- `plant_model.h5` (100-150 MB)
- `classes.json`
- `training_history.json`

## Model Files

After training, these files are created:

```
backend/model/
├── plant_model.h5           # Trained model (100-150 MB)
├── classes.json             # Class index to name mapping
└── training_history.json    # Training metrics per epoch
```

## Next Steps

1. Integrate with frontend application
2. Deploy to production server
3. Monitor model performance
4. Collect feedback and retrain periodically

## Advanced Configuration

Edit `backend/train_model.py` to customize:

```python
# Image size (larger = more accurate but slower)
IMG_SIZE = 224  # Try 299 for better accuracy

# Batch size (larger = faster but needs more memory)
BATCH_SIZE = 32  # Reduce if out of memory

# Training epochs
EPOCHS = 50  # Increase for better accuracy

# Learning rate
LEARNING_RATE = 0.0001  # Lower for fine-tuning
```

## Support

If you encounter issues:
1. Check the error message carefully
2. Verify dataset structure
3. Ensure all dependencies are installed
4. Check available disk space (need 2GB+)
5. Monitor memory usage during training

## License

MIT
