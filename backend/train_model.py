"""
Complete Plant Disease Classification Model Training Pipeline
Uses MobileNetV2 with transfer learning for efficient training
"""
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from datetime import datetime

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 16  # Reduced for 8GB RAM systems
EPOCHS = 30  # Reduced for faster training on CPU
LEARNING_RATE = 0.0001
TRAIN_DIR = "data/train"
TEST_DIR = "data/test/test"
MODEL_DIR = "backend/model"
MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.h5")
CLASSES_PATH = os.path.join(MODEL_DIR, "classes.json")

def create_model(num_classes):
    """
    Create MobileNetV2-based transfer learning model
    """
    # Load pre-trained MobileNetV2 without top layers
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def prepare_data():
    """
    Prepare data generators with augmentation
    """
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2  # 20% for validation
    )
    
    # Test data (no augmentation)
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
    Main training function
    """
    print("=" * 60)
    print("Plant Disease Classification - Model Training")
    print("=" * 60)
    print("\n⚠ CPU Training Mode Detected")
    print("  Estimated time: 6-10 hours on i3 processor")
    print("  You can stop training anytime with Ctrl+C")
    print("  The best model will be saved automatically\n")
    
    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Prepare data
    print("\n[1/5] Loading and preparing data...")
    train_gen, val_gen = prepare_data()
    
    num_classes = len(train_gen.class_indices)
    print(f"✓ Found {num_classes} disease classes")
    print(f"✓ Training samples: {train_gen.samples}")
    print(f"✓ Validation samples: {val_gen.samples}")
    
    # Save class mappings
    class_indices = train_gen.class_indices
    class_names = {v: k for k, v in class_indices.items()}
    with open(CLASSES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"✓ Class mappings saved to {CLASSES_PATH}")
    
    # Create model
    print("\n[2/5] Building model architecture...")
    model = create_model(num_classes)
    print(f"✓ Model created with {num_classes} output classes")
    
    # Compile model
    print("\n[3/5] Compiling model...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    print("✓ Model compiled")
    
    # Model summary
    model.summary()
    
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
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    print(f"\n[4/5] Training model for up to {EPOCHS} epochs...")
    print("-" * 60)
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate
    print("\n[5/5] Final evaluation...")
    val_loss, val_acc, val_top3 = model.evaluate(val_gen, verbose=0)
    print(f"✓ Validation Accuracy: {val_acc*100:.2f}%")
    print(f"✓ Top-3 Accuracy: {val_top3*100:.2f}%")
    print(f"✓ Validation Loss: {val_loss:.4f}")
    
    # Save training history
    history_path = os.path.join(MODEL_DIR, "training_history.json")
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']]
    }
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Classes saved to: {CLASSES_PATH}")
    print(f"History saved to: {history_path}")
    
    return model, history

if __name__ == "__main__":
    # Set memory growth for GPU if available
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"✓ GPU available: {len(gpus)} device(s)")
        except RuntimeError as e:
            print(f"GPU configuration error: {e}")
    else:
        print("⚠ No GPU detected, training on CPU (will be slower)")
    
    # Start training
    model, history = train()
