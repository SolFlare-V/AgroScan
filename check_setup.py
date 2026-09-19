"""
Pre-training setup checker
Verifies that everything is ready for training
"""
import os
import sys
import importlib.util

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False

def check_package(package_name, display_name=None):
    """Check if a package is installed"""
    if display_name is None:
        display_name = package_name
    
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name} ({version})")
            return True
        except:
            print(f"⚠ {display_name} (installed but can't import)")
            return False
    else:
        print(f"✗ {display_name} (not installed)")
        return False

def check_directory(path, description):
    """Check if directory exists"""
    if os.path.exists(path) and os.path.isdir(path):
        # Count items
        items = os.listdir(path)
        print(f"✓ {description} ({len(items)} items)")
        return True
    else:
        print(f"✗ {description} (not found)")
        return False

def check_disk_space():
    """Check available disk space"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free // (2**30)
        if free_gb >= 2:
            print(f"✓ Disk space ({free_gb}GB free)")
            return True
        else:
            print(f"⚠ Disk space ({free_gb}GB free, need 2GB+)")
            return False
    except:
        print("⚠ Could not check disk space")
        return True

def check_gpu():
    """Check if GPU is available"""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✓ GPU detected ({len(gpus)} device(s))")
            for gpu in gpus:
                print(f"  - {gpu.name}")
            return True
        else:
            print("⚠ No GPU detected (training will be slower on CPU)")
            return True
    except:
        print("⚠ Could not check GPU")
        return True

def main():
    """Run all checks"""
    print("=" * 70)
    print("Pre-Training Setup Checker")
    print("=" * 70)
    
    all_passed = True
    
    # Python version
    print("\n[1] Python Version")
    print("-" * 70)
    if not check_python_version():
        all_passed = False
    
    # Required packages
    print("\n[2] Required Packages")
    print("-" * 70)
    packages = [
        ('tensorflow', 'TensorFlow'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
    ]
    
    for package, display in packages:
        if not check_package(package, display):
            all_passed = False
    
    # Optional packages
    print("\n[3] Optional Packages")
    print("-" * 70)
    check_package('matplotlib', 'Matplotlib (for visualization)')
    
    # Dataset
    print("\n[4] Dataset")
    print("-" * 70)
    if not check_directory("data/train", "Training data"):
        all_passed = False
    check_directory("data/test/test", "Test data")
    
    # Directories
    print("\n[5] Project Structure")
    print("-" * 70)
    if not check_directory("backend", "Backend directory"):
        all_passed = False
    if not check_directory("backend/utils", "Utils directory"):
        all_passed = False
    
    # System resources
    print("\n[6] System Resources")
    print("-" * 70)
    check_disk_space()
    check_gpu()
    
    # Files
    print("\n[7] Required Files")
    print("-" * 70)
    files = [
        "backend/train_model.py",
        "backend/app.py",
        "backend/utils/preprocess.py",
        "backend/requirements.txt"
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All checks passed! Ready to train.")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run: python start_training.py")
        print("   OR")
        print("2. Run: python backend/train_model.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("=" * 70)
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r backend/requirements.txt")
        print("2. Extract dataset to 'data' folder")
        print("3. Ensure all project files are present")
        sys.exit(1)

if __name__ == "__main__":
    main()
