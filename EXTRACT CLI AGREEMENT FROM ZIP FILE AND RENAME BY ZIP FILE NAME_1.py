import os
import zipfile
import shutil
from tkinter import Tk, filedialog

# --- SELECT INPUT FOLDER (folder containing zips) ---
root = Tk()
root.withdraw()  # hide the main window
ZIP_FOLDER = filedialog.askdirectory(title="📂 Select Folder Containing ZIP Files")
root.destroy()

if not ZIP_FOLDER:
    print("❌ No folder selected. Exiting.")
    exit()

# --- OUTPUT / TEMP FOLDERS ---
OUTPUT_FOLDER = os.path.join(ZIP_FOLDER, "CLI_PDFs")   # inside same folder
TEMP_FOLDER = os.path.join(ZIP_FOLDER, "temp_unzip")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# --- Function: Extract zip ---
def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_to)
        return True
    except zipfile.BadZipFile:
        print(f"⚠️ Skipped (not a valid zip): {zip_path}")
        return False

# --- MAIN LOOP ---
for file in os.listdir(ZIP_FOLDER):
    if file.lower().endswith(".zip"):
        zip_name = os.path.splitext(file)[0]   # 📛 name of the zip (without .zip)
        zip_path = os.path.join(ZIP_FOLDER, file)
        extract_path = os.path.join(TEMP_FOLDER, zip_name)

        print(f"📦 Extracting: {file}")
        if extract_zip(zip_path, extract_path):
            # scan extracted files
            for root, _, files in os.walk(extract_path):
                for fname in files:
                    if fname.lower().endswith(".pdf") and fname.upper().startswith("CLI_"):
                        pdf_path = os.path.join(root, fname)

                        # 👇 Rename to zip name
                        dest_name = f"{zip_name}.pdf"
                        dest_path = os.path.join(OUTPUT_FOLDER, dest_name)

                        shutil.copy2(pdf_path, dest_path)
                        print(f"✅ Copied {fname} → {dest_name}")

print("🎉 Done! All CLI agreements renamed by zip name are in:", OUTPUT_FOLDER)
