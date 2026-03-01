# tabs/stats_tab.py

import tkinter as tk

import customtkinter as ctk

from tkinter import scrolledtext



def setup_stats_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(1, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    header = ctk.CTkLabel(frame, text="Analiză Date & Statistici", font=("Inter", 18, "bold"))

    header.pack(pady=10)



    # Scrolled text wrapper

    app.stats_text = scrolledtext.ScrolledText(frame, height=20, font=('Consolas', 11), 

                                              bg="#1e293b",

                                              fg="white",

                                              padx=10, pady=10)

    app.stats_text.pack(fill='both', expand=True, padx=20, pady=10)

    

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")

    btn_frame.pack(fill='x', padx=20, pady=5)

    

    ctk.CTkButton(btn_frame, text="Actualizează Statistici", width=200, command=app.update_stats).pack(side='left', padx=5)

    

    app.update_stats()

