# tabs/split_view_tab.py

import tkinter as tk

from tkinter import ttk, messagebox, filedialog

from pathlib import Path

import pandas as pd

import re

from docx import Document

from ui_utils import add_tooltip



def setup_split_view_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(0, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # Paned Window for side-by-side view

    paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)

    paned.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)



    # Left Side: Word Preview

    word_frame = ttk.LabelFrame(paned, text="Previzualizare Șablon Word")

    paned.add(word_frame, weight=1)



    word_toolbar = ttk.Frame(word_frame)

    word_toolbar.pack(fill='x', padx=5, pady=5)

    

    ttk.Button(word_toolbar, text="Încarcă Șablon", command=lambda: load_word_template(app)).pack(side='left', padx=5)

    app.split_word_label = ttk.Label(word_toolbar, text="Niciun fișier selectat", foreground="gray")

    app.split_word_label.pack(side='left', padx=5)



    app.split_word_text = tk.Text(word_frame, wrap='word', state='disabled', font=("Segoe UI", 10))

    app.split_word_text.pack(fill='both', expand=True, padx=5, pady=5)

    

    # Scrollbar for Word text

    word_scroll = ttk.Scrollbar(app.split_word_text, orient=tk.VERTICAL, command=app.split_word_text.yview)

    word_scroll.pack(side='right', fill='y')

    app.split_word_text.configure(yscrollcommand=word_scroll.set)



    # Right Side: Excel Data

    excel_frame = ttk.LabelFrame(paned, text="Date Excel (Global)")

    paned.add(excel_frame, weight=1)



    excel_toolbar = ttk.Frame(excel_frame)

    excel_toolbar.pack(fill='x', padx=5, pady=5)

    

    ttk.Label(excel_toolbar, text="Căutare coloană:").pack(side='left', padx=5)

    app.split_excel_search = tk.StringVar()

    ttk.Entry(excel_toolbar, textvariable=app.split_excel_search, width=20).pack(side='left', padx=5)

    ttk.Button(excel_toolbar, text="Găsește coloana", command=lambda: highlight_excel_column(app)).pack(side='left', padx=2)

    

    # Info panel for placeholder details

    app.split_info_var = tk.StringVar(value="Faceși clic pe un placeholder din stânga pentru a vedea datele.")

    info_lbl = ttk.Label(excel_frame, textvariable=app.split_info_var, wraplength=400, foreground="blue", font=("Segoe UI", 9, "bold"))

    info_lbl.pack(fill='x', padx=10, pady=5)



    # Treeview for Excel data

    tree_container = ttk.Frame(excel_frame)

    tree_container.pack(fill='both', expand=True, padx=5, pady=5)

    tree_container.grid_rowconfigure(0, weight=1)

    tree_container.grid_columnconfigure(0, weight=1)



    app.split_excel_tree = ttk.Treeview(tree_container, show='headings')

    app.split_excel_tree.grid(row=0, column=0, sticky='nsew')

    

    x_scroll = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=app.split_excel_tree.xview)

    x_scroll.grid(row=1, column=0, sticky='ew')

    y_scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=app.split_excel_tree.yview)

    y_scroll.grid(row=0, column=1, sticky='ns')

    app.split_excel_tree.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)



    # Tag configuration for highlighting

    app.split_word_text.tag_config("placeholder", foreground="red", font=("Segoe UI", 10, "bold"), underline=True)

    app.split_word_text.tag_config("active_placeholder", background="yellow", foreground="red", font=("Segoe UI", 10, "bold"))

    

    # Bindings

    app.split_word_text.tag_bind("placeholder", "<Button-1>", lambda e: on_placeholder_click(app, e))

    app.split_excel_search.trace_add("write", lambda *args: highlight_excel_column(app))



