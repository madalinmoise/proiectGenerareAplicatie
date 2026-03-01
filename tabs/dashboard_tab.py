# tabs/dashboard_tab.py

import tkinter as tk

from tkinter import ttk

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def setup_dashboard_tab(app, parent):

    frame = parent



    # Stats frame

    stats_frame = tk.Frame(frame, bg="#f5f5f5", bd=1, relief="solid")

    stats_frame.pack(fill="x", pady=(0, 10))



    app.lbl_stat_rows = tk.Label(stats_frame, text="Total Rânduri: 0", font=("Arial", 12, "bold"),

                                  bg="#f5f5f5", fg="#333", width=20, pady=10)

    app.lbl_stat_rows.pack(side="left", padx=10)



    app.lbl_stat_cols = tk.Label(stats_frame, text="Coloane: 0", font=("Arial", 12, "bold"),

                                  bg="#f5f5f5", fg="#333", width=20, pady=10)

    app.lbl_stat_cols.pack(side="left", padx=10)



    app.lbl_stat_empty = tk.Label(stats_frame, text="Celule Goale: -", font=("Arial", 12, "bold"),

                                   bg="#f5f5f5", fg="#d32f2f", width=20, pady=10)

    app.lbl_stat_empty.pack(side="left", padx=10)



    # Chart canvas

    app.dashboard_chart_frame = tk.Frame(frame, bg="white")

    app.dashboard_chart_frame.pack(fill="both", expand=True)



    # Buton refresh

    ttk.Button(frame, text="Reîmprospătează Dashboard", command=app.refresh_dashboard).pack(pady=5)

