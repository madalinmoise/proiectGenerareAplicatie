import sys
import os
import multiprocessing as mp
import customtkinter as ctk

# Multiprocessing init for Windows
if sys.platform.startswith('win'):
    try:
        mp.set_start_method('spawn', force=True)
    except RuntimeError:
        pass

sys.path.insert(0, os.path.dirname(__file__))

def show_startup_hub():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Enterprise Document Hub - Launchpad")
    root.geometry("500x350")
    root.resizable(False, False)

    # Center
    root.update_idletasks()
    w, h = 500, 350
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"+{x}+{y}")

    ctk.CTkLabel(root, text="DOC GEN ENTERPRISE", font=("Inter", 24, "bold"), text_color="#3b82f6").pack(pady=(40, 10))
    ctk.CTkLabel(root, text="Selectați modul de operare", font=("Inter", 14)).pack(pady=(0, 30))

    def launch_desktop():
        root.destroy()
        from ui.main_window import EnterpriseApp
        app = EnterpriseApp()
        app.mainloop()

    def launch_web():
        root.destroy()
        print("Starting Web Server on http://localhost:5000...")
        import web_api
        from core.engine import DocumentEngine
        # We need a main_app instance for web_api
        from ui.main_window import EnterpriseApp
        # Using a minimal version for web or just withdraw the full one
        # Note: on some systems withdraw() might still trigger DPI scaling logic
        # if the engine hasn't fully detached.
        try:
            app = EnterpriseApp()
            app.withdraw()
            import threading
            threading.Thread(target=web_api.start_server, args=(app,), daemon=True).start()
            import webbrowser
            webbrowser.open("http://localhost:5000")
            app.mainloop()
        except Exception as e:
            print(f"Critical Error starting server: {e}")

    ctk.CTkButton(root, text="Desktop Application", height=50, width=300,
                  font=("Inter", 15, "bold"), command=launch_desktop).pack(pady=10)
    ctk.CTkButton(root, text="Web Dashboard", height=50, width=300,
                  font=("Inter", 15, "bold"), fg_color="#475569", command=launch_web).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_startup_hub()
