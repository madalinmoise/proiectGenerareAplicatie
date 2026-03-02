# tabs/settings_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext

from ui_utils import add_tooltip

from config import config



def setup_settings_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(4, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # Notebook în setări

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

    ttk.Button(btn_frame, text="Începe înregistrare macro", command=app.start_recording).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="Oprește înregistrare macro", command=app.stop_recording).pack(side='left', padx=5)



    # Modele Rapide de Scripturi

    templates_frame = ttk.LabelFrame(script_frame, text="Funcșii predefinite rapide")

    templates_frame.pack(fill='x', padx=5, pady=5)

    

    app.script_template_var = tk.StringVar()

    script_combo = ttk.Combobox(templates_frame, textvariable=app.script_template_var, state='readonly', width=50)

    script_combo['values'] = [

        "Nume la majuscule (Uppercase)",

        "Titlecase pentru 'Nume' și 'Prenume'",

        "Elimină spașiile libere (Strip)",

        "Formatare Dată (YYYY-MM-DD)",

        "Convert ; la linie noua", "Șablon gol (def process_row)"

    ]

    script_combo.pack(side='left', padx=5, pady=5)

    

    def apply_script_template(*args):

        choice = app.script_template_var.get()

        app.script_text.delete('1.0', tk.END)

        if choice == "Convert ; la linie noua":
            code = (
                "def process_row(row):\n"
                "    for key in row:\n"
                "        if isinstance(row[key], str) and row[key].endswith(';'):\n"
                "            row[key] = row[key] + '\n'\n"
                "    return row\n"
            )
        elif choice == "Nume la majuscule (Uppercase)":

            code = (

                "def process_row(row):\n"

                "    if 'Nume' in row:\n"

                "        row['Nume'] = str(row['Nume']).upper()\n"

                "    return row\n"

            )

        elif choice == "Convert ; la linie noua":
            code = (
                "def process_row(row):\n"
                "    for key in row:\n"
                "        if isinstance(row[key], str) and row[key].endswith(';'):\n"
                "            row[key] = row[key] + '\n'\n"
                "    return row\n"
            )
        elif choice == "Titlecase pentru 'Nume' și 'Prenume'":

            code = (

                "def process_row(row):\n"

                "    for col in ['Nume', 'Prenume']:\n"

                "        if col in row:\n"

                "            row[col] = str(row[col]).title()\n"

                "    return row\n"

            )

        elif choice == "Convert ; la linie noua":
            code = (
                "def process_row(row):\n"
                "    for key in row:\n"
                "        if isinstance(row[key], str) and row[key].endswith(';'):\n"
                "            row[key] = row[key] + '\n'\n"
                "    return row\n"
            )
        elif choice == "Elimină spașiile libere (Strip)":

            code = (

                "def process_row(row):\n"

                "    for key in row:\n"

                "        if isinstance(row[key], str):\n"

                "            row[key] = row[key].strip()\n"

                "    return row\n"

            )

        elif choice == "Convert ; la linie noua":
            code = (
                "def process_row(row):\n"
                "    for key in row:\n"
                "        if isinstance(row[key], str) and row[key].endswith(';'):\n"
                "            row[key] = row[key] + '\n'\n"
                "    return row\n"
            )
        elif choice == "Formatare Dată (YYYY-MM-DD)":

            code = (

                "import datetime\n"

                "def process_row(row):\n"

                "    for key in row:\n"

                "        if 'data' in key.lower() or 'date' in key.lower():\n"

                "            try:\n"

                "                val = row[key]\n"

                "                if hasattr(val, 'strftime'):\n"

                "                    row[key] = val.strftime('%Y-%m-%d')\n"

                "            except:\n"

                "                pass\n"

                "    return row\n"

            )

        else: # Șablon gol

            code = (

                "def process_row(row):\n"

                "    # Scrie codul tau aici\n"

                "    return row\n"

            )

        app.script_text.insert('1.0', code)

        

    ttk.Button(templates_frame, text="Incarcă model", command=apply_script_template).pack(side='left', padx=5)



    # Touch mode

    touch_frame = ttk.Frame(settings_notebook)

    settings_notebook.add(touch_frame, text="Interfașă")

    ttk.Checkbutton(touch_frame, text="Mod touch-friendly (butoane mai mari)", variable=app.touch_mode, command=app.apply_touch_mode).pack(anchor='w', padx=5, pady=5)

    ttk.Label(touch_frame, text="Temă:").pack(anchor='w', padx=5)

    ttk.Radiobutton(touch_frame, text="Deschisă", variable=app.theme, value="light", command=app.apply_theme).pack(anchor='w', padx=20)

    ttk.Radiobutton(touch_frame, text="Închisă", variable=app.theme, value="dark", command=app.apply_theme).pack(anchor='w', padx=20)



    # Advanced

    adv_frame = ttk.Frame(settings_notebook)

    settings_notebook.add(adv_frame, text="Avansat")

    ttk.Button(adv_frame, text="Conectare SharePoint", command=app.connect_sharepoint).pack(anchor='w', padx=5, pady=5)

    ttk.Button(adv_frame, text="Plugin marketplace", command=app.open_plugin_marketplace).pack(anchor='w', padx=5, pady=5)

    ttk.Button(adv_frame, text="Minimizează în system tray", command=app.minimize_to_tray).pack(anchor='w', padx=5, pady=5)



    # Tastă inișială pt script

    app.script_template_var.set("Convert ; la linie noua", "Șablon gol (def process_row)")

    apply_script_template()

