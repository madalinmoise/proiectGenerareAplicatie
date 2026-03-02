from web_api import app, start_server
import threading
import time
from core.engine import DocumentEngine
from ui.main_window import EnterpriseApp

if __name__ == "__main__":
    # Create a mock or hidden app instance
    import customtkinter as ctk
    # ctk might fail without X11, let's see.
    try:
        main_app = EnterpriseApp()
        main_app.withdraw()
        threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False, 'use_reloader': False}, daemon=True).start()
        print("Server started on http://localhost:5000")
        time.sleep(10) # Give it time to be up
    except Exception as e:
        print(f"Failed to start app/server: {e}")
