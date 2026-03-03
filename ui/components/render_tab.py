import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab
from tkinter import filedialog, messagebox

class RenderTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Source Selection
        src_frame = ctk.CTkFrame(self)
        src_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(src_frame, text="1. Data Configuration", font=("Inter", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        self.data_path_var = ctk.StringVar(value=self.engine.config.get('data_file', ''))
        path_frame = ctk.CTkFrame(src_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkEntry(path_frame, textvariable=self.data_path_var, placeholder_text="Select Excel Data...").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(path_frame, text="Browse", width=100, command=self.browse_data).pack(side="right")

        # Action Hub
        hub = ctk.CTkFrame(self)
        hub.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(hub, text="2. Production Controls", font=("Inter", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        self.start_btn = ctk.CTkButton(hub, text="🚀 START BATCH GENERATION", height=50, font=("Inter", 14, "bold"),
                                       command=self.start_generation)
        self.start_btn.pack(pady=20, padx=50, fill="x")

        self.stop_btn = ctk.CTkButton(hub, text="🛑 EMERGENCY STOP", fg_color="#ef4444", hover_color="#dc2626",
                                      command=self.engine.stop_job, state="disabled")
        self.stop_btn.pack(pady=10, padx=50, fill="x")

    def browse_data(self):
        f = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if f:
            self.data_path_var.set(f)
            self.engine.set_config({'data_file': f})

    def start_generation(self):
        options = {
            'parallel': True,
            'pdf_gen': True
        }
        if self.engine.start_job(options):
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")

    def on_engine_event(self, event_type, data):
        if event_type == 'job_finished':
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            messagebox.showinfo("Production Hub", "Batch process completed.")
