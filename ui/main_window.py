import customtkinter as ctk
import tkinter as tk
from ui.components.sidebar import EnterpriseSidebar
from app import PlaceholderApp

class EnterpriseApp(PlaceholderApp):
    def __init__(self):
        super().__init__()
        self.title("Enterprise Document Hub")
        self.geometry("1200x800")

        # Hide the default toolbar and notebook as we will use our own layout
        for child in self.winfo_children():
            if isinstance(child, (ctk.CTkFrame, tk.Frame)):
                 child.pack_forget()

        # New Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar with our custom callbacks
        self.sidebar = EnterpriseSidebar(self, tab_callback=self.set_enterprise_tab)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Move tabs to our new container
        for name, frame in self.tabs.items():
            frame.master = self.main_container # Hack to move it
            # Actually, the original tabs are in self.notebook which is now hidden.
            # Let's just use the original set method but it updates the sidebar too.
            pass

    def set_enterprise_tab(self, name):
        # Map our sidebar labels to the actual tab names in PlaceholderApp
        mapping = {
            "Dashboard": "Dashboard",
            "Extracție": "Pasul 1: Extrage placeholders",
            "Randare": "Pasul 2: Generează documente",
            "Analiză & Rapoarte": "Rapoarte",
            "Audit Log": "Audit Log",
            "Setări": "Setări"
        }
        actual_name = mapping.get(name, name)
        self.notebook.set(actual_name)

if __name__ == "__main__":
    app = EnterpriseApp()
    app.mainloop()
