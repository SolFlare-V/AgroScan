import io
import numpy as np
from PIL import Image
import tensorflow as tf

def load_and_preprocess(image_bytes: bytes):
    """
    Standardize the image for the MobileNetV2 model:
    - Resize to 224x224
    - Normalize RGB values to [0, 1]
    - Expand dims for batch processing
    """
    # Open the image from bytes
    img = Image.open(io.BytesIO(image_bytes))
    
    # Ensure image is in RGB mode
    if img.mode != "RGB":
        img = img.convert("RGB")
        
    # Convert to numpy array first
    img_array = np.array(img).astype(np.float32)
    
    # Use tf.image.resize for BILINEAR interpolation (exactly like training)
    img_array = tf.image.resize(img_array, (224, 224)).numpy()
    
    # NOTE: We do NOT rescaling to [-1, 1] manually because the model has a 
    # built-in layers.Rescaling(1./127.5, offset=-1) layer.
    
    # Add batch dimension (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array
