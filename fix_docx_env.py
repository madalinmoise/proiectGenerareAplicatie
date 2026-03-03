import subprocess
import sys

def fix():
    print("Attempting to fix docx environment...")
    # The legacy 'docx' package causes conflicts. 'python-docx' is the modern one.
    # We must ensure 'docx' is uninstalled.
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "docx"])
    except:
        pass

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "python-docx"])
    except Exception as e:
        print(f"Error upgrading python-docx: {e}")

if __name__ == "__main__":
    fix()
