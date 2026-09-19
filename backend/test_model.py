"""
Test the trained model on sample images
"""
import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path

MODEL_PATH = "backend/model/plant_model.h5"
CLASSES_PATH = "backend/model/classes.json"
TEST_DIR = "data/test/test"

def load_model_and_classes():
    """Load trained model and class mappings"""
    if not os.path.exists(MODEL_PATH):
        print(f"✗ Model not found: {MODEL_PATH}")
        print("  Please train the model first: python backend/train_model.py")
        return None, None
    
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✓ Model loaded from {MODEL_PATH}")
    
    if not os.path.exists(CLASSES_PATH):
        print(f"✗ Classes file not found: {CLASSES_PATH}")
        return model, None
    
    with open(CLASSES_PATH, 'r') as f:
        class_names = json.load(f)
    print(f"✓ Loaded {len(class_names)} classes")
    
    return model, class_names

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(model, class_names, image_path):
    """Make prediction on a single image"""
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array, verbose=0)
    
    # Get top 3 predictions
    top_3_idx = np.argsort(predictions[0])[-3:][::-1]
    
    results = []
    for idx in top_3_idx:
        class_name = class_names.get(str(idx), "Unknown")
        confidence = predictions[0][idx]
        results.append((class_name, confidence))
    
    return results

def test_model():
    """Test model on sample images"""
    print("=" * 70)
    print("Model Testing")
    print("=" * 70)
    
    # Load model
    model, class_names = load_model_and_classes()
    if model is None or class_names is None:
        return
    
    # Get test images
    if not os.path.exists(TEST_DIR):
        print(f"\n✗ Test directory not found: {TEST_DIR}")
        return
    
    test_images = [f for f in os.listdir(TEST_DIR) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not test_images:
        print(f"\n✗ No test images found in {TEST_DIR}")
        return
    
    print(f"\n✓ Found {len(test_images)} test images")
    print("\nTesting on sample images...")
    print("=" * 70)
    
    # Test on first 10 images
    for i, img_name in enumerate(test_images[:10], 1):
        img_path = os.path.join(TEST_DIR, img_name)
        
        print(f"\n[{i}] {img_name}")
        print("-" * 70)
        
        try:
            results = predict_image(model, class_names, img_path)
            
            print("Top 3 Predictions:")
            for rank, (class_name, confidence) in enumerate(results, 1):
                display_name = class_name.replace("___", " - ").replace("_", " ")
                print(f"  {rank}. {display_name:<45} {confidence*100:>6.2f}%")
            
            # Check if prediction matches filename
            predicted_class = results[0][0]
            if any(part.lower() in img_name.lower() 
                   for part in predicted_class.split("___")):
                print("  ✓ Prediction matches filename!")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_model()
