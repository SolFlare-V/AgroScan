import os
import google.generativeai as genai
from PIL import Image
import io
import json
from dotenv import load_dotenv

def get_gemini_insight(image_bytes: bytes, local_prediction: str):
    """
    A Hybrid Reasoning Layer that:
    1. Validates if the image contains a plant leaf.
    2. Overrides the local model if Gemini detects a clear contradiction.
    3. Provides professional agricultural improvement suggestions.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or "YOUR_GEMINI" in api_key:
        return {
            "is_leaf": True, 
            "correct_name": local_prediction,
            "gemini_advice": "Configure your GEMINI_API_KEY in .env for AI-powered suggestions and accuracy verification."
        }

    try:
        genai.configure(api_key=api_key)
        # Use JSON mode for reliable parsing
        model = genai.GenerativeModel('gemini-1.5-flash',
                                      generation_config={"response_mime_type": "application/json"})
        img = Image.open(io.BytesIO(image_bytes))
        
        prompt = f"""
        Role: Professional Plant Pathologist.
        Local AI model identification: {local_prediction}.
        
        Analyze the image and return a JSON object with:
        - "is_plant": boolean (true if image is a plant leaf/part, false otherwise)
        - "disease_name": string (Correct plant and disease name. If the Local AI is wrong, fix it. Ex: 'Tomato Late Blight')
        - "expert_advice": string (3 professional tips for treatment and health)
        
        Example JSON:
        {{
            "is_plant": true,
            "disease_name": "Tomato Early Blight",
            "expert_advice": "1. Prune affected lower leaves. 2. Apply copper-based fungicide. 3. Avoid overhead watering."
        }}
        """
        
        response = model.generate_content([prompt, img])
        
        # Robust parsing
        try:
            data = json.loads(response.text)
            print(f"[DEBUG] Gemini JSON Response: {data}")
            
            return {
                "is_leaf": data.get("is_plant", True),
                "correct_name": data.get("disease_name", local_prediction),
                "gemini_advice": data.get("expert_advice", "Expert suggestions unavailable.")
            }
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to parse Gemini JSON: {response.text}")
            return {
                "is_leaf": True, 
                "correct_name": local_prediction,
                "gemini_advice": "Expert suggestions format error."
            }

    except Exception as e:
        print(f"[ERROR] Gemini Reasoning Layer failed: {e}")
        return {
            "is_leaf": True, 
            "correct_name": local_prediction,
            "gemini_advice": f"Expert suggestions offline: {str(e)}"
        }
