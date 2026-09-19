# Plant Disease Classification - Backend

Complete backend API for plant disease detection using deep learning.

## Features

- MobileNetV2-based transfer learning model
- 38+ plant disease classes detection
- REST API with FastAPI
- Image preprocessing pipeline
- Real-time predictions with confidence scores
- Treatment recommendations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset

Ensure your dataset is structured as:
```
data/
├── train/
│   ├── Apple___Apple_scab/
│   ├── Apple___Black_rot/
│   ├── Tomato___Early_blight/
│   └── ... (38 classes total)
└── test/
    └── test/
        └── ... (test images)
```

### 3. Train the Model

```bash
python backend/train_model.py
```

Training will:
- Load and augment training data
- Create MobileNetV2 transfer learning model
- Train for up to 50 epochs with early stopping
- Save best model to `backend/model/plant_model.h5`
- Save class mappings to `backend/model/classes.json`
- Save training history for analysis

Expected training time:
- GPU: 2-4 hours
- CPU: 8-12 hours

### 4. Run the API Server

```bash
python backend/app.py
```

Or with uvicorn:
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "ok",
  "api": "AgroScan",
  "model_loaded": true
}
```

### Predict Disease
```
POST /predict
Content-Type: multipart/form-data
```

Parameters:
- `file`: Image file (JPG, PNG)

Response:
```json
{
  "disease": "Tomato - Early blight",
  "confidence": 95.67,
  "is_healthy": false,
  "advice": "Improve air circulation, mulch soil, rotate crops, apply fungicides if severe.",
  "source": "AI Model"
}
```

## Model Architecture

- Base: MobileNetV2 (pre-trained on ImageNet)
- Input: 224x224x3 RGB images
- Custom layers:
  - GlobalAveragePooling2D
  - Dropout (0.3)
  - Dense (512, ReLU)
  - Dropout (0.3)
  - Dense (38, Softmax)

## Training Configuration

- Optimizer: Adam (lr=0.0001)
- Loss: Categorical Crossentropy
- Metrics: Accuracy, Top-3 Accuracy
- Batch Size: 32
- Epochs: 50 (with early stopping)
- Data Split: 80% train, 20% validation

## Data Augmentation

- Rotation: ±20°
- Width/Height Shift: ±20%
- Shear: 20%
- Zoom: 20%
- Horizontal Flip: Yes

## Files Structure

```
backend/
├── app.py                 # FastAPI application
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── model/                 # Model artifacts (created after training)
│   ├── plant_model.h5    # Trained model
│   ├── classes.json      # Class mappings
│   └── training_history.json
└── utils/
    └── preprocess.py     # Image preprocessing
```

## Troubleshooting

### GPU Not Detected
If training on CPU is too slow, ensure TensorFlow GPU is properly installed:
```bash
pip install tensorflow-gpu==2.13.0
```

### Out of Memory
Reduce batch size in `train_model.py`:
```python
BATCH_SIZE = 16  # or 8
```

### Model Not Loading
Ensure you've completed training and the model file exists:
```bash
ls backend/model/plant_model.h5
```

## Performance Expectations

Expected validation accuracy: 92-96%
Expected top-3 accuracy: 98-99%

## License

MIT
