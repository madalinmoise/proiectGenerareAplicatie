import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext

def setup_stats_tab(app, parent):
    frame = parent
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Enterprise Header
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    ctk.CTkLabel(header_frame, text="📊 Raport Analitic Detaliat",
                 font=("Inter", 22, "bold")).pack(side="left")

    ctk.CTkButton(header_frame, text="🔄 Actualizează Analiza", width=180,
                  command=app.update_stats).pack(side="right", padx=10)

    # Scrolled text wrapper with modern slate look
    app.stats_text = scrolledtext.ScrolledText(frame, height=20, font=('Consolas', 11),
                                              bg="#0f172a", # Slate 900
                                              fg="#f8fafc", # Slate 50
                                              insertbackground="white",
                                              padx=20, pady=20,
                                              borderwidth=0)
    app.stats_text.pack(fill='both', expand=True, padx=20, pady=10)

    # Quick Info Bar
    info_bar = ctk.CTkFrame(frame, height=40, fg_color=("#e2e8f0", "#1e293b"))
    info_bar.pack(fill="x", padx=20, pady=(0, 20))

    ctk.CTkLabel(info_bar, text="💡 Sfat: Folosește Centrul de Raportare pentru reprezentări grafice.",
                 font=("Inter", 12, "italic")).pack(pady=5)

    app.update_stats()
