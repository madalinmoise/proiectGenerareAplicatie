import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

def setup_dashboard_tab(app, parent):
    frame = parent

    # Hero Section
    hero_frame = ctk.CTkFrame(frame, fg_color=("#3b82f6", "#1e3a8a"), corner_radius=15, height=150)
    hero_frame.pack(fill="x", padx=20, pady=20)
    hero_frame.pack_propagate(False)

    ctk.CTkLabel(hero_frame, text="Bun venit în Centrul Documentelor",
                 font=("Inter", 24, "bold"), text_color="white").pack(pady=(30, 5))
    ctk.CTkLabel(hero_frame, text="Automatizare Inteligentă pentru Administrație Enterprise",
                 font=("Inter", 14), text_color="white").pack()

    # Quick Stats Grid
    stats_container = ctk.CTkFrame(frame, fg_color="transparent")
    stats_container.pack(fill="x", padx=20, pady=10)

    for i in range(3): stats_container.grid_columnconfigure(i, weight=1)

    # Card 1: Records
    card1 = ctk.CTkFrame(stats_container, corner_radius=10)
    card1.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
    app.lbl_stat_rows = ctk.CTkLabel(card1, text="Total Rânduri: 0", font=("Inter", 15, "bold"))
    app.lbl_stat_rows.pack(pady=20)

    # Card 2: Features
    card2 = ctk.CTkFrame(stats_container, corner_radius=10)
    card2.grid(row=0, column=1, padx=10, sticky="nsew")
    app.lbl_stat_cols = ctk.CTkLabel(card2, text="Coloane: 0", font=("Inter", 15, "bold"))
    app.lbl_stat_cols.pack(pady=20)

    # Card 3: Integrity
    card3 = ctk.CTkFrame(stats_container, corner_radius=10)
    card3.grid(row=0, column=2, padx=(10, 0), sticky="nsew")
    app.lbl_stat_empty = ctk.CTkLabel(card3, text="Celule Goale: -", font=("Inter", 15, "bold"), text_color="#ef4444")
    app.lbl_stat_empty.pack(pady=20)

    # Main Visual Area
    content_frame = ctk.CTkFrame(frame, corner_radius=15)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(content_frame, text="Vizualizare Distribuție Date", font=("Inter", 16, "bold")).pack(pady=10)

    app.dashboard_chart_frame = tk.Frame(content_frame, bg="white")
    app.dashboard_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Action bar
    action_bar = ctk.CTkFrame(frame, fg_color="transparent")
    action_bar.pack(fill="x", padx=20, pady=(0, 20))

    ctk.CTkButton(action_bar, text="🔄 Actualizează Date", width=200, command=app.refresh_dashboard).pack(side="left")
    ctk.CTkButton(action_bar, text="📋 Vezi Audit", width=200, fg_color="#6b7280", command=lambda: app.notebook.set("Audit Log")).pack(side="right")
