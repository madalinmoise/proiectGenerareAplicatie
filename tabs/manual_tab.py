import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog, messagebox

def setup_manual_tab(app, parent):
    frame = parent

    header = tk.Frame(frame, bg="#002B7F", height=60)
    header.pack(fill="x", pady=(0,10))
    header.pack_propagate(False)
    tk.Label(header, text="MANUAL OPERATOR - V6.1 ENTERPRISE",
             font=("Arial", 16, "bold"), bg="#002B7F", fg="white").pack(pady=15)

    text_frame = tk.Frame(frame)
    text_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    app.manual_text = tk.Text(text_frame, wrap="word", font=("Consolas", 10),
                               yscrollcommand=scrollbar.set, bg="#fdfdfd",
                               padx=15, pady=15)
    app.manual_text.pack(side="left", fill="both", expand=True)
    scrollbar.configure(command=app.manual_text.yview)

    # Build manual content from AI Guide Knowledge Base
    manual_content = "=== MANUAL COMPLET DE UTILIZARE ENTERPRISE ===\n\n"
    if hasattr(app, 'local_guide'):
        kb = app.local_guide.knowledge_base
        for key, value in kb.items():
            manual_content += f"--- SECȚIUNEA: {key.upper()} ---\n"
            manual_content += value + "\n\n"

        # Add special enterprise section
        manual_content += "--- SECȚIUNEA: NOUTĂȚI ENTERPRISE ---\n"
        manual_content += "Aplicația include acum analize automate pentru:\n"
        manual_content += "1. Academic: Identificare automată Studenți, Masteranzi, Doctoranzi.\n"
        manual_content += "2. Cercetare: Distribuție pe grade (CSI, CSII, etc.).\n"
        manual_content += "3. Integritate: Audit pentru celule goale și cereri de asistență.\n"
    else:
        manual_content += "Informație manual momentan indisponibilă."

    app.manual_text.insert("1.0", manual_content)
    app.manual_text.configure(state="disabled")

    # Butoane
    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(fill="x", pady=(10,0))

    tk.Button(btn_frame, text="Salvează Manual ca PDF", command=app.export_manual_pdf,
              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Salvează Manual ca TXT", command=app.export_manual_txt,
              bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Căutare în Manual", command=app.search_in_manual,
              bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=10).pack(side="left", padx=5)
