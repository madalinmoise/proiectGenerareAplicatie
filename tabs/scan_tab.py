# tabs/scan_tab.py

import tkinter as tk

from tkinter import ttk

from ui_utils import add_tooltip

from config import config



def setup_scan_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(3, weight=1)

    frame.grid_columnconfigure(1, weight=1)



    ttk.Label(frame, text="Fișiere șablon:").grid(row=0, column=0, sticky='w', padx=5, pady=5)

    app.scan_files_listbox = tk.Listbox(frame, height=5, selectmode=tk.EXTENDED)

    app.scan_files_listbox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=app.scan_files_listbox.yview)

    scrollbar.grid(row=0, column=2, sticky='ns')

    app.scan_files_listbox.configure(yscrollcommand=scrollbar.set)

    if hasattr(app, 'setup_drop_target'):

        app.setup_drop_target(app.scan_files_listbox, app.on_scan_drop)

    app.make_listbox_drag_drop(app.scan_files_listbox)

    app.add_context_menu(app.scan_files_listbox, app.add_scan_files, app.remove_scan_files)



    btn_frame = ttk.Frame(frame)

    btn_frame.grid(row=0, column=3, padx=5, pady=5, sticky='n')

    btn_add = ttk.Button(btn_frame, text="Adaugă fișiere", command=app.add_scan_files)

    btn_add.pack(pady=2)

    add_tooltip(btn_add, "Adaugă fișiere șablon")

    btn_remove = ttk.Button(btn_frame, text="Șterge selectate", command=lambda: app.remove_selected_files(app.scan_files_listbox))

    btn_remove.pack(pady=2)

    add_tooltip(btn_remove, "Elimină fișierele selectate din listă")



    action_frame = ttk.Frame(frame)

    action_frame.grid(row=1, column=0, columnspan=4, pady=5)

    app.scan_interactive_btn = ttk.Button(action_frame, text="Scanează interactiv", command=app.start_scan_interactive)

    app.scan_interactive_btn.pack(side='left', padx=5)

    add_tooltip(app.scan_interactive_btn, "Analizează placeholder-urile și arată problemele")

    app.correct_btn = ttk.Button(action_frame, text="Corectare automată (rapidă)", command=app.start_correct)

    app.correct_btn.pack(side='left', padx=5)

    add_tooltip(app.correct_btn, "Corectează automat placeholder-urile (spașii, diacritice)")

    app.scan_report_btn = ttk.Button(action_frame, text="Generează raport text", command=app.start_scan_report)

    app.scan_report_btn.pack(side='left', padx=5)

    add_tooltip(app.scan_report_btn, "Creează un raport detaliat în fereastra de log")

    app.undo_btn = ttk.Button(action_frame, text="↩ Undo ultima corecție", command=app.undo_last_correction)

    app.undo_btn.pack(side='left', padx=5)

    add_tooltip(app.undo_btn, "Revino la versiunea anterioară a fișierelor modificate")



    app.results_frame = ttk.LabelFrame(frame, text="Rezultate scanare")

    app.results_frame.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

    app.results_frame.grid_rowconfigure(0, weight=1)

    app.results_frame.grid_columnconfigure(0, weight=1)

    app.initial_label = ttk.Label(app.results_frame, text="Selectați fișiere și apăsați 'Scanează interactiv'.")

    app.initial_label.grid(row=0, column=0, sticky='nsew')



    app.history_frame = ttk.LabelFrame(frame, text="Istoric corecții")

    app.history_frame.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

    app.history_listbox = tk.Listbox(app.history_frame, height=3)

    app.history_listbox.pack(fill='x', padx=2, pady=2)

