"""
Visualize training history and model performance
"""
import json
import os
import matplotlib.pyplot as plt

HISTORY_PATH = "backend/model/training_history.json"

def plot_training_history():
    """Plot training and validation metrics"""
    if not os.path.exists(HISTORY_PATH):
        print(f"✗ Training history not found: {HISTORY_PATH}")
        print("  Train the model first: python backend/train_model.py")
        return
    
    with open(HISTORY_PATH, 'r') as f:
        history = json.load(f)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot accuracy
    ax1.plot(history['accuracy'], label='Training Accuracy', linewidth=2)
    ax1.plot(history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    # Plot loss
    ax2.plot(history['loss'], label='Training Loss', linewidth=2)
    ax2.plot(history['val_loss'], label='Validation Loss', linewidth=2)
    ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_path = "backend/model/training_plot.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Training plot saved to: {output_path}")
    
    # Show statistics
    print("\nTraining Statistics:")
    print("=" * 50)
    print(f"Total Epochs: {len(history['accuracy'])}")
    print(f"Best Training Accuracy: {max(history['accuracy'])*100:.2f}%")
    print(f"Best Validation Accuracy: {max(history['val_accuracy'])*100:.2f}%")
    print(f"Final Training Loss: {history['loss'][-1]:.4f}")
    print(f"Final Validation Loss: {history['val_loss'][-1]:.4f}")
    
    # Check for overfitting
    train_acc = history['accuracy'][-1]
    val_acc = history['val_accuracy'][-1]
    gap = train_acc - val_acc
    
    print("\nModel Analysis:")
    print("=" * 50)
    if gap > 0.1:
        print("⚠ Warning: Possible overfitting detected")
        print(f"  Training-Validation gap: {gap*100:.2f}%")
        print("  Consider: More dropout, data augmentation, or regularization")
    elif gap < 0.02:
        print("✓ Model is well-balanced")
    else:
        print("✓ Model shows good generalization")
    
    plt.show()

if __name__ == "__main__":
    try:
        plot_training_history()
    except ImportError:
        print("✗ matplotlib not installed")
        print("  Install with: pip install matplotlib")
