# tabs/forms_tab.py

import tkinter as tk

from tkinter import ttk, filedialog, messagebox

from ui_utils import ScrollableFrame

from docx import Document



def setup_forms_tab(app, parent):

    frame = parent



    tk.Label(frame, text="GENERATOR IMPORT MICROSOFT FORMS", font=("Impact", 14),

             bg="white", fg="#002B7F").pack(pady=(0,10))

    tk.Label(frame, text="Selectează coloanele din Excel care vor deveni întrebări în formular.",

             bg="white", font=("Arial", 10), fg="#555").pack(pady=(0,20))



    grp_cols = tk.LabelFrame(frame, text="Selectează Întrebările (Coloane Excel)",

                              font=("Arial", 10, "bold"), bg="white")

    grp_cols.pack(fill="both", expand=True, pady=5)



    # Toolbar

    tools = tk.Frame(grp_cols, bg="white")

    tools.pack(fill="x", padx=5, pady=5)

    tk.Button(tools, text="Toate", command=lambda: app.toggle_forms_cols(True), bg="#e0e0e0").pack(side="left", padx=2)

    tk.Button(tools, text="Nimic", command=lambda: app.toggle_forms_cols(False), bg="#e0e0e0").pack(side="left", padx=2)



    app.forms_scroll = ScrollableFrame(grp_cols)

    app.forms_scroll.pack(fill="both", expand=True, padx=5, pady=5)

    app.forms_vars = {}



    tk.Button(frame, text="GENEREAZĂ FIȘIER IMPORT (.DOCX)", bg="#4CAF50", fg="white",

              font=("Arial", 12, "bold"), height=2, command=app.genereaza_fisier_forms).pack(fill="x", pady=20)

