import customtkinter as ctk
from ui.components.base_tab import EnterpriseTab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ReportsTab(EnterpriseTab):
    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(sidebar, text="Analytic Controls", font=("Inter", 16, "bold")).pack(pady=20)

        ctk.CTkButton(sidebar, text="Grade Cercetare (CS..)", command=self.show_research).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="Statut Studenți", command=self.show_students).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(sidebar, text="Integritate Date", command=self.show_integrity, fg_color="#ef4444").pack(fill="x", padx=10, pady=5)

        self.chart_container = ctk.CTkFrame(self)
        self.chart_container.grid(row=0, column=1, sticky="nsew")
        self.chart_container.grid_rowconfigure(0, weight=1)
        self.chart_container.grid_columnconfigure(0, weight=1)

        self.placeholder_lbl = ctk.CTkLabel(self.chart_container, text="Select analysis type from the sidebar")
        self.placeholder_lbl.pack(expand=True)

    def _display_plot(self, fig):
        for w in self.chart_container.winfo_children(): w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        plt.close(fig)

    def show_research(self):
        stats = self.engine.get_stats().get('research_grades', {})
        if not stats: return
        fig, ax = plt.subplots(figsize=(8, 6))
        pd.Series(stats).plot(kind='bar', ax=ax, color='#3b82f6')
        ax.set_title("Distribuție Grade Cercetare")
        self._display_plot(fig)

    def show_students(self):
        stats = self.engine.get_stats().get('student_types', {})
        if not stats: return
        fig, ax = plt.subplots(figsize=(8, 6))
        pd.Series(stats).plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title("Tipuri Studenți / Participanți")
        self._display_plot(fig)

    def show_integrity(self):
        audit = self.engine.get_stats().get('integrity', {})
        fig, ax = plt.subplots(figsize=(8, 6))
        labels = ['Empty Rows', 'Help Requested']
        vals = [audit.get('empty_row_count', 0), audit.get('help_request_count', 0)]
        ax.bar(labels, vals, color=['#ef4444', '#f59e0b'])
        ax.set_title("Data Integrity Audit")
        self._display_plot(fig)
