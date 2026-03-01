import requests
import os

url_excel = "http://127.0.0.1:5000/api/wizard/upload-excel"
url_template = "http://127.0.0.1:5000/api/wizard/upload-template"
url_options = "http://127.0.0.1:5000/api/wizard/options"
url_start = "http://127.0.0.1:5000/api/wizard/start"

# 1. Upload Excel
with open("fisier_excel.xlsx", "rb") as f:
    r = requests.post(url_excel, files={"file": f})
    print(f"Excel Upload: {r.json()}")

# 2. Upload Template
template_path = "Modele documente/Anexa 10 Declaratie angajare membru echipa.docx"
with open(template_path, "rb") as f:
    r = requests.post(url_template, files={"files[]": ("Anexa10.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    print(f"Template Upload: {r.json()}")

# 3. Set Options
options = {
    "folder_column": "Nume de familie",
    "output_dir": r"c:\Users\Administrator\Downloads\program expert\out_final_verification",
    "filename_pattern": "{Nume de familie}_{Prenume}_V6",
    "multiprocessing": False
}
r = requests.post(url_options, json=options)
print(f"Options: {r.json()}")

# 4. Start
r = requests.post(url_start)
print(f"Start: {r.json()}")
