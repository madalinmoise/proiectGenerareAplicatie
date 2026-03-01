# tabs/audit_tab.py

import tkinter as tk

from tkinter import ttk

import json

from ui_utils import add_tooltip



def setup_audit_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(1, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    top_frame = ttk.Frame(frame)

    top_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    ttk.Label(top_frame, text="Filtru acțiune:").pack(side='left', padx=5)

    app.audit_filter = tk.StringVar()

    filter_entry = ttk.Entry(top_frame, textvariable=app.audit_filter, width=20)

    filter_entry.pack(side='left', padx=5)

    ttk.Button(top_frame, text="Aplică", command=app.load_audit_log).pack(side='left', padx=5)

    ttk.Button(top_frame, text="Reîmprospătează", command=app.load_audit_log).pack(side='left', padx=5)



    # Treeview pentru log

    tree_frame = ttk.Frame(frame)

    tree_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    tree_frame.grid_rowconfigure(0, weight=1)

    tree_frame.grid_columnconfigure(0, weight=1)



    app.audit_tree = ttk.Treeview(tree_frame, columns=('timestamp', 'user', 'action', 'details'), show='headings')

    app.audit_tree.heading('timestamp', text='Timestamp')

    app.audit_tree.heading('user', text='User')

    app.audit_tree.heading('action', text='Acțiune')

    app.audit_tree.heading('details', text='Detalii')

    app.audit_tree.column('timestamp', width=150)

    app.audit_tree.column('user', width=100)

    app.audit_tree.column('action', width=150)

    app.audit_tree.column('details', width=400)

    app.audit_tree.grid(row=0, column=0, sticky='nsew')

    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=app.audit_tree.yview)

    scroll.grid(row=0, column=1, sticky='ns')

    app.audit_tree.configure(yscrollcommand=scroll.set)



    app.load_audit_log()

