import os
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import MobileNetV2
import matplotlib.pyplot as plt

# AeroFarm-AI: Optimized Transfer Learning Protocol
DATA_DIR = './data'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'val')
MODEL_SAVE_PATH = 'backend/model/plant_model.h5'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10 # Reduced epochs since transfer learning is efficient

def train_aerofarm_model():
    print("--- AeroFarm-AI: Initializing FAST Transfer Learning Training ---")
    tf.keras.backend.clear_session()

    # 1. Efficient Data Loading
    print(f"Loading datasets from {DATA_DIR}...")
    try:
        # We only take a subset if the dataset is too huge, but let's try with 32 batch first
        train_ds = tf.keras.utils.image_dataset_from_directory(
            TRAIN_DIR,
            image_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            label_mode='int',
            shuffle=True
        )

        val_ds = tf.keras.utils.image_dataset_from_directory(
            VAL_DIR,
            image_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            label_mode='int'
        )
        
        class_names = train_ds.class_names
        num_classes = len(class_names)
        print(f"Detected {num_classes} categories.")
        
    except Exception as e:
        print(f"Dataset error: {e}")
        return

    # Pipeline optimization (NO .cache() to save RAM)
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 2. Base Model: MobileNetV2 (Pre-trained on ImageNet)
    print("Loading Pre-trained MobileNetV2 base...")
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False # Freeze the base knowledge

    # 3. Build the AeroFarm Head
    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Rescaling(1./127.5, offset=-1), # MobileNetV2 specific rescaling (-1 to 1)
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # 4. Training with Early Stopping
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    checkpoint = callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max', verbose=1
    )
    
    early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=3)

    print("Starting training session...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[checkpoint, early_stop]
    )

    # 5. Save report
    plot_results(history)
    print(f"Success! Optimized model saved to: {MODEL_SAVE_PATH}")

def plot_results(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    plt.figure(figsize=(10, 5))
    plt.plot(acc, label='Train Acc', color='#00ff88')
    plt.plot(val_acc, label='Val Acc', color='#f59e0b')
    plt.title('AeroFarm-AI Performance')
    plt.legend()
    plt.savefig('training_report.png')
    plt.close()
    print("Report saved as training_report.png")

if __name__ == "__main__":
    train_aerofarm_model()
