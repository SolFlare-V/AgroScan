"""
One-command script to verify dataset and start training
"""
import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    try:
        import tensorflow
        import numpy
        import PIL
        print("✓ All dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nInstall dependencies with:")
        print("  pip install -r backend/requirements.txt")
        return False

def verify_dataset():
    """Run dataset verification"""
    print("\n" + "=" * 70)
    print("Step 1: Verifying Dataset")
    print("=" * 70)
    
    if not os.path.exists("data/train"):
        print("✗ Training data not found!")
        print("  Please extract the dataset to the 'data' folder")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, "backend/verify_dataset.py"],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error verifying dataset: {e}")
        return False

def start_training():
    """Start model training"""
    print("\n" + "=" * 70)
    print("Step 2: Starting Model Training")
    print("=" * 70)
    print("\nThis will take 2-4 hours on GPU or 8-12 hours on CPU")
    print("You can monitor progress in real-time below.\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "backend/train_model.py"],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n\n⚠ Training interrupted by user")
        return False
    except Exception as e:
        print(f"✗ Error during training: {e}")
        return False

def main():
    """Main execution flow"""
    print("=" * 70)
    print("AgroScan - Automated Training Pipeline")
    print("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Verify dataset
    if not verify_dataset():
        print("\n✗ Dataset verification failed")
        sys.exit(1)
    
    # Confirm before training
    print("\n" + "=" * 70)
    response = input("\nReady to start training? This will take several hours. (y/n): ")
    if response.lower() != 'y':
        print("Training cancelled")
        sys.exit(0)
    
    # Start training
    success = start_training()
    
    if success:
        print("\n" + "=" * 70)
        print("✓ Training completed successfully!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Test the model: python backend/test_model.py")
        print("2. Visualize results: python backend/visualize_training.py")
        print("3. Start API server: python backend/app.py")
    else:
        print("\n✗ Training failed or was interrupted")
        sys.exit(1)

if __name__ == "__main__":
    main()
