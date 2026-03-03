import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab

class SettingsTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(container, text="System Preferences", font=("Inter", 18, "bold")).pack(anchor="w", padx=20, pady=20)

        # Theme toggle
        self.theme_var = ctk.StringVar(value=self.engine.config.get('theme', 'dark'))
        ctk.CTkLabel(container, text="Appearance Mode").pack(anchor="w", padx=30)
        ctk.CTkOptionMenu(container, values=["Light", "Dark", "System"],
                          variable=self.theme_var, command=self.change_theme).pack(anchor="w", padx=30, pady=10)

    def change_theme(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        self.engine.set_config({'theme': new_mode})
