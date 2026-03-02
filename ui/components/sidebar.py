import customtkinter as ctk
from ui_constants import PRIMARY_COLOR

class EnterpriseSidebar(ctk.CTkFrame):
    def __init__(self, master, tab_callback, **kwargs):
        super().__init__(master, width=240, corner_radius=0, **kwargs)
        self.tab_callback = tab_callback

        self.grid_rowconfigure(10, weight=1)

        # Branding
        self.logo_label = ctk.CTkLabel(self, text="DOC GEN\nENTERPRISE",
                                      font=("Inter", 20, "bold"),
                                      text_color=PRIMARY_COLOR)
        self.logo_label.grid(row=0, column=0, padx=20, pady=30)

        self.buttons = {}
        self.create_nav_button("Dashboard", "Dashboard", 1)
        self.create_nav_button("Extracție", "Pasul 1: Extrage placeholders", 2)
        self.create_nav_button("Randare", "Pasul 2: Generează documente", 3)
        self.create_nav_button("Analiză & Rapoarte", "Rapoarte", 4)
        self.create_nav_button("Audit Log", "Audit Log", 5)
        self.create_nav_button("Setări", "Setări", 6)

        # Select default
        self.select_button("Dashboard")

    def create_nav_button(self, label, tab_name, row):
        btn = ctk.CTkButton(self, text=label, anchor="w",
                            fg_color="transparent", text_color=("gray10", "gray90"),
                            hover_color=("gray70", "gray30"), font=("Inter", 14, "bold"),
                            height=45, corner_radius=8,
                            command=lambda: self.select_button(label, tab_name))
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.buttons[label] = btn

    def select_button(self, label, tab_name=None):
        for btn in self.buttons.values():
            btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

        self.buttons[label].configure(fg_color=PRIMARY_COLOR, text_color="white")
        if tab_name:
            self.tab_callback(tab_name)
