# tabs/ai_guide_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext

from ui_utils import add_tooltip, CreateToolTip



def setup_ai_guide_tab(app, parent):

    frame = parent



    # Header

    header = tk.Frame(frame, bg="#002B7F", height=70)

    header.pack(fill="x", pady=(0, 10))

    header.pack_propagate(False)



    tk.Label(header, text="GHID INTELIGENT LOCAL",

             font=("Arial", 18, "bold"), bg="#002B7F", fg="white").pack(pady=15)



    # Quick action buttons - folosim tk.LabelFrame în loc de ttk.LabelFrame pentru a accepta font

    quick_frame = tk.LabelFrame(frame, text="Acțiuni Rapide",

                                 font=('Arial', 11, 'bold'), bg="white", fg="#01579B")

    quick_frame.pack(fill='x', pady=(0, 10))



    btn_row1 = tk.Frame(quick_frame, bg="white")

    btn_row1.pack(fill='x', pady=2)

    btn_row2 = tk.Frame(quick_frame, bg="white")

    btn_row2.pack(fill='x', pady=2)



    quick_buttons = [

        ("Tutorial Complet", "tutorial", "#4CAF50"),

        ("Creare Template", "cum creez template", "#2196F3"),

        ("Format Excel", "format excel", "#FF9800"),

        ("⚠️ Rezolvare Erori", "erori comune", "#F44336"),

        ("Funcșii Avansate", "functii avansate", "#9C27B0"),

        ("❓ Cum Folosesc", "cum folosesc", "#00BCD4"),

    ]



    for i, (text, cmd, color) in enumerate(quick_buttons):

        parent_row = btn_row1 if i < 3 else btn_row2

        btn = tk.Button(parent_row, text=text,

                        command=lambda c=cmd: app.send_guide_message(c),

                        bg=color, fg="white", font=('Arial', 10, 'bold'),

                        padx=12, pady=8, relief="raised")

        btn.pack(side='left', padx=4, pady=3, expand=True, fill='x')

        tooltips = {

            "tutorial": "Tutorial interactiv pas-cu-pas",

            "cum creez template": "Ghid pentru template-uri Word",

            "format excel": "Cum să formatezi Excel",

            "erori comune": "Solușii pentru probleme",

            "functii avansate": "PDF, Merge, ZIP, Paralel",

            "cum folosesc": "Ghid complet de utilizare"

        }

        CreateToolTip(btn, tooltips.get(cmd, ""))



    # Chat display - folosim tk.LabelFrame

    chat_frame = tk.LabelFrame(frame, text="Conversașie",

                                font=('Arial', 11, 'bold'), bg="white")

    chat_frame.pack(fill='both', expand=True, pady=(0, 10))



    app.guide_text = scrolledtext.ScrolledText(

        chat_frame, wrap=tk.WORD, height=15,

        font=('Consolas', 10), bg="#1a1a1a", fg="#00ff00",

        insertbackground="white", padx=10, pady=10

    )

    app.guide_text.pack(fill='both', expand=True)

    app.guide_text.configure(state='disabled')



    # Configure tags for styling

    app.guide_text.tag_config("user", foreground="#4FC3F7", font=('Consolas', 10, 'bold'))

    app.guide_text.tag_config("guide", foreground="#81C784", font=('Consolas', 10))

    app.guide_text.tag_config("system", foreground="#FFB74D", font=('Consolas', 9, 'italic'))

    app.guide_text.tag_config("important", foreground="#FF6E40", font=('Consolas', 10, 'bold'))



    # Input area

    input_frame = tk.Frame(frame, bg="white")

    input_frame.pack(fill='x', pady=(0, 5))



    tk.Label(input_frame, text="Întrebare:", bg="white", fg="#01579B",

             font=('Arial', 11, 'bold')).pack(side='left', padx=(0, 8))



    app.guide_input = tk.Entry(input_frame, font=('Consolas', 11),

                                bg="#f5f5f5", relief="solid", bd=1)

    app.guide_input.pack(side='left', fill='x', expand=True, padx=(0, 8))

    app.guide_input.bind('<Return>', lambda e: app.send_guide_message())



    app.guide_send_btn = tk.Button(

        input_frame, text="📤 Trimite", command=app.send_guide_message,

        bg="#1976D2", fg="white", font=('Arial', 11, 'bold'),

        padx=20, pady=8, relief="raised", cursor="hand2"

    )

    app.guide_send_btn.pack(side='left', padx=3)



    tk.Button(

        input_frame, text="Șterge", command=app.clear_guide_conversation,

        bg="#D32F2F", fg="white", font=('Arial', 11, 'bold'),

        padx=20, pady=8, relief="raised"

    ).pack(side='left', padx=3)



    # Tutorial status indicator

    app.tutorial_status_frame = tk.Frame(frame, bg="#FFF3E0", relief="solid", bd=1)

    app.tutorial_status_label = tk.Label(

        app.tutorial_status_frame,

        text="", font=("Arial", 10, "bold"),

        bg="#FFF3E0", fg="#E65100"

    )

    app.tutorial_status_label.pack(padx=10, pady=5)

    app.tutorial_status_frame.pack_forget()  # hidden initially



    # Welcome message

    app.add_guide_message("system", "Bine ai venit la Ghidul Inteligent! Scrie 'tutorial' pentru ajutor pas-cu-pas.")

