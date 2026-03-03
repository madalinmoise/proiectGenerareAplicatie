import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab
from tkinter import filedialog, messagebox

class ExtractTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Template list
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(list_frame, text="Current Templates", font=("Inter", 16, "bold")).pack(anchor="w", padx=20, pady=10)

        self.files_box = ctk.CTkTextbox(list_frame, height=100)
        self.files_box.pack(fill="x", padx=20, pady=5)
        self.refresh_files()

        # Extract Controls
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(btn_frame, text="🔍 Extract Placeholders", command=self.do_extract).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="➕ Add Templates", fg_color="#10b981", command=self.add_files).pack(side="left", padx=10, pady=10)

    def refresh_files(self):
        self.files_box.configure(state="normal")
        self.files_box.delete("1.0", "end")
        for f in self.engine.config.get('template_files', []):
            self.files_box.insert("end", f"{f}\n")
        self.files_box.configure(state="disabled")

    def add_files(self):
        fs = filedialog.askopenfilenames(filetypes=[("Word", "*.docx")])
        if fs:
            current = self.engine.config.get('template_files', [])
            self.engine.set_config({'template_files': list(set(current + list(fs)))})
            self.refresh_files()

    def do_extract(self):
        placeholders, mapping = self.engine.extract_placeholders()
        if placeholders:
            messagebox.showinfo("Extraction", f"Found {len(placeholders)} unique placeholders.")
        else:
            messagebox.showwarning("Extraction", "No placeholders found in selected files.")

    def on_engine_event(self, event_type, data):
        if event_type == 'config_updated':
            self.refresh_files()
