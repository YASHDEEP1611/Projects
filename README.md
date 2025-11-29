import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# ----------------------- Functions ----------------------- #
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Python File",
        filetypes=[("Python Files", "*.py")]
    )
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def select_icon():
    icon_path = filedialog.askopenfilename(
        title="Select Icon",
        filetypes=[("Icon Files", "*.ico")]
    )
    if icon_path:
        entry_icon.delete(0, tk.END)
        entry_icon.insert(0, icon_path)

def convert_to_exe():
    py_file = entry_path.get().strip()
    if not py_file or not os.path.exists(py_file):
        messagebox.showerror("Error", "Please select a valid .py file.")
        return

    icon_path = entry_icon.get().strip()
    console_option = var_console.get()

    # ---------------- Check PyInstaller ---------------- #
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        messagebox.showerror(
            "Error",
            "⚠️ PyInstaller not installed in this Python environment.\n\n"
            "Run this in your terminal:\n\npip install pyinstaller"
        )
        return

    # ---------------- Build Command ---------------- #
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile"]
    if not console_option:
        cmd.append("--noconsole")
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    cmd.append(py_file)

    print("Running command:", " ".join(cmd))  # Debug log
    messagebox.showinfo("Converting", "Conversion started. Please wait...")

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Done", "✅ Conversion complete! Check the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"❌ Conversion failed!\n\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def convert_to_exe_thread():
    # Run conversion in a separate thread to avoid freezing GUI
    threading.Thread(target=convert_to_exe).start()

# ----------------------- GUI Setup ----------------------- #
root = tk.Tk()
root.title("PY to EXE Converter")
root.geometry("480x270")
root.resizable(False, False)

# --- Select Python file ---
tk.Label(root, text="Select .py file:", font=("Segoe UI", 10, "bold")).pack(pady=5)
frame_file = tk.Frame(root)
frame_file.pack()
entry_path = tk.Entry(frame_file, width=45)
entry_path.pack(side=tk.LEFT, padx=5)
tk.Button(frame_file, text="Browse", command=select_file).pack(side=tk.LEFT)

# --- Optional icon ---
tk.Label(root, text="Optional icon (.ico):", font=("Segoe UI", 10, "bold")).pack(pady=5)
frame_icon = tk.Frame(root)
frame_icon.pack()
entry_icon = tk.Entry(frame_icon, width=45)
entry_icon.pack(side=tk.LEFT, padx=5)
tk.Button(frame_icon, text="Browse", command=select_icon).pack(side=tk.LEFT)

# --- Console option ---
var_console = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Show Console (for CLI apps)", variable=var_console).pack(pady=10)

# --- Convert button ---
tk.Button(
    root,
    text="Convert to EXE",
    command=convert_to_exe_thread,
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=5
).pack(pady=10)

root.mainloop()
