# tabs/manual_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext, filedialog, simpledialog, messagebox



def setup_manual_tab(app, parent):

    frame = parent



    header = tk.Frame(frame, bg="#002B7F", height=60)

    header.pack(fill="x", pady=(0,10))

    header.pack_propagate(False)

    tk.Label(header, text="MANUAL OPERATOR - V6.0 PROFESSIONAL",

             font=("Arial", 16, "bold"), bg="#002B7F", fg="white").pack(pady=15)



    text_frame = tk.Frame(frame)

    text_frame.pack(fill="both", expand=True)



    scrollbar = tk.Scrollbar(text_frame)

    scrollbar.pack(side="right", fill="y")



    app.manual_text = tk.Text(text_frame, wrap="word", font=("Consolas", 9),

                               yscrollcommand=scrollbar.set, bg="#f9f9f9",

                               padx=10, pady=10)

    app.manual_text.pack(side="left", fill="both", expand=True)

    scrollbar.configure(command=app.manual_text.yview)



    # Încărcăm conținutul manualului (preluat din main8.py)

    manual_content = """... (conținutul manualului) ..."""

    app.manual_text.insert("1.0", manual_content)

    app.manual_text.configure(state="disabled")



    # Butoane

    btn_frame = tk.Frame(frame, bg="white")

    btn_frame.pack(fill="x", pady=(10,0))

    tk.Button(btn_frame, text="Salvează Manual ca PDF", command=app.export_manual_pdf,

              bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Salvează Manual ca TXT", command=app.export_manual_txt,

              bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Căutare în Manual", command=app.search_in_manual,

              bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

