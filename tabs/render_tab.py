# tabs/render_tab.py

import tkinter as tk

from tkinter import ttk, filedialog

from ui_utils import add_tooltip

import os



def setup_render_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(10, weight=1)

    frame.grid_columnconfigure(1, weight=1)



    # 1. Fișiere șablon

    ttk.Label(frame, text="0. Fișiere șablon (render):").grid(row=0, column=0, sticky='w', padx=5, pady=5)

    app.render_files_listbox = tk.Listbox(frame, height=4, selectmode=tk.EXTENDED)

    app.render_files_listbox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=app.render_files_listbox.yview)

    scrollbar.grid(row=0, column=2, sticky='ns')

    app.render_files_listbox.configure(yscrollcommand=scrollbar.set)

    

    btn_lib_frame = ttk.Frame(frame)

    btn_lib_frame.grid(row=0, column=3, padx=5, pady=5, sticky='n')

    ttk.Button(btn_lib_frame, text="Adaugă", command=app.add_render_files).pack(pady=2)

    ttk.Button(btn_lib_frame, text="Șterge", command=app.remove_render_files).pack(pady=2)



    # Date intrare

    ttk.Label(frame, text="1. Selectați fișierul de date (Excel):").grid(row=1, column=0, sticky='w', padx=5, pady=5)

    ttk.Entry(frame, textvariable=app.data_file_path, width=50).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    ttk.Button(frame, text="Răsfoiește", command=app.browse_data_file).grid(row=1, column=2, padx=5, pady=5)



    # Notă: Selecția de foaie a fost eliminată (se folosește automat prima foaie)



    ttk.Label(frame, text="2. Alege coloana pentru numele folderelor:").grid(row=2, column=0, sticky='w', padx=5, pady=5)

    app.folder_column_combo = ttk.Combobox(frame, textvariable=app.folder_column, state='readonly')

    app.folder_column_combo.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    add_tooltip(app.folder_column_combo, "Documentele fiecărui rând vor fi puse într-un folder cu acest nume (ex: Nume_Prenume)")



    ttk.Label(frame, text="3. Director output:").grid(row=3, column=0, sticky='w', padx=5, pady=5)

    ttk.Entry(frame, textvariable=app.output_dir_path, width=50).grid(row=3, column=1, padx=5, pady=5, sticky='ew')

    ttk.Button(frame, text="Răsfoiește", command=app.browse_output_dir).grid(row=3, column=2, padx=5, pady=5)



    ttk.Label(frame, text="4. Model nume fișier:").grid(row=4, column=0, sticky='w', padx=5, pady=5)

    entry_filename = ttk.Entry(frame, textvariable=app.filename_pattern, width=50)

    entry_filename.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    add_tooltip(entry_filename, "Folosiși {Nume_Coloană} pentru date dinamice")



    # Dashboard Statistici Live (Feature 5)

    app.dash_frame = ttk.LabelFrame(frame, text="📈 Dashboard Statistici Live")

    app.dash_frame.grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

    

    app.lbl_stat_total = ttk.Label(app.dash_frame, text="Total: 0")

    app.lbl_stat_total.pack(side='left', padx=10)

    app.lbl_stat_success = ttk.Label(app.dash_frame, text="Succes: 0", foreground='green')

    app.lbl_stat_success.pack(side='left', padx=10)

    app.lbl_stat_error = ttk.Label(app.dash_frame, text="Erori: 0", foreground='red')

    app.lbl_stat_error.pack(side='left', padx=10)

    

    app.progress_bar = ttk.Progressbar(app.dash_frame, orient='horizontal', length=200, mode='determinate')

    app.progress_bar.pack(side='right', padx=10, fill='x', expand=True)



    # Opțiuni

    adv_frame = ttk.LabelFrame(frame, text="Opțiuni Avansate")

    adv_frame.grid(row=6, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

    ttk.Checkbutton(adv_frame, text="Procesare paralelă", variable=app.multiprocessing_var).pack(anchor='w', padx=5)

    ttk.Checkbutton(adv_frame, text="Generează și PDF", variable=app.pdf_var).pack(anchor='w', padx=5)

    ttk.Checkbutton(adv_frame, text="Arhivă ZIP per rând", variable=app.zip_per_row_var).pack(anchor='w', padx=5)



    btn_action_frame = ttk.Frame(frame)

    btn_action_frame.grid(row=7, column=0, columnspan=4, pady=5)

    app.render_btn = ttk.Button(btn_action_frame, text="Generează documente", command=app.start_render)

    app.render_btn.pack(side='left', padx=5)

    

    app.web_wizard_btn = ttk.Button(btn_action_frame, text="Deschide Web Wizard", command=app.open_web_wizard)

    app.web_wizard_btn.pack(side='left', padx=5)



    ttk.Checkbutton(frame, text="Reia de la ultimul checkpoint", variable=app.auto_recovery_var).grid(row=8, column=0, columnspan=4, pady=5)



    # Navigation (Feature 6)

    nav_frame = ttk.Frame(frame)

    nav_frame.grid(row=9, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

    

    app.btn_prev_step_2 = ttk.Button(nav_frame, text="Pasul 1: Extragere", command=lambda: app.notebook.set("Pasul 1: Extrage placeholders"))

    app.btn_prev_step_2.pack(side='left')

    

    app.btn_next_step_2 = ttk.Button(nav_frame, text="Pasul 3: Vizualizare & Verificare", 
                                     command=lambda: app.notebook.set("4. Vizualizare Excel")) # Excel Viewer is index 4

    app.btn_next_step_2.pack(side='right')



    # Previzualizare

    preview_frame = ttk.LabelFrame(frame, text="Previzualizare")

    preview_frame.grid(row=10, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

    app.render_preview_text = tk.Text(preview_frame, height=5, state='disabled')

    app.render_preview_text.pack(fill='both', expand=True, padx=5, pady=5)

