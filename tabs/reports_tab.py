import tkinter as tk
from tkinter import ttk
from ui_utils import add_tooltip

def setup_reports_tab(app, parent):
    frame = parent
    frame.grid_rowconfigure(3, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Header section
    header_frame = ttk.Frame(frame)
    header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
    ttk.Label(header_frame, text="📊 Centru de Raportare Enterprise", font=("Inter", 18, "bold")).pack(side='left')

    # Source Selection
    source_frame = ttk.LabelFrame(frame, text="Configurare Sursă Date")
    source_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

    ttk.Label(source_frame, text="Coloană Activă:").pack(side='left', padx=5, pady=10)
    app.report_source_col = tk.StringVar()
    app.report_source_combo = ttk.Combobox(source_frame, textvariable=app.report_source_col, state='readonly', width=40)
    app.report_source_combo.pack(side='left', padx=5, pady=10)

    def refresh_report_cols():
        if hasattr(app, 'global_excel_df') and app.global_excel_df is not None:
            cols = list(app.global_excel_df.columns)
            app.report_source_combo['values'] = cols
            if cols and not app.report_source_col.get():
                app.report_source_col.set(cols[0])

    app.refresh_report_cols = refresh_report_cols
    ttk.Button(source_frame, text="🔄 Refresh", command=refresh_report_cols).pack(side='left', padx=5)

    # Unified Statistics Dashboard
    dashboard_frame = ttk.Frame(frame)
    dashboard_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
    dashboard_frame.grid_columnconfigure(0, weight=1)
    dashboard_frame.grid_columnconfigure(1, weight=3)
    dashboard_frame.grid_rowconfigure(0, weight=1)

    # Left: Button grid
    controls_container = ttk.LabelFrame(dashboard_frame, text="Acțiuni & Analize")
    controls_container.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

    # Use a canvas/scrollbar for buttons if too many
    btn_grid = ttk.Frame(controls_container)
    btn_grid.pack(fill='both', expand=True, padx=5, pady=5)

    # Research & Academic
    ttk.Label(btn_grid, text="Academic & Cercetare", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(5, 2))
    ttk.Button(btn_grid, text="Grade Cercetare (CSI..)", command=app.stats_research_grades).pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Tipuri Studenți", command=app.stats_student_types).pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Activități Proiect", command=app.stats_activities).pack(fill='x', pady=2)

    # HR & General
    ttk.Label(btn_grid, text="Resurse Umane", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(10, 2))
    ttk.Button(btn_grid, text="Distribuție Departament", command=app.stats_departments).pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Nivel Educație", command=app.stats_education_level).pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Gen & Demografice", command=app.stats_gender).pack(fill='x', pady=2)

    # Integrity & Audit
    ttk.Label(btn_grid, text="Integritate Date", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(10, 2))
    ttk.Button(btn_grid, text="Cine are celule goale?", command=app.audit_empty_cells).pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Solicitări Ajutor", command=app.audit_help_requests).pack(fill='x', pady=2)

    # Manual Tool
    ttk.Label(btn_grid, text="Analiză Manuală", font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(10, 2))
    app.manual_chart_type = tk.StringVar(value='bar')
    ttk.Combobox(btn_grid, textvariable=app.manual_chart_type, values=['bar', 'pie', 'line'], state='readonly').pack(fill='x', pady=2)
    ttk.Button(btn_grid, text="Generează din Coloană", command=app.generate_manual_stat).pack(fill='x', pady=5)

    # Right: Chart Display
    app.report_canvas_frame = ttk.Frame(dashboard_frame, style='White.TFrame')
    app.report_canvas_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    app.report_canvas_frame.grid_rowconfigure(0, weight=1)
    app.report_canvas_frame.grid_columnconfigure(0, weight=1)

    # Footer
    footer = ttk.Frame(frame)
    footer.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
    ttk.Button(footer, text="💾 Exportă Imagine Grafic", command=app.export_report_image).pack(side='right')

    refresh_report_cols()
