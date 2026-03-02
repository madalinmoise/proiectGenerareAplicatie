# tabs/email_tab.py

import tkinter as tk

from tkinter import ttk, scrolledtext

from ui_utils import add_tooltip



def setup_email_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(4, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # General Options

    opts_frame = ttk.LabelFrame(frame, text="Setări Expediere Email")

    opts_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    

    app.email_config['enabled'] = tk.BooleanVar(value=app.email_config['enabled'].get() if 'enabled' in app.email_config else False)

    ttk.Checkbutton(opts_frame, text="Activează trimitere email după generare", variable=app.email_config['enabled']).grid(row=0, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    

    # Noua opțiune "Fără Autentificare"

    app.email_no_auth = tk.BooleanVar(value=False)

    ttk.Checkbutton(opts_frame, text="Fără autentificare (ex: Server Relay local)", variable=app.email_no_auth).grid(row=0, column=2, columnspan=2, sticky='w', padx=5, pady=5)



    # Server SMTP Settings

    server_frame = ttk.LabelFrame(frame, text="Server SMTP")

    server_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    

    ttk.Label(server_frame, text="Server SMTP:").grid(row=0, column=0, sticky='w', padx=5)

    ttk.Entry(server_frame, textvariable=app.email_config['smtp_server'], width=30).grid(row=0, column=1, padx=5, pady=2)

    

    ttk.Label(server_frame, text="Port:").grid(row=0, column=2, sticky='w', padx=5)

    ttk.Combobox(server_frame, textvariable=app.email_config['smtp_port'], values=[587, 465, 25], width=10).grid(row=0, column=3, sticky='w', padx=5, pady=2)

    

    ttk.Label(server_frame, text="Utilizator:").grid(row=1, column=0, sticky='w', padx=5)

    ttk.Entry(server_frame, textvariable=app.email_config['username'], width=30).grid(row=1, column=1, padx=5, pady=2)

    

    ttk.Label(server_frame, text="Parolă:").grid(row=1, column=2, sticky='w', padx=5)

    ttk.Entry(server_frame, textvariable=app.email_config['password'], show='*', width=30).grid(row=1, column=3, padx=5, pady=2)

    

    ttk.Label(server_frame, text="Expeditor (De la):").grid(row=2, column=0, sticky='w', padx=5)

    ttk.Entry(server_frame, textvariable=app.email_config['from'], width=30).grid(row=2, column=1, padx=5, pady=2)



    # Destinatar și Subiect Settings

    target_frame = ttk.LabelFrame(frame, text="Destinatar & Conținut")

    target_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    

    ttk.Label(target_frame, text="Destinatar (Către):").grid(row=0, column=0, sticky='w', padx=5)

    ttk.Entry(target_frame, textvariable=app.email_config['to'], width=30).grid(row=0, column=1, padx=5, pady=2)

    add_tooltip(target_frame.grid_slaves(row=0, column=1)[0], "Adresa manuală de email către care se trimit fișierele.")



    ttk.Label(target_frame, text="SAU Coloană Excel Destinatar:").grid(row=1, column=0, sticky='w', padx=5)

    

    # ComboBox pentru coloana email, se va popula când Excel e încărcat global

    app.email_column_combo = ttk.Combobox(target_frame, textvariable=app.email_column, state='readonly', width=27)

    app.email_column_combo.grid(row=1, column=1, padx=5, pady=2)

    add_tooltip(app.email_column_combo, "Tragerea dinamica a email-ului fiecarui rând. Alege '(Niciunul)' pentru a folosi Destinatarul manual de mai sus.")



    ttk.Label(target_frame, text="Subiect (ex: Documente {nume}):").grid(row=2, column=0, sticky='w', padx=5)

    ttk.Entry(target_frame, textvariable=app.email_subject_pattern, width=30).grid(row=2, column=1, padx=5, pady=2)

    

    ttk.Label(target_frame, text="Corp mesaj:").grid(row=3, column=0, sticky='nw', padx=5)

    app.email_body_text = scrolledtext.ScrolledText(target_frame, height=6, width=50)

    app.email_body_text.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='w')

    app.email_body_text.insert('1.0', app.email_config['body'].get())

    

    def update_email_body(e=None):

        app.email_config['body'].set(app.email_body_text.get('1.0', 'end-1c'))

    app.email_body_text.bind('<KeyRelease>', update_email_body)



    # Mod expediere

    mode_frame = ttk.LabelFrame(frame, text="Mod expediere fișiere")

    mode_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)

    

    # app.email_send_mode is pre-initialized in app.__init__

    ttk.Radiobutton(mode_frame, text="Trimite fiecare document individual", variable=app.email_send_mode, value='individual').pack(anchor='w', padx=5, pady=2)

    ttk.Radiobutton(mode_frame, text="Trimite toate documentele generate pentru un rând într-un singur mail ZIP", variable=app.email_send_mode, value='row_zip').pack(anchor='w', padx=5, pady=2)

    ttk.Radiobutton(mode_frame, text="Trimite toate documentele generate o singură dată (Arhivă ZIP generală)", variable=app.email_send_mode, value='all_zip').pack(anchor='w', padx=5, pady=2)

