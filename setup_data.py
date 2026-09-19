import os
import shutil
import subprocess
import zipfile
import sys
from pathlib import Path

# Config: AeroFarm-AI Data Setup
KAGGLE_DATASET = "vipoooool/new-plant-diseases-dataset"
ZIP_FILE = "new-plant-diseases-dataset.zip"
TARGET_DIR = "data"

def setup_kaggle_api():
    """Configures Kaggle API credentials for the Antigravity workspace."""
    print("--- AeroFarm-AI: Data Setup System Initialization ---")
    
    # Check if the environment variable is already set
    if "KAGGLE_API_TOKEN" in os.environ:
        print("✓ Detected KAGGLE_API_TOKEN in environment. Ready for download.")
        return

    home = Path.home()
    kaggle_config_dir = home / ".kaggle"
    kaggle_json_src = Path("kaggle.json")
    kaggle_json_dest = kaggle_config_dir / "kaggle.json"

    # Step 1: Detect and Move API Key
    print("[1/4] Configuring Kaggle API credentials...")
    if not kaggle_json_src.exists():
        if not kaggle_json_dest.exists():
            print("(!) NOTICE: 'kaggle.json' not found and KAGGLE_API_TOKEN is not set.")
            print("    Please run: $env:KAGGLE_API_TOKEN=\"YOUR_TOKEN_HERE\" before running this script.")
            sys.exit(1)
        else:
            print("✓ Kaggle API key already exists in the home configuration folder.")
    else:
        # Create .kaggle folder if it doesn't exist
        kaggle_config_dir.mkdir(exist_ok=True, parents=True)
        
        # Move kaggle.json to the correct folder
        shutil.move(str(kaggle_json_src), str(kaggle_json_dest))
        print(f"✓ Moved kaggle.json to {kaggle_json_dest}")

        if os.name != 'nt':  # Linux/Mac
            os.chmod(str(kaggle_json_dest), 0o600)
            print("✓ Set file permissions to 600.")
        else:
            print("✓ Verified credentials on Windows system.")


def download_and_extract():
    """Installs dependencies, downloads the 2.7GB dataset, and extracts files."""
    
    # Step 2: Ensure Kaggle library is installed
    print("[2/4] Verifying 'kaggle' library installation...")
    try:
        import kaggle
    except ImportError:
        print("Kaggle library not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        print("Library installed successfully.")

    # Step 3: Download Dataset
    print(f"[3/4] Downloading high-quality dataset: '{KAGGLE_DATASET}'...")
    print("This is a 2.7GB file. Please ensure you have a stable connection.")
    
    try:
        # Re-import to ensure API is ready
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        # Download command
        api.dataset_download_files(KAGGLE_DATASET, path=".", unzip=False)
        print("Download complete.")
    except Exception as e:
        print(f"API Error: {e}")
        # Fallback to subprocess if API auth fails
        try:
            subprocess.check_call(["kaggle", "datasets", "download", "-d", KAGGLE_DATASET])
        except Exception:
            print("Failed to download dataset. Check your Kaggle API credentials.")
            sys.exit(1)

    # Step 4: Unzip and Cleanup
    print(f"[4/4] Extracting files into '{TARGET_DIR}' folder...")
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    try:
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            # Extracting with progress
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            for i, file in enumerate(file_list):
                zip_ref.extract(file, TARGET_DIR)
                if i % 1000 == 0:
                    print(f"Extraction progress: {int((i/total_files)*100)}% ({i}/{total_files} files)", end="\r")
            
            print("\nExtraction complete.")
            
            # Final Cleanup
            print("Cleaning up workspace...")
            os.remove(ZIP_FILE)
            print(f"Deleted heavy ZIP file: {ZIP_FILE}")
            print("\n--- AeroFarm-AI: Data Setup Complete ---")
            print(f"Dataset ready in: {os.path.abspath(TARGET_DIR)}")

    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    setup_kaggle_api()
    download_and_extract()
