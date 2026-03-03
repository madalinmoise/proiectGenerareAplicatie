import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab
from tkinter import ttk, messagebox
import pandas as pd

class ExcelViewerTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(toolbar, text="Excel Data Explorer", font=("Inter", 16, "bold")).pack(side="left", padx=10)
        ctk.CTkButton(toolbar, text="Load/Refresh", width=120, command=self.refresh_data).pack(side="left", padx=10)

        # Search
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, placeholder_text="Search in data...", width=250)
        search_entry.pack(side="right", padx=10)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_data())

        # Treeview
        container = ctk.CTkFrame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(container, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scroll = ctk.CTkScrollbar(container, command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        self.df = None
        self.refresh_data()

    def refresh_data(self):
        self.df = self.engine.load_data()
        if self.df is not None:
            self.display_df(self.df)

    def display_df(self, df):
        # Clear
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for idx, row in df.head(100).iterrows():
            self.tree.insert("", "end", values=list(row))

    def filter_data(self):
        if self.df is None: return
        term = self.search_var.get().lower()
        if not term:
            self.display_df(self.df)
            return

        filtered = self.df[self.df.apply(lambda row: row.astype(str).str.lower().str.contains(term).any(), axis=1)]
        self.display_df(filtered)
