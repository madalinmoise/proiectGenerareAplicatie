import tkinter as tk
from tkinter import ttk, scrolledtext
from ui_utils import add_tooltip
from config import config

def setup_settings_tab(app, parent):
    frame = parent
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Notebook in settings
    settings_notebook = ttk.Notebook(frame)
    settings_notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    # Scripting
    script_frame = ttk.Frame(settings_notebook)
    settings_notebook.add(script_frame, text="Scripting")
    ttk.Label(script_frame, text="Scripturi personalizate (Python):").pack(anchor='w', padx=5, pady=5)
    app.script_text = scrolledtext.ScrolledText(script_frame, height=15)
    app.script_text.pack(fill='both', expand=True, padx=5, pady=5)

    btn_frame = ttk.Frame(script_frame)
    btn_frame.pack(fill='x', padx=5, pady=5)
    ttk.Button(btn_frame, text="Salvează script", command=app.save_script).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Încarcă script", command=app.load_script).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Resetează Scripturi", command=lambda: setattr(app, 'scripts', [])).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Începe înregistrare macro", command=app.start_recording).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Oprește înregistrare macro", command=app.stop_recording).pack(side='left', padx=5)

    # Quick Script Templates
    templates_frame = ttk.LabelFrame(script_frame, text="Funcții predefinite rapide")
    templates_frame.pack(fill='x', padx=5, pady=5)

    app.script_template_var = tk.StringVar()
    script_combo = ttk.Combobox(templates_frame, textvariable=app.script_template_var, state='readonly', width=50)
    script_combo['values'] = [
        "Nume la majuscule (Uppercase)",
        "Titlecase pentru 'Nume' și 'Prenume'",
        "Elimină spațiile libere (Strip)",
        "Formatare Dată (YYYY-MM-DD)",
        "Convert ; la linie noua",
        "Șablon gol (def process_row)"
    ]
    script_combo.pack(side='left', padx=5, pady=5)

    def apply_script_template(*args):
        choice = app.script_template_var.get()
        app.script_text.delete('1.0', tk.END)

        if choice == "Convert ; la linie noua":
            code = """def process_row(row):
    for key in row:
        if isinstance(row[key], str):
            row[key] = row[key].replace(';', ';\\n')
    return row"""
        elif choice == "Nume la majuscule (Uppercase)":
            code = """def process_row(row):
    if 'Nume' in row:
        row['Nume'] = str(row['Nume']).upper()
    return row"""
        elif choice == "Titlecase pentru 'Nume' și 'Prenume'":
            code = """def process_row(row):
    for col in ['Nume', 'Prenume']:
        if col in row:
            row[col] = str(row[col]).title()
    return row"""
        elif choice == "Elimină spațiile libere (Strip)":
            code = """def process_row(row):
    for key in row:
        if isinstance(row[key], str):
            row[key] = row[key].strip()
    return row"""
        elif choice == "Formatare Dată (YYYY-MM-DD)":
            code = """import datetime
def process_row(row):
    for key in row:
        if 'data' in key.lower() or 'date' in key.lower():
            try:
                val = row[key]
                if hasattr(val, 'strftime'):
                    row[key] = val.strftime('%Y-%m-%d')
            except:
                pass
    return row"""
        else: # Șablon gol
            code = """def process_row(row):
    # Scrie codul tau aici
    return row"""

        app.script_text.insert('1.0', code)

    ttk.Button(templates_frame, text="Incarcă model", command=apply_script_template).pack(side='left', padx=5)

    # Appearance
    touch_frame = ttk.Frame(settings_notebook)
    settings_notebook.add(touch_frame, text="Interfață")
    ttk.Checkbutton(touch_frame, text="Mod touch-friendly", variable=app.touch_mode, command=app.apply_touch_mode).pack(anchor='w', padx=5, pady=5)

    # Theme selection
    theme_frame = ttk.LabelFrame(touch_frame, text="Temă Aplicație")
    theme_frame.pack(fill='x', padx=5, pady=5)
    ttk.Radiobutton(theme_frame, text="Deschisă (Light)", variable=app.theme, value="light", command=app.apply_theme).pack(anchor='w', padx=20, pady=2)
    ttk.Radiobutton(theme_frame, text="Închisă (Dark)", variable=app.theme, value="dark", command=app.apply_theme).pack(anchor='w', padx=20, pady=2)

    # Advanced
    adv_frame = ttk.Frame(settings_notebook)
    settings_notebook.add(adv_frame, text="Avansat")
    ttk.Button(adv_frame, text="Conectare SharePoint", command=app.connect_sharepoint).pack(anchor='w', padx=5, pady=5)
    ttk.Button(adv_frame, text="Plugin marketplace", command=app.open_plugin_marketplace).pack(anchor='w', padx=5, pady=5)
    ttk.Button(adv_frame, text="Minimizează în system tray", command=app.minimize_to_tray).pack(anchor='w', padx=5, pady=5)

    app.script_template_var.set("Șablon gol (def process_row)")
    apply_script_template()
