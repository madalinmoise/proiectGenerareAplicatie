import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab
from tkinter import ttk

class AuditTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(toolbar, text="System Event Log", font=("Inter", 16, "bold")).pack(side="left", padx=10)

        self.log_container = ctk.CTkFrame(self)
        self.log_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.log_container.grid_columnconfigure(0, weight=1)
        self.log_container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.log_container, columns=("time", "event", "details"), show="headings")
        self.tree.heading("time", text="Timestamp")
        self.tree.heading("event", text="Event Type")
        self.tree.heading("details", text="Technical Details")
        self.tree.column("time", width=150)
        self.tree.column("event", width=150)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scroll = ctk.CTkScrollbar(self.log_container, command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

    def on_engine_event(self, event_type, data):
        from datetime import datetime
        t = datetime.now().strftime("%H:%M:%S")
        self.tree.insert("", 0, values=(t, event_type, str(data)))
