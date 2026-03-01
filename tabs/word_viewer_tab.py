# tabs/word_viewer_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext, filedialog, messagebox

from ui_utils import add_tooltip

import os

from pathlib import Path

from docx import Document

import re



def setup_word_viewer_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(2, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # Toolbar 1: File Selection

    top_frame = ttk.Frame(frame)

    top_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    

    ttk.Label(top_frame, text="Documente generate:").pack(side='left', padx=5)

    app.word_files_combo = ttk.Combobox(top_frame, state='readonly', width=50)

    app.word_files_combo.pack(side='left', padx=5, fill='x', expand=True)

    app.word_files_combo.bind('<<ComboboxSelected>>', lambda e: on_word_combo_select(app))

    

    ttk.Button(top_frame, text="Actualizează lista", command=lambda: refresh_word_file_list(app)).pack(side='left', padx=5)

    ttk.Button(top_frame, text="Deschide folder", command=lambda: os.startfile(app.output_dir_path.get())).pack(side='left', padx=5)



    # Toolbar 2: Search & Navigation

    search_frame = ttk.Frame(frame)

    search_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    

    ttk.Label(search_frame, text="Caută în document:").pack(side='left', padx=5)

    app.word_search_var = tk.StringVar()

    ttk.Entry(search_frame, textvariable=app.word_search_var, width=30).pack(side='left', padx=5)

    ttk.Button(search_frame, text="Caută", command=app.word_viewer_search).pack(side='left', padx=2)

    

    app.word_info_lbl = ttk.Label(search_frame, text="", foreground="blue")

    app.word_info_lbl.pack(side='left', padx=10)



    # Text Viewer

    text_frame = ttk.Frame(frame)

    text_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

    text_frame.grid_rowconfigure(0, weight=1)

    text_frame.grid_columnconfigure(0, weight=1)

    

    app.word_text = scrolledtext.ScrolledText(text_frame, wrap='word', font=('Segoe UI', 10))

    app.word_text.grid(row=0, column=0, sticky='nsew')

    app.word_text.configure(state='disabled')

    

    # Tag configuration

    app.word_text.tag_config("match", background="yellow")

    app.word_text.tag_config("placeholder", foreground="red", font=("Segoe UI", 10, "bold"))



    app.word_current_file = None

    app.word_search_results = []

    app.word_search_index = 0



def refresh_word_file_list(app):

    """Scanează directorul de output pentru fișiere docx și populează combo-ul."""

    out_dir = app.output_dir_path.get()

    if not out_dir or not os.path.exists(out_dir):

        app.word_files_combo['values'] = []

        return

    

    all_docx = []

    for root, dirs, files in os.walk(out_dir):

        for f in files:

            if f.endswith('.docx') and not f.startswith('~$'):

                # Calea relativă la out_dir pentru afișare mai curată

                full_path = os.path.join(root, f)

                rel_path = os.path.relpath(full_path, out_dir)

                all_docx.append(rel_path)

    

    app.word_files_combo['values'] = all_docx

    if all_docx:

        app.log(f"Găsite {len(all_docx)} documente Word generate.")



def on_word_combo_select(app):

    rel_path = app.word_files_combo.get()

    if not rel_path:

        return

    

    full_path = os.path.join(app.output_dir_path.get(), rel_path)

    if os.path.exists(full_path):

        app.word_viewer_load_file(full_path)



def highlight_placeholders_in_viewer(app):

    """Caută și marchează {{...}} sau Â«...Â» în textul încărcat."""

    content = app.word_text.get('1.0', tk.END)

    app.word_text.tag_remove("placeholder", "1.0", tk.END)

    

    patterns = [r'\{\{.*?\}\}', r'«.*?»']

    count = 0

    for pattern in patterns:

        for match in re.finditer(pattern, content):

            start_idx = app.word_text.index(f"1.0 + {match.start()} c")

            end_idx = app.word_text.index(f"1.0 + {match.end()} c")

            app.word_text.tag_add("placeholder", start_idx, end_idx)

            count += 1

    

    if count > 0:

        app.word_info_lbl.configure(text=f"Detecție: {count} placeholder-e găsite.")

    else:

        app.word_info_lbl.configure(text="")



# Notă: Metodele word_viewer_load_file, search etc. trebuie să existe în app.py sau să fie adăugate

