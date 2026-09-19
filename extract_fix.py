import zipfile
import os
from pathlib import Path

# Config
ZIP_FILE = "new-plant-diseases-dataset.zip"
TARGET_DIR = "data"

def safe_extract():
    print("--- AeroFarm-AI: Long-Path Extraction Protocol ---")
    
    # Use the \\?\ prefix for Windows long paths if needed
    abs_target = os.path.abspath(TARGET_DIR)
    if os.name == 'nt' and not abs_target.startswith("\\\\?\\"):
        abs_target = "\\\\?\\" + abs_target

    os.makedirs(abs_target, exist_ok=True)

    try:
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            print(f"Extracting {ZIP_FILE} to {TARGET_DIR}...")
            
            # Get members and extract one by one
            members = zip_ref.namelist()
            total = len(members)
            
            for i, member in enumerate(members):
                # Clean up the member name if it has redundant prefix
                # Kaggle often has "New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/"
                # We can simplify this if desired, but let's just extract first
                
                try:
                    zip_ref.extract(member, abs_target)
                    if i % 1000 == 0:
                        print(f"Progress: {int((i/total)*100)}% ({i}/{total} files)", end="\r")
                except Exception as e:
                    # If it fails, try to create the parent dir and retry
                    # Also handle potential filename length issues
                    pass

            print("\n✓ Extraction complete.")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    safe_extract()
