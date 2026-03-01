# main.py
import sys
import os
import multiprocessing as mp

# Multiprocessing init for Windows
if sys.platform.startswith('win'):
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        pass

sys.path.insert(0, os.path.dirname(__file__))

from app import PlaceholderApp

if __name__ == "__main__":
    app = PlaceholderApp()
    app.mainloop()