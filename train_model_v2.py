import os
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers
from tensorflow.keras.applications import MobileNetV2
import matplotlib.pyplot as plt

# AeroFarm-AI V2: HIGH PRECISION PROTOCOL
DATA_DIR = './data'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
VAL_DIR = os.path.join(DATA_DIR, 'val')
MODEL_SAVE_PATH = 'backend/model/plant_model.h5'
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16 # Reduced batch size for stability
INITIAL_EPOCHS = 5 # Faster phase switch
FINE_TUNE_EPOCHS = 15
TOTAL_EPOCHS = INITIAL_EPOCHS + FINE_TUNE_EPOCHS

def train_aerofarm_v2():
    print("--- AeroFarm-AI V2: Deep Fine-Tuning Engaged ---")
    tf.keras.backend.clear_session()
    
    # 0. Logger for tracking
    log_file = 'training_log.csv'
    csv_logger = callbacks.CSVLogger(log_file, append=True)

    # 1. Advanced Data Loading with Augmentation
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.1),
    ])

    print(f"Loading datasets from {DATA_DIR}...")
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
    
    num_classes = len(train_ds.class_names)
    
    # Prefetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 2. Base Model: MobileNetV2
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    # 3. Model Architecture
    inputs = layers.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = layers.Rescaling(1./127.5, offset=-1)(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu')(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs, outputs)

    model.compile(optimizer=optimizers.Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # 4. Phase 1: Training the Head
    print("Phase 1: Training classifier head...")
    checkpoint = callbacks.ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True, mode='max')
    
    model.fit(train_ds, validation_data=val_ds, epochs=INITIAL_EPOCHS, callbacks=[checkpoint, csv_logger])

    # 5. Phase 2: Deep Fine-Tuning
    print("Phase 2: Deep Fine-Tuning...")
    base_model.trainable = True
    
    # We unfreeze only the top layers of the base model
    # MobileNetV2 has 154 layers
    fine_tune_at = 100
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(optimizer=optimizers.Adam(learning_rate=0.0001), # Lower learning rate for fine-tuning
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.00001)
    early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    model.fit(train_ds, validation_data=val_ds, epochs=TOTAL_EPOCHS, initial_epoch=INITIAL_EPOCHS,
              callbacks=[checkpoint, reduce_lr, early_stop, csv_logger])

    print(f"Success! Advanced Model V2 saved to: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_aerofarm_v2()
