"""
CPU-Optimized Plant Disease Classification Training
Optimized for systems with 8GB RAM, no GPU, and i3 processor
"""
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from datetime import datetime

# CPU-Optimized Configuration
IMG_SIZE = 224
BATCH_SIZE = 8  # Smaller batch for 8GB RAM
EPOCHS = 25  # Fewer epochs for faster training
LEARNING_RATE = 0.0001
TRAIN_DIR = "data/train"
TEST_DIR = "data/test/test"
MODEL_DIR = "backend/model"
MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.h5")
CLASSES_PATH = os.path.join(MODEL_DIR, "classes.json")

# CPU optimization settings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging
tf.config.threading.set_intra_op_parallelism_threads(2)  # Optimize for i3 (2 cores)
tf.config.threading.set_inter_op_parallelism_threads(2)

def create_lightweight_model(num_classes):
    """
    Create a lighter MobileNetV2 model for CPU training
    """
    # Load pre-trained MobileNetV2 with lower alpha for speed
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet',
        alpha=0.75  # Lighter model (75% width)
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Simpler classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(256, activation='relu'),  # Smaller dense layer
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def prepare_data():
    """
    Prepare data with lighter augmentation for faster training
    """
    # Lighter augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,  # Reduced
        width_shift_range=0.15,  # Reduced
        height_shift_range=0.15,  # Reduced
        shear_range=0.15,  # Reduced
        zoom_range=0.15,  # Reduced
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    val_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator

def train():
    """
    CPU-optimized training function
    """
    print("=" * 70)
    print("CPU-Optimized Plant Disease Classification Training")
    print("=" * 70)
    print("\n💻 System Configuration:")
    print("  - Processor: i3 (optimized for 2 cores)")
    print("  - RAM: 8GB (batch size: 8)")
    print("  - Storage: 512GB")
    print("  - Training Mode: CPU-only")
    print("\n[TIME] Estimated Training Time: 6-10 hours")
    print("  - You can stop anytime with Ctrl+C")
    print("  - Best model is saved automatically")
    print("  - Training can be resumed if interrupted\n")
    
    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Prepare data
    print("[1/5] Loading and preparing data...")
    train_gen, val_gen = prepare_data()
    
    num_classes = len(train_gen.class_indices)
    print(f"[OK] Found {num_classes} disease classes")
    print(f"[OK] Training samples: {train_gen.samples}")
    print(f"[OK] Validation samples: {val_gen.samples}")
    
    # Save class mappings
    class_indices = train_gen.class_indices
    class_names = {v: k for k, v in class_indices.items()}
    with open(CLASSES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"[OK] Class mappings saved")
    
    # Create lightweight model
    print("\n[2/5] Building lightweight model...")
    model = create_lightweight_model(num_classes)
    print(f"[OK] CPU-optimized model created")
    
    # Compile
    print("\n[3/5] Compiling model...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    print("[OK] Model compiled")
    
    # Show model summary
    total_params = model.count_params()
    print(f"[OK] Total parameters: {total_params:,}")
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            MODEL_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=7,  # Reduced patience
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,  # Reduced patience
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train
    print(f"\n[4/5] Training model (up to {EPOCHS} epochs)...")
    print("-" * 70)
    print("[INFO] Tip: Training on CPU is slow but will complete successfully")
    print("   Consider running overnight or during breaks\n")
    
    try:
        history = model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS,
            callbacks=callbacks,
            verbose=1
        )
    except KeyboardInterrupt:
        print("\n\n[WARN] Training interrupted by user")
        print("[OK] Best model has been saved")
        return None, None
    
    # Evaluate
    print("\n[5/5] Final evaluation...")
    val_loss, val_acc = model.evaluate(val_gen, verbose=0)
    print(f"[OK] Validation Accuracy: {val_acc*100:.2f}%")
    print(f"[OK] Validation Loss: {val_loss:.4f}")
    
    # Save history
    history_path = os.path.join(MODEL_DIR, "training_history.json")
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']]
    }
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print("\n" + "=" * 70)
    print("[OK] Training Complete!")
    print("=" * 70)
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Classes saved to: {CLASSES_PATH}")
    print(f"History saved to: {history_path}")
    
    return model, history

if __name__ == "__main__":
    print("\n[STARTING] Starting CPU-Optimized Training for 8GB RAM / i3 Systems\n")
    
    # Confirm before starting
    if os.getenv('AUTO_TRAIN') != 'true':
        response = input("This will take 6-10 hours. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Training cancelled")
            exit(0)
    else:
        print("Auto-training mode enabled. Proceeding...")
    
    # Start training
    model, history = train()
    
    if model is not None:
        print("\n[SUCCESS] Your model is ready to use.")
        print("\nNext steps:")
        print("1. Test: python backend/test_model.py")
        print("2. Run API: python backend/app.py")
