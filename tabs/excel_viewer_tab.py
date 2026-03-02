# tabs/excel_viewer_tab.py

import tkinter as tk

import customtkinter as ctk

from tkinter import ttk, messagebox, filedialog

from ui_utils import add_tooltip, ScrollableFrame

import pandas as pd

from pathlib import Path

import re

from docx import Document



def setup_excel_viewer_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(1, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # PanedWindow for side-by-side view (Excel vs Word Preview)

    app.excel_paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)

    app.excel_paned.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)



    # LEFT SIDE: Excel Browser

    left_side = ttk.Frame(app.excel_paned)

    app.excel_paned.add(left_side, weight=2)

    left_side.grid_rowconfigure(2, weight=1)

    left_side.grid_columnconfigure(0, weight=1)



    # Toolbar

    toolbar = ctk.CTkFrame(left_side)

    toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    

    ctk.CTkLabel(toolbar, text="Fișier Excel:").pack(side='left', padx=10)

    app.lbl_loading_excel = ctk.CTkLabel(toolbar, text="Global", text_color="#2196f3")

    app.lbl_loading_excel.pack(side='left', padx=5)

    

    ctk.CTkButton(toolbar, text="Refresh", width=100, command=lambda: refresh_excel_viewer_content(app)).pack(side='left', padx=5)

    

    # BUTON PREVIZUALIZARE LIVE (Nou în Phase 3)

    ctk.CTkButton(toolbar, text="✨ Previzualizare Live", fg_color="#2e7d32", hover_color="#1b5e20",

                  command=app.preview_document).pack(side='left', padx=5)

    

    ctk.CTkLabel(toolbar, text="Căutare:").pack(side='left', padx=(20, 0))

    app.excel_search_var = tk.StringVar()

    search_entry = ctk.CTkEntry(toolbar, textvariable=app.excel_search_var, width=200, placeholder_text="Caută în tabel...")

    search_entry.pack(side='left', padx=5)

    search_entry.bind('<KeyRelease>', lambda e: update_tree_columns(app))

    

    ctk.CTkButton(toolbar, text="X", width=20, command=lambda: [app.excel_search_var.set(""), update_tree_columns(app)]).pack(side='left')

    

    # Column Selector

    columns_container = ttk.LabelFrame(left_side, text="Coloane Vizibile")

    columns_container.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    app.excel_columns_frame = ScrollableFrame(columns_container, height=60)

    app.excel_columns_frame.pack(fill='x', expand=True, padx=2, pady=2)

    app.excel_columns_inner = app.excel_columns_frame.scrollable_frame

    app.excel_visible_vars = {}



    # Treeview

    tree_frame = ttk.Frame(left_side)

    tree_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

    tree_frame.grid_rowconfigure(0, weight=1)

    tree_frame.grid_columnconfigure(0, weight=1)

    

    app.excel_tree = ttk.Treeview(tree_frame, show='headings')

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=app.excel_tree.yview)

    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=app.excel_tree.xview)

    app.excel_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    app.excel_tree.grid(row=0, column=0, sticky='nsew')

    vsb.grid(row=0, column=1, sticky='ns')

    hsb.grid(row=1, column=0, sticky='ew')

    

    app.excel_tree.bind('<<TreeviewSelect>>', lambda e: on_excel_row_select(app))



    # RIGHT SIDE: Word Preview

    right_side = ttk.LabelFrame(app.excel_paned, text="Previzualizare Șablon & Verificare")

    app.excel_paned.add(right_side, weight=1)

    right_side.grid_rowconfigure(1, weight=1)

    right_side.grid_columnconfigure(0, weight=1)



    word_toolbar = ttk.Frame(right_side)

    word_toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    

    ttk.Button(word_toolbar, text="Încarcă Șablon", command=lambda: load_word_template_split(app)).pack(side='left', padx=5)

    app.split_word_label = ttk.Label(word_toolbar, text="Niciun fișier selectat", foreground="gray")

    app.split_word_label.pack(side='left', padx=5)



    app.split_word_text = tk.Text(right_side, wrap='word', state='disabled', font=("Segoe UI", 10))

    app.split_word_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    

    word_scroll = ttk.Scrollbar(right_side, orient=tk.VERTICAL, command=app.split_word_text.yview)

    word_scroll.grid(row=1, column=1, sticky='ns')

    app.split_word_text.configure(yscrollcommand=word_scroll.set)



    app.split_info_var = tk.StringVar(value="Selectați un rând în Excel + clic pe un placeholder.")

    info_lbl = ttk.Label(right_side, textvariable=app.split_info_var, wraplength=300, foreground="blue", font=("Segoe UI", 9, "bold"))

    info_lbl.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=5)



    app.split_word_text.tag_config("placeholder", foreground="red", font=("Segoe UI", 10, "bold"), underline=True)

    app.split_word_text.tag_config("active_placeholder", background="yellow", foreground="red", font=("Segoe UI", 10, "bold"))

    app.split_word_text.tag_bind("placeholder", "<Button-1>", lambda e: on_split_placeholder_click(app, e))



    # Navigation (Feature 6)

    nav_frame = ttk.Frame(frame)

    nav_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    

    app.btn_prev_step_4 = ttk.Button(nav_frame, text="Pasul 2: Randare", 

                                     command=lambda: app.notebook.select(1))

    app.btn_prev_step_4.pack(side='left', padx=5)

    

    app.btn_next_step_4 = ttk.Button(nav_frame, text="Finalizare - Mergi la Generare", 

                                     command=lambda: app.notebook.select(1))

    app.btn_next_step_4.pack(side='right', padx=5)