def load_word_template(app):

    file_path = filedialog.askopenfilename(filetypes=[("Word documents", "*.docx")])

    if not file_path:

        return

    

    app.split_word_label.configure(text=Path(file_path).name, foreground="black")

    try:

        doc = Document(file_path)

        full_text = []

        for para in doc.paragraphs:

            full_text.append(para.text)

        

        app.split_word_text.configure(state='normal')

        app.split_word_text.delete('1.0', tk.END)

        app.split_word_text.insert('1.0', "\n".join(full_text))

        

        # Highlight placeholders

        content = app.split_word_text.get('1.0', tk.END)

        # Search for {{...}} or «...»

        patterns = [r'\{\{.*?\}\}', r'«.*?»']

        for pattern in patterns:

            for match in re.finditer(pattern, content):

                start_idx = app.split_word_text.index(f"1.0 + {match.start()} c")

                end_idx = app.split_word_text.index(f"1.0 + {match.end()} c")

                app.split_word_text.tag_add("placeholder", start_idx, end_idx)

        

        app.split_word_text.configure(state='disabled')

    except Exception as e:

        messagebox.showerror("Eroare", f"Nu s-a putut încărca fișierul Word: {e}")



def refresh_split_excel_view(app):

    """Refreshes the Excel tree in Split View using global_excel_df."""

    if not hasattr(app, 'global_excel_df') or app.global_excel_df is None:

        return

    

    df = app.global_excel_df

    tree = app.split_excel_tree

    

    # Clear tree

    for item in tree.get_children():

        tree.delete(item)

    

    # Set columns

    cols = list(df.columns)

    tree['columns'] = cols

    for col in cols:

        tree.heading(col, text=col)

        tree.column(col, width=100, minwidth=50)

    

    # Insert data (limit to first 100 rows for preview performance)

    preview_df = df.head(100)

    for idx, row in preview_df.iterrows():

        values = [str(v) if pd.notna(v) else "" for v in row]

        tree.insert('', 'end', values=values)



def on_placeholder_click(app, event):

    # Find which placeholder was clicked

    index = app.split_word_text.index(f"@{event.x},{event.y}")

    tags = app.split_word_text.tag_names(index)

    

    if "placeholder" in tags:

        # Get the range of the tag

        ranges = app.split_word_text.tag_ranges("placeholder")

        clicked_placeholder = ""

        for i in range(0, len(ranges), 2):

            if app.split_word_text.compare(ranges[i], "<=", index) and app.split_word_text.compare(index, "<=", ranges[i+1]):

                clicked_placeholder = app.split_word_text.get(ranges[i], ranges[i+1])

                # Highlight as active

                app.split_word_text.tag_remove("active_placeholder", "1.0", tk.END)

                app.split_word_text.tag_add("active_placeholder", ranges[i], ranges[i+1])

                break

        

        # Clean placeholder name

        clean_name = clicked_placeholder.strip("{}«»")

        app.split_info_var.set(f"Placeholder selectat: {clicked_placeholder} -> Caut coloana: '{clean_name}'")

        

        # Search in Excel columns

        if hasattr(app, 'global_excel_df') and app.global_excel_df is not None:

            cols = list(app.global_excel_df.columns)

            found = False

            for i, col in enumerate(cols):

                if clean_name.lower() in col.lower():

                    # Scroll tree to this column

                    app.split_excel_tree.see(app.split_excel_tree.get_children()[0]) # Reset view

                    # Actually treeview doesn't have a direct "see column", so we use horizontal scroll if possible

                    # But we can at least show it in search

                    app.split_excel_search.set(col)

                    app.split_info_var.set(f"Placeholder: {clicked_placeholder} -> Mapat la coloana Excel: '{col}'")

                    found = True

                    break

            if not found:

                app.split_info_var.set(f"Placeholder: {clicked_placeholder} -> NU s-a găsit coloană corespunzătoare în Excel.")



def highlight_excel_column(app):

    search_term = app.split_excel_search.get().strip().lower()

    if not search_term or not hasattr(app, 'global_excel_df') or app.global_excel_df is None:

        return

    

    cols = list(app.global_excel_df.columns)

    for i, col in enumerate(cols):

        if search_term in col.lower():

            # Scroll treeview horizontally to the column (not easy with standard ttk.Treeview)

            # We will at least update the label

            pass

