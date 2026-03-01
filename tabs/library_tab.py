# tabs/library_tab.py

import tkinter as tk

from tkinter import ttk

from ui_utils import add_tooltip



def setup_library_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(1, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    btn_frame = ttk.Frame(frame)

    btn_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    ttk.Button(btn_frame, text="Importă șablon în bibliotecă", command=app.import_to_library).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Adaugă la proiect", command=app.add_from_library).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Șterge din bibliotecă", command=app.delete_from_library).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Backup proiect", command=app.backup_project).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Restaurare", command=app.restore_backup).pack(side='left', padx=5)



    tree_frame = ttk.Frame(frame)

    tree_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    tree_frame.grid_rowconfigure(0, weight=1)

    tree_frame.grid_columnconfigure(0, weight=1)



    app.library_tree = ttk.Treeview(tree_frame, columns=('id', 'nume', 'categorie', 'versiune', 'autor', 'modificat'), show='headings')

    app.library_tree.heading('id', text='ID')

    app.library_tree.heading('nume', text='Nume')

    app.library_tree.heading('categorie', text='Categorie')

    app.library_tree.heading('versiune', text='Versiune')

    app.library_tree.heading('autor', text='Autor')

    app.library_tree.heading('modificat', text='Modificat')

    app.library_tree.column('id', width=50)

    app.library_tree.column('nume', width=200)

    app.library_tree.column('categorie', width=100)

    app.library_tree.column('versiune', width=80)

    app.library_tree.column('autor', width=100)

    app.library_tree.column('modificat', width=150)

    app.library_tree.grid(row=0, column=0, sticky='nsew')

    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=app.library_tree.yview)

    scroll.grid(row=0, column=1, sticky='ns')

    app.library_tree.configure(yscrollcommand=scroll.set)



    app.load_library()

