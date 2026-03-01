# tabs/extract_tab.py

import tkinter as tk

from tkinter import ttk, filedialog

import threading

from template_utils import extract_all_placeholders_from_files, generate_excel_template

from ui_utils import add_tooltip

from config import config

_FONT = ("Segoe UI", 11)
_FONT_BOLD = ("Segoe UI", 11, "bold")


def setup_extract_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(3, weight=1)

    frame.grid_columnconfigure(1, weight=1)



    ttk.Label(frame, text="Fișiere șablon:", font=_FONT).grid(row=0, column=0, sticky='w', padx=5, pady=5)

    app.extract_files_listbox = tk.Listbox(frame, height=5, selectmode=tk.EXTENDED, font=_FONT)

    app.extract_files_listbox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=app.extract_files_listbox.yview)

    scrollbar.grid(row=0, column=2, sticky='ns')

    app.extract_files_listbox.configure(yscrollcommand=scrollbar.set)

    if hasattr(app, 'setup_drop_target'):

        app.setup_drop_target(app.extract_files_listbox, app.on_extract_drop)

    app.make_listbox_drag_drop(app.extract_files_listbox)

    app.add_context_menu(app.extract_files_listbox, app.add_extract_files, app.remove_extract_files)



    btn_frame = ttk.Frame(frame)

    btn_frame.grid(row=0, column=3, padx=5, pady=5, sticky='n')

    btn_add = ttk.Button(btn_frame, text="Adaugă fișiere", command=app.add_extract_files)

    btn_add.pack(pady=2, fill='x')

    add_tooltip(btn_add, "Adaugă fișiere șablon (.docx, .odt, .txt, .html)")

    btn_remove = ttk.Button(btn_frame, text="Șterge selectate", command=app.remove_extract_files)

    btn_remove.pack(pady=2, fill='x')

    add_tooltip(btn_remove, "Elimină fișierele selectate din listă")



    ttk.Label(frame, text="Nume fișier Excel de ieșire:", font=_FONT).grid(row=1, column=0, sticky='w', padx=5, pady=5)

    ttk.Entry(frame, textvariable=app.excel_output_path, width=50, font=_FONT).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    btn_save = ttk.Button(frame, text="Salvează ca...", command=app.browse_excel_output)

    btn_save.grid(row=1, column=3, padx=5, pady=5)

    add_tooltip(btn_save, "Alege locația și numele fișierului Excel")



    btn_action_frame = ttk.Frame(frame)

    btn_action_frame.grid(row=2, column=0, columnspan=4, pady=5)

    app.extract_btn = ttk.Button(btn_action_frame, text="Extrage și generează Excel", command=app.start_extract)

    app.extract_btn.pack(side='left', padx=5, ipady=4)

    add_tooltip(app.extract_btn, "Extrage placeholder-urile și creează un fișier Excel cu acestea")

    app.extract_only_btn = ttk.Button(btn_action_frame, text="Doar extragere", command=app.start_extract_only)

    app.extract_only_btn.pack(side='left', padx=5, ipady=4)

    add_tooltip(app.extract_only_btn, "Extrage placeholder-urile fără a genera Excel")



    app.extract_placeholder_frame = ttk.LabelFrame(frame, text="Placeholder-uri găsite (dublu-click pentru a deschide în Vizualizare)")

    app.extract_placeholder_frame.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

    app.extract_placeholder_frame.grid_rowconfigure(0, weight=1)

    app.extract_placeholder_frame.grid_columnconfigure(0, weight=1)



    app.extract_placeholder_listbox = tk.Listbox(app.extract_placeholder_frame, font=_FONT)

    app.extract_placeholder_listbox.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

    scroll_ph = ttk.Scrollbar(app.extract_placeholder_frame, orient=tk.VERTICAL, command=app.extract_placeholder_listbox.yview)

    scroll_ph.grid(row=0, column=1, sticky='ns')

    app.extract_placeholder_listbox.configure(yscrollcommand=scroll_ph.set)

    app.extract_placeholder_listbox.bind('<Double-1>', app.on_extract_placeholder_double_click)



    ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=4, sticky='ew', pady=10)



    footer_frame = ttk.Frame(frame)

    footer_frame.grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=5)



    instr = ttk.Label(footer_frame, text="După generare, completați fișierul Excel cu datele dorite (fiecare rând = un set de valori).\n"
                                   "Apoi treceți la Pasul 2.", justify='left', font=("Segoe UI", 10))

    instr.pack(side='left')



    app.btn_next_step_1 = ttk.Button(footer_frame, text="Pasul 2: Randare Documente ->",
                               command=lambda: app.notebook.set("Pasul 2: Generează documente"))

    app.btn_next_step_1.pack(side='right', ipady=4)

    add_tooltip(app.btn_next_step_1, "Treceți la tab-ul de generare a documentelor")
