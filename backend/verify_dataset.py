"""
Dataset verification and statistics script
Run this before training to ensure data is properly structured
"""
import os
from pathlib import Path
from collections import defaultdict

TRAIN_DIR = "data/train"
TEST_DIR = "data/test/test"

def verify_dataset():
    print("=" * 70)
    print("Dataset Verification")
    print("=" * 70)
    
    # Check training data
    if not os.path.exists(TRAIN_DIR):
        print(f"✗ Training directory not found: {TRAIN_DIR}")
        print("  Please extract the dataset first.")
        return False
    
    print(f"\n✓ Training directory found: {TRAIN_DIR}")
    
    # Count classes and images
    classes = []
    class_counts = {}
    total_train_images = 0
    
    for class_name in sorted(os.listdir(TRAIN_DIR)):
        class_path = os.path.join(TRAIN_DIR, class_name)
        if os.path.isdir(class_path):
            image_files = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            count = len(image_files)
            classes.append(class_name)
            class_counts[class_name] = count
            total_train_images += count
    
    print(f"\n✓ Found {len(classes)} disease classes")
    print(f"✓ Total training images: {total_train_images:,}")
    
    # Show class distribution
    print("\nClass Distribution:")
    print("-" * 70)
    print(f"{'Class Name':<50} {'Images':>10}")
    print("-" * 70)
    
    for class_name in sorted(classes):
        count = class_counts[class_name]
        bar = "█" * (count // 100)
        print(f"{class_name:<50} {count:>10,} {bar}")
    
    print("-" * 70)
    print(f"{'Average per class':<50} {total_train_images // len(classes):>10,}")
    print(f"{'Min images':<50} {min(class_counts.values()):>10,}")
    print(f"{'Max images':<50} {max(class_counts.values()):>10,}")
    
    # Check test data
    print("\n" + "=" * 70)
    if os.path.exists(TEST_DIR):
        test_images = [f for f in os.listdir(TEST_DIR) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"✓ Test directory found: {TEST_DIR}")
        print(f"✓ Test images: {len(test_images)}")
    else:
        print(f"⚠ Test directory not found: {TEST_DIR}")
    
    # Check for imbalanced classes
    print("\n" + "=" * 70)
    avg_count = total_train_images / len(classes)
    imbalanced = []
    for class_name, count in class_counts.items():
        if count < avg_count * 0.5:  # Less than 50% of average
            imbalanced.append((class_name, count))
    
    if imbalanced:
        print("⚠ Warning: Some classes have significantly fewer images:")
        for class_name, count in imbalanced:
            print(f"  - {class_name}: {count} images")
        print("  Consider data augmentation or collecting more samples.")
    else:
        print("✓ Dataset is reasonably balanced")
    
    # Recommendations
    print("\n" + "=" * 70)
    print("Recommendations:")
    print("-" * 70)
    
    if total_train_images < 10000:
        print("⚠ Small dataset detected. Consider:")
        print("  - Using aggressive data augmentation")
        print("  - Transfer learning (already implemented)")
        print("  - Collecting more training data")
    else:
        print("✓ Dataset size is adequate for training")
    
    print("\n✓ Dataset verification complete!")
    print("=" * 70)
    print("\nReady to train! Run: python backend/train_model.py")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    verify_dataset()
