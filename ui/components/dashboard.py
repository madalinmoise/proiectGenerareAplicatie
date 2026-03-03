import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab

class DashboardTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Hero Section
        hero = ctk.CTkFrame(self, fg_color=("#3b82f6", "#1e3a8a"), corner_radius=15, height=140)
        hero.pack(fill="x", padx=20, pady=20)
        hero.pack_propagate(False)
        ctk.CTkLabel(hero, text="Enterprise Command Center", font=("Inter", 24, "bold"), text_color="white").pack(pady=(25, 2))
        ctk.CTkLabel(hero, text="High-Performance Document Generation Engine", font=("Inter", 14), text_color="white").pack()

        # Stats Area
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        for i in range(3): stats_frame.grid_columnconfigure(i, weight=1)

        self.card_rows = self.create_card(stats_frame, "Records", "0", 0)
        self.card_cols = self.create_card(stats_frame, "Parameters", "0", 1)
        self.card_status = self.create_card(stats_frame, "Engine Status", "Ready", 2)

        # Active Job Info
        self.job_frame = ctk.CTkFrame(self, corner_radius=12)
        self.job_frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(self.job_frame, text="Active Job Queue", font=("Inter", 16, "bold")).pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.job_frame, width=400)
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        self.status_lbl = ctk.CTkLabel(self.job_frame, text="No active jobs in queue")
        self.status_lbl.pack()

    def create_card(self, master, title, val, col):
        card = ctk.CTkFrame(master, corner_radius=10, height=100)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        ctk.CTkLabel(card, text=title, font=("Inter", 12)).pack(pady=(15, 0))
        lbl = ctk.CTkLabel(card, text=val, font=("Inter", 20, "bold"))
        lbl.pack(pady=(0, 15))
        return lbl

    def on_engine_event(self, event_type, data):
        if event_type == 'job_progress':
            p = data['current'] / data['total']
            self.progress_bar.set(p)
            self.status_lbl.configure(text=f"Processing {data['current']} of {data['total']}...")
        elif event_type == 'job_started':
            self.card_status.configure(text="RUNNING", text_color="#3b82f6")
        elif event_type == 'job_finished':
            self.card_status.configure(text="READY", text_color=("gray10", "gray90"))
            self.progress_bar.set(1)
            self.status_lbl.configure(text="Job completed successfully.")
