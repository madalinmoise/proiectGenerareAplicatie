# tabs/reports_tab.py

import tkinter as tk

from tkinter import ttk

from ui_utils import add_tooltip



def setup_reports_tab(app, parent):

    frame = parent

    frame.grid_rowconfigure(3, weight=1)

    frame.grid_columnconfigure(0, weight=1)



    # Frame pentru filtre (sus)

    filter_frame = ttk.LabelFrame(frame, text="Filtre")

    filter_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

    filter_frame.grid_columnconfigure(0, weight=1)



    # Aici vom adăuga controale pentru filtre (deocamdată placeholder)

    ttk.Label(filter_frame, text="(Filtrele vor fi implementate în versiunea următoare)").pack(padx=5, pady=5)



    # Frame pentru selecție coloane și tip grafic

    custom_frame = ttk.LabelFrame(frame, text="Raport personalizat")

    custom_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    custom_frame.grid_columnconfigure(1, weight=1)



    ttk.Label(custom_frame, text="Coloana X:").grid(row=0, column=0, sticky='w', padx=5)

    app.custom_x_col = tk.StringVar()

    app.custom_x_combo = ttk.Combobox(custom_frame, textvariable=app.custom_x_col, state='readonly', width=30)

    app.custom_x_combo.grid(row=0, column=1, padx=5, sticky='ew')



    ttk.Label(custom_frame, text="Coloana Y (opșional):").grid(row=1, column=0, sticky='w', padx=5)

    app.custom_y_col = tk.StringVar()

    app.custom_y_combo = ttk.Combobox(custom_frame, textvariable=app.custom_y_col, state='readonly', width=30)

    app.custom_y_combo.grid(row=1, column=1, padx=5, sticky='ew')



    ttk.Label(custom_frame, text="Tip grafic:").grid(row=2, column=0, sticky='w', padx=5)

    app.custom_chart_type = tk.StringVar(value='bar')

    chart_combo = ttk.Combobox(custom_frame, textvariable=app.custom_chart_type,

                                values=['bar', 'pie', 'line', 'scatter'], state='readonly', width=15)

    chart_combo.grid(row=2, column=1, padx=5, sticky='w')



    btn_custom = ttk.Button(custom_frame, text="Generează", command=app.generate_custom_chart)

    btn_custom.grid(row=3, column=0, columnspan=2, pady=5)



    # Butoane pentru statistici predefinite

    stats_frame = ttk.LabelFrame(frame, text="Statistici predefinite")

    stats_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    

    # Folosim un grid interior pentru butoane

    for i in range(4): stats_frame.grid_columnconfigure(i, weight=1)



    btn_post = ttk.Button(stats_frame, text="Categorii post", command=app.stats_post_categories)

    btn_post.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_post, "Numărul de persoane pe categorii de post")



    btn_dept = ttk.Button(stats_frame, text="Departamente", command=app.stats_departments)

    btn_dept.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_dept, "Distribușia pe departamente")



    btn_edu = ttk.Button(stats_frame, text="Nivel educație", command=app.stats_education_level)

    btn_edu.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_edu, "Nivelul de educație (licenșă/master/doctorat)")



    btn_act = ttk.Button(stats_frame, text="Activităși", command=app.stats_activities)

    btn_act.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_act, "Repartizarea pe activităși")



    btn_id = ttk.Button(stats_frame, text="Tip act identitate", command=app.stats_id_types)

    btn_id.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_id, "Statistici privind tipul actului de identitate")



    btn_gender = ttk.Button(stats_frame, text="Distribuție Gen", command=app.stats_gender)

    btn_gender.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_gender, "Distribușia pe gen (Feminim/Masculin)")



    btn_age = ttk.Button(stats_frame, text="Grupe Vârstă", command=app.stats_age_groups)

    btn_age.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_age, "Statistici pe grupe de vârstă")



    btn_usage = ttk.Button(stats_frame, text="Utilizare Șabloane", command=app.stats_template_usage)

    btn_usage.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_usage, "Top cele mai utilizate șabloane (din audit)")



    btn_skills = ttk.Button(stats_frame, text="Matrice competenșe", command=app.skills_matrix)

    btn_skills.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='ew')

    add_tooltip(btn_skills, "Top competenșe menșionate în documente")



    # Buton export date filtrate

    export_btn = ttk.Button(frame, text="Exportă date filtrate", command=app.export_filtered_data)

    export_btn.grid(row=4, column=0, pady=5)



    # Canvas pentru afișarea graficelor

    app.report_canvas_frame = ttk.Frame(frame)

    app.report_canvas_frame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)

    app.report_canvas_frame.grid_rowconfigure(0, weight=1)

    app.report_canvas_frame.grid_columnconfigure(0, weight=1)

