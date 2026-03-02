# tabs/editor_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext

from ui_utils import add_tooltip



def setup_editor_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(2, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # Listă șabloane

    ttk.Label(frame, text="Șabloane:").grid(row=0, column=0, sticky='w', padx=5)

    app.editor_listbox = tk.Listbox(frame, height=6)

    app.editor_listbox.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    scroll_ed = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=app.editor_listbox.yview)

    scroll_ed.grid(row=1, column=1, sticky='ns')

    app.editor_listbox.configure(yscrollcommand=scroll_ed.set)

    app.refresh_editor_list()



    # Căutare/înlocuire

    search_frame = ttk.LabelFrame(frame, text="Căutare și înlocuire")

    search_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)



    ttk.Label(search_frame, text="Caută:").grid(row=0, column=0, sticky='w', padx=5)

    app.search_var = tk.StringVar()

    ttk.Entry(search_frame, textvariable=app.search_var, width=30).grid(row=0, column=1, padx=5)



    ttk.Label(search_frame, text="Înlocuiește cu:").grid(row=1, column=0, sticky='w', padx=5)

    app.replace_var = tk.StringVar()

    ttk.Entry(search_frame, textvariable=app.replace_var, width=30).grid(row=1, column=1, padx=5)



    btn_frame = ttk.Frame(search_frame)

    btn_frame.grid(row=2, column=0, columnspan=2, pady=5)

    ttk.Button(btn_frame, text="Caută în toate", command=app.search_in_templates).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Înlocuiește în toate", command=app.replace_in_templates).pack(side='left', padx=5)



    app.editor_text = scrolledtext.ScrolledText(frame, wrap='word', height=15)

    app.editor_text.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

