import os
import base64
import io
import json
from groq import Groq
from PIL import Image
from dotenv import load_dotenv

def get_groq_insight(image_bytes: bytes, local_prediction: str):
    """
    Hybrid Reasoning Layer using Llama 4 Scout (Native Multimodal).
    Optimized for high-precision botanical identification.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or "YOUR_GROQ" in api_key:
        return {
            "is_leaf": True, 
            "correct_name": local_prediction,
            "gemini_advice": "Critical: Intelligence API key missing. Please check backend configuration."
        }

    try:
        client = Groq(api_key=api_key)
        
        # Prepare image
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Llama 4 Scout handles resolution well, but 800px is enough
        img.thumbnail((1024, 1024))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Advanced Prompt for Correction
        prompt = f"""
        System: Specialized Plant Pathologist & Vision Expert.
        Input: A photo of a plant leaf.
        Local AI Prediction: '{local_prediction}'
        
        Challenge: The user suspects the local AI is WRONG. 
        It often confuses Apple leaves for Strawberry. 
        Look EXTREMELY CLOSELY at the leaf shape, serration, and texture.
        
        Identify the plant and any disease exactly. 
        If it's an Apple leaf, correctly identify it as 'Apple - [Disease Name]'.
        
        Return JSON ONLY:
        {{
            "is_plant": boolean,
            "disease_name": "Corrected Identity (e.g. 'Apple Black Rot')",
            "expert_advice": "3 specific professional treatment tips"
        }}
        """

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"}
        )

        data = json.loads(completion.choices[0].message.content)
        print(f"[DEBUG] Llama 4 Scout Verdict: {data}")

        return {
            "is_leaf": data.get("is_plant", True),
            "correct_name": data.get("disease_name", local_prediction),
            "gemini_advice": data.get("expert_advice", "No advice generated.")
        }

    except Exception as e:
        print(f"[ERROR] Groq Llama 4 Scout Failure: {str(e)}")
        # Check if 413 (Payload Too Large)? No.
        return {
            "is_leaf": True, 
            "correct_name": local_prediction,
            "gemini_advice": f"Model Reasoning Error: {str(e)[:100]}..."
        }
