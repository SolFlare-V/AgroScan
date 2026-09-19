import os
import groq
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

if not api_key or "YOUR_GROQ" in api_key:
    print("ERROR: Groq API Key is not set in .env")
    exit(1)

client = groq.Groq(api_key=api_key)

models_to_test = [
    "llama-3.2-90b-vision-preview",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-11b-text-preview"
]

print(f"Testing models with API Key: {api_key[:10]}...")

for model_id in models_to_test:
    try:
        print(f"Checking model: {model_id}...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello, can you see this text?",
                }
            ],
            model=model_id,
        )
        print(f"SUCCESS: {model_id} is active!")
    except Exception as e:
        print(f"FAILED: {model_id} - {str(e)}")

print("\nListing all available models:")
try:
    models = client.models.list()
    for m in models.data:
        if "vision" in m.id or "llama-3.2" in m.id:
            print(f"- {m.id}")
except Exception as e:
    print(f"Error listing models: {e}")