def refresh_excel_viewer_content(app):

    if not hasattr(app, 'global_excel_df') or app.global_excel_df is None:

        return

    df = app.global_excel_df

    for child in app.excel_columns_inner.winfo_children():

        child.destroy()

    app.excel_visible_vars = {}

    row, col = 0, 0

    for c_name in df.columns:

        var = tk.BooleanVar(value=True)

        app.excel_visible_vars[c_name] = var

        cb = ttk.Checkbutton(app.excel_columns_inner, text=c_name, variable=var, 

                             command=lambda: update_tree_columns(app))

        cb.grid(row=row, column=col, sticky='w', padx=5)

        col += 1

        if col > 4:

            row += 1

            col = 0

    update_tree_columns(app)



def update_tree_columns(app):

    if not hasattr(app, 'global_excel_df') or app.global_excel_df is None:

        return

    df = app.global_excel_df

    tree = app.excel_tree

    visible_cols = [c for c, var in app.excel_visible_vars.items() if var.get()]

    for item in tree.get_children():

        tree.delete(item)

    tree['columns'] = visible_cols

    for col in visible_cols:

        tree.heading(col, text=col)

        tree.column(col, width=120, minwidth=50)



    search_term = app.excel_search_var.get().lower() if hasattr(app, 'excel_search_var') else ""

    

    # Filtrăm datele dacă există un termen de căutare

    if search_term:

        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

    else:

        filtered_df = df



    for idx, row in filtered_df.head(200).iterrows():

        values = [str(row[c]) if pd.notna(row[c]) else "" for c in visible_cols]

        tree.insert('', 'end', values=values, iid=str(idx))



def on_excel_row_select(app):

    pass



def load_word_template_split(app):

    file_path = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])

    if not file_path:

        return

    app.split_word_label.configure(text=Path(file_path).name, foreground="black")

    try:

        doc = Document(file_path)

        full_text = [para.text for para in doc.paragraphs]

        app.split_word_text.configure(state='normal')

        app.split_word_text.delete('1.0', tk.END)

        app.split_word_text.insert('1.0', "\n".join(full_text))

        content = app.split_word_text.get('1.0', tk.END)

        for pattern in [r'\{\{.*?\}\}', r'«.*?»']:

            for match in re.finditer(pattern, content):

                start = app.split_word_text.index(f"1.0 + {match.start()} c")

                end = app.split_word_text.index(f"1.0 + {match.end()} c")

                app.split_word_text.tag_add("placeholder", start, end)

        app.split_word_text.configure(state='disabled')

    except Exception as e:

        messagebox.showerror("Eroare", f"Nu s-a putut încărca Word: {e}")



def on_split_placeholder_click(app, event):

    index = app.split_word_text.index(f"@{event.x},{event.y}")

    tags = app.split_word_text.tag_names(index)

    if "placeholder" in tags:

        ranges = app.split_word_text.tag_ranges("placeholder")

        clicked = ""

        for i in range(0, len(ranges), 2):

            if app.split_word_text.compare(ranges[i], "<=", index) and app.split_word_text.compare(index, "<=", ranges[i+1]):

                clicked = app.split_word_text.get(ranges[i], ranges[i+1])

                app.split_word_text.tag_remove("active_placeholder", "1.0", tk.END)

                app.split_word_text.tag_add("active_placeholder", ranges[i], ranges[i+1])

                break

        clean = clicked.strip("{}«»").strip()

        selected = app.excel_tree.selection()

        if not selected:

            app.split_info_var.set(f"Placeholder: {clicked}. SELECTAțI UN RÂND ÎN STÂNGA!")

            return

        row_idx = int(selected[0])

        if hasattr(app, 'global_excel_df') and app.global_excel_df is not None:

            df = app.global_excel_df

            found_col = next((col for col in df.columns if clean.lower() == col.lower() or clean.lower() in col.lower()), None)

            if found_col:

                val = df.iloc[row_idx][found_col]

                app.split_info_var.set(f"'{clicked}' -> Coloana: '{found_col}'\nValoare rând curent: {val}")

            else:

                app.split_info_var.set(f"'{clicked}' -> Coloana '{clean}' NU a fost găsită!")

