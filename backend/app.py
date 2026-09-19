import os
import json
import random
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import uvicorn
from dotenv import load_dotenv
from backend.utils.preprocess import load_and_preprocess
from backend.utils.groq_api import get_groq_insight as get_hybrid_insight

# Load environment variables
load_dotenv()

app = FastAPI(title="AEROFARM API", version="1.0.0")

# Enable CORS for the frontend development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and class mappings
MODEL_PATH = "backend/model/plant_model.h5"
CLASSES_PATH = "backend/model/classes.json"
model = None
class_names = {}

if os.path.exists(MODEL_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("[INFO] Model loaded successfully.")
        
        # Load class mappings
        if os.path.exists(CLASSES_PATH):
            with open(CLASSES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"[INFO] Loaded {len(class_names)} disease classes.")
        else:
            print("[WARN] Class mappings not found. Model loaded but predictions may be incorrect.")
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
else:
    print(f"[WARN] Model file not found. Run 'python backend/train_model.py' to train the model.")

# Disease advice database
DISEASE_ADVICE = {
    "healthy": "The plant is looking great! Continue regular monitoring and proper care.",
    "Apple___Apple_scab": "Remove infected leaves, improve air circulation, and apply fungicides during wet periods.",
    "Apple___Black_rot": "Prune infected branches, remove mummified fruits, and apply fungicides preventively.",
    "Apple___Cedar_apple_rust": "Remove nearby cedar trees if possible, apply fungicides in spring.",
    "Blueberry___healthy": "Blueberry is healthy. Keep soil acidic and ensure adequate moisture.",
    "Cherry_(including_sour)___healthy": "Cherry tree is thriving. Maintain pruning and monitoring.",
    "Cherry_(including_sour)___Powdery_mildew": "Improve air circulation and apply sulfur-based fungicides if necessary.",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Rotate crops, till crop residue, and use resistant hybrids.",
    "Corn_(maize)___Common_rust_": "Plant resistant hybrids and apply fungicides if infection is severe.",
    "Corn_(maize)___Northern_Leaf_Blight": "Use resistant varieties and rotate crops to reduce residue.",
    "Grape___Black_rot": "Prune for better air circulation and remove mummified fruits.",
    "Grape___Esca_(Black_Measles)": "Prune infected wood and protect wounds. No effective chemical cure.",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Improve air flow and remove infected leaves to prevent spread.",
    "Orange___Haunglongbing_(Citrus_greening)": "Destroy infected trees to prevent spread. Control the Asian Citrus Psyllid.",
    "Peach___Bacterial_spot": "Apply copper-based sprays and choose resistant cultivars for new plantings.",
    "Pepper,_bell___Bacterial_spot": "Avoid overhead watering and apply bactericides like copper sprays.",
    "Potato___Early_blight": "Maintain plant vigor and use overhead irrigation early in the day.",
    "Potato___Late_blight": "Apply fungicides preventively and remove infected plants immediately.",
    "Squash___Powdery_mildew": "Apply neem oil or potassium bicarbonate-based sprays to infected areas.",
    "Strawberry___Leaf_scorch": "Remove old foliage and ensure adequate spacing for air circulation.",
    "Tomato___Bacterial_spot": "Remove infected leaves and apply copper-based bactericides.",
    "Tomato___Early_blight": "Rotate crops and apply fungicides. Avoid wetting the leaves.",
    "Tomato___Late_blight": "Remove and destroy infected plants. Use preventive fungicides.",
    "Tomato___Leaf_Mold": "Lower humidity and increase ventilation in greenhouses.",
    "Tomato___Septoria_leaf_spot": "Avoid overhead watering and remove lower leaves to reduce infection.",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Increase humidity and use insecticidal soaps or predatory mites.",
    "Tomato___Target_Spot": "Improve air circulation and use fungicides if the disease progresses.",
    "Tomato___Tomato_mosaic_virus": "Remove infected plants immediately and avoid handling plants after smoking.",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Control whitefly populations and use physical barriers like fine mesh.",
    "default": "Consult with a local agricultural extension office for specific treatment recommendations."
}

@app.get("/health")
def health_check():
    return {"status": "ok", "api": "AEROFARM", "model_loaded": model is not None}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    
    try:
        # Read file bytes
        contents = await file.read()
        
        # Preprocess the image
        processed_image = load_and_preprocess(contents)
        
        # Perform prediction
        if model and class_names:
            # Real model prediction
            predictions = model.predict(processed_image, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            print(f"[DEBUG] Predicted Index: {predicted_class_idx}, Confidence: {confidence:.4f}")
            
            # Get disease name
            disease_name = class_names.get(str(predicted_class_idx), "Unknown")
            
            # Check if healthy
            is_healthy = "healthy" in disease_name.lower()
            
            # Get advice
            advice = DISEASE_ADVICE.get(disease_name, DISEASE_ADVICE["default"])
            if is_healthy:
                advice = DISEASE_ADVICE["healthy"]
            
            # Format disease name for display
            display_name = disease_name.replace("___", " - ").replace("_", " ")
            
            # Get Hybrid Insight (Validation + Accuracy Correction + Expert Suggestions)
            hybrid_data = get_hybrid_insight(contents, display_name)
            
            # 1. Validation Logic: Stop if not a plant
            if not hybrid_data["is_leaf"]:
                return {
                    "disease": "Identity Verification Failed",
                    "confidence": 0.0,
                    "is_healthy": False,
                    "advice": "Security Alert: This system is optimized for botanical analysis only. The uploaded image does not appear to be a plant leaf.",
                    "gemini_advice": "No plant detected. Please upload a clear photo of the affected foliage.",
                    "source": "ML Sentinel"
                }

            # 2. Hybrid Accuracy Logic: Groq overrides local CNN if contradiction detected
            final_disease_name = hybrid_data["correct_name"]
            
            # Recalculate healthy status based on final name
            is_healthy = "healthy" in final_disease_name.lower()

            result = {
                "disease": final_disease_name,
                "confidence": round(confidence, 4),
                "is_healthy": is_healthy,
                "advice": advice if final_disease_name == display_name else f"ML Recognition: {final_disease_name} (Updated from: {display_name})",
                "gemini_advice": hybrid_data["gemini_advice"],
                "source": "AEROFARM Intelligent Diagnostic"
            }
            print(f"[DEBUG] Final Hybrid Result: {result}")
        else:
            # Fallback when model not available
            raise HTTPException(
                status_code=503, 
                detail="Model not loaded. Please train the model first by running: python backend/train_model.py"
            )
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
