import tkinter as tk
from tkinter import ttk
import json
from ui_utils import add_tooltip
import customtkinter as ctk

def setup_audit_tab(app, parent):
    frame = parent
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Enterprise Toolbar
    top_frame = ctk.CTkFrame(frame)
    top_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

    ctk.CTkLabel(top_frame, text="Filtru Acțiune:").pack(side='left', padx=10)
    app.audit_filter = tk.StringVar()
    filter_entry = ctk.CTkEntry(top_frame, textvariable=app.audit_filter, width=250, placeholder_text="Caută în log-uri...")
    filter_entry.pack(side='left', padx=10)
    filter_entry.bind('<KeyRelease>', lambda e: app.load_audit_log())

    ctk.CTkButton(top_frame, text="🔄 Refresh", width=120, command=app.load_audit_log).pack(side='right', padx=10)
    ctk.CTkButton(top_frame, text="📊 Export CSV", width=120, fg_color="#059669", command=app.export_audit_csv).pack(side='right', padx=5)

    # Modern Treeview for logs
    tree_container = ctk.CTkFrame(frame)
    tree_container.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))
    tree_container.grid_rowconfigure(0, weight=1)
    tree_container.grid_columnconfigure(0, weight=1)

    style = ttk.Style()
    style.configure("Audit.Treeview", font=("Segoe UI", 10), rowheight=30)
    style.configure("Audit.Treeview.Heading", font=("Segoe UI", 11, "bold"))

    app.audit_tree = ttk.Treeview(tree_container, columns=('timestamp', 'user', 'action', 'details'),
                                  show='headings', style="Audit.Treeview")

    app.audit_tree.heading('timestamp', text='🕒 Timestamp')
    app.audit_tree.heading('user', text='👤 User')
    app.audit_tree.heading('action', text='⚡ Acțiune')
    app.audit_tree.heading('details', text='📝 Detalii')

    app.audit_tree.column('timestamp', width=180, stretch=False)
    app.audit_tree.column('user', width=120, stretch=False)
    app.audit_tree.column('action', width=180, stretch=False)
    app.audit_tree.column('details', width=600)

    app.audit_tree.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    scroll = ctk.CTkScrollbar(tree_container, command=app.audit_tree.yview)
    scroll.grid(row=0, column=1, sticky='ns')
    app.audit_tree.configure(yscrollcommand=scroll.set)

    app.load_audit_log()
