# scanner_utils.py

import re

import difflib

import traceback

from datetime import datetime

from pathlib import Path

from template_utils import extract_placeholders_from_file

import logging



logger = logging.getLogger('HRAudit')



def normalize_placeholder(name):

    diacritice = {

        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ț': 't',

        'Ă': 'A', 'Â': 'A', 'Î': 'I', 'Ș': 'S', 'Ț': 'T'

    }

    for diac, ascii_char in diacritice.items():

        name = name.replace(diac, ascii_char)

    name = re.sub(r'\s+', '_', name.strip())

    return name



def scan_template_files(file_paths, log_queue=None, progress_callback=None):

    try:

        if not file_paths:

            if log_queue:

                log_queue.put("Nu s-au selectat fișiere.")

            return None



        report_lines = []

        report_lines.append("=" * 60)

        report_lines.append(f"RAPORT SCANARE ȘABLOANE - {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        report_lines.append("=" * 60)



        all_placeholders = {}

        problems = {

            'spaces_inside': [],

            'diacritics': [],

            'too_long': [],

            'similar': []

        }



        for i, file_path in enumerate(file_paths):

            if log_queue:

                log_queue.put(f"Scanez: {Path(file_path).name}")

            logger.info(f"Scanez: {Path(file_path).name}")

            if progress_callback:

                progress_callback(i+1, len(file_paths))

            placeholders = extract_placeholders_from_file(file_path)

            for ph in placeholders:

                if ph not in all_placeholders:

                    all_placeholders[ph] = []

                all_placeholders[ph].append(Path(file_path).name)



        for ph in sorted(all_placeholders.keys()):

            files_list = ", ".join(all_placeholders[ph])

            if ' ' in ph:

                problems['spaces_inside'].append((ph, files_list))

            if re.search(r'[ăâîșțĂÂÎȘȚ]', ph):

                problems['diacritics'].append((ph, files_list))

            if len(ph) > 40:

                problems['too_long'].append((ph, files_list))



        ph_list = list(all_placeholders.keys())

        similar_groups = []

        for i, ph1 in enumerate(ph_list):

            for ph2 in ph_list[i+1:]:

                norm1 = re.sub(r'[_\s]+', '', ph1.lower())

                norm2 = re.sub(r'[_\s]+', '', ph2.lower())

                if norm1 == norm2 and ph1 != ph2:

                    similar_groups.append((ph1, ph2))

                else:

                    similarity = difflib.SequenceMatcher(None, ph1.lower(), ph2.lower()).ratio()

                    if similarity > 0.8:

                        similar_groups.append((ph1, ph2, f"{similarity:.2f}"))



        if similar_groups:

            problems['similar'] = similar_groups



        report_lines.append("\n**Placeholder-uri găsite**")

        for ph in sorted(all_placeholders.keys()):

            report_lines.append(f"  - {ph} (în: {', '.join(all_placeholders[ph])})")



        report_lines.append("\n" + "=" * 60)

        report_lines.append("**PROBLEME IDENTIFICATE**")

        report_lines.append("=" * 60)



        if problems['spaces_inside']:

            report_lines.append("\n❌ Placeholder-uri cu SPAȚII ÎN INTERIOR (trebuie corectate):")

            for ph, files in problems['spaces_inside']:

                report_lines.append(f"  - {ph} (în: {files})")



        if problems['diacritics']:

            report_lines.append("\n⚠Placeholder-uri cu DIACRITICE (recomandat înlocuit):")

            for ph, files in problems['diacritics']:

                report_lines.append(f"  - {ph} (în: {files})")



        if problems['too_long']:

            report_lines.append("\n📏 Placeholder-uri FOARTE LUNGI (>40 caractere):")

            for ph, files in problems['too_long']:

                report_lines.append(f"  - {ph} (în: {files})")



        if problems['similar']:

            report_lines.append("\nPlaceholder-uri SIMILARE (posibil aceeați informație):")

            for group in problems['similar']:

                if len(group) == 2:

                    report_lines.append(f"  - {group[0]}  ↔  {group[1]}")

                else:

                    report_lines.append(f"  - {group[0]}  ↔  {group[1]}  (similaritate {group[2]})")



        if not any(problems.values()):

            report_lines.append("\n✅ Nu s-au găsit probleme! Șabloanele sunt curate.")



        report_lines.append("\n" + "=" * 60)

        report_text = "\n".join(report_lines)



        if log_queue:

            log_queue.put("\n" + report_text)

        logger.info("Scanare finalizată cu succes.")

        return report_text



    except Exception as e:

        logger.error(f"Eroare la scanare: {str(e)}\n{traceback.format_exc()}")

        if log_queue:

            log_queue.put(f"Eroare la scanare: {str(e)}")

        return None



def export_scan_report_html(report_text, output_path):

    html_content = f"""<!DOCTYPE html>

<html>

<head><meta charset="UTF-8"><title>Raport scanare șabloane</title>

<style>body {{ font-family: Arial, sans-serif; margin: 20px; }} pre {{ background: #f4f4f4; padding: 10px; }}</style>

</head>

<body><h1>Raport scanare șabloane</h1><pre>{report_text}</pre></body>

</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:

        f.write(html_content)



def export_scan_report_pdf(report_text, output_path):

    try:

        from reportlab.lib.pagesizes import A4

        from reportlab.pdfgen import canvas

        from reportlab.lib.utils import simpleSplit

    except ImportError:

        raise ImportError("ReportLab nu este instalat. Instalați cu: pip install reportlab")

    c = canvas.Canvas(output_path, pagesize=A4)

    width, height = A4

    margin = 50

    y = height - margin

    line_height = 14

    c.setFont("Helvetica", 10)

    for line in report_text.split('\n'):

        if y < margin:

            c.showPage()

            y = height - margin

            c.setFont("Helvetica", 10)

        words = line.split(' ')

        lines = []

        current = ""

        for w in words:

            if c.stringWidth(current + " " + w, "Helvetica", 10) < width - 2*margin:

                current += (" " + w if current else w)

            else:

                lines.append(current)

                current = w

        if current:

            lines.append(current)

        for l in lines:

            c.drawString(margin, y, l)

            y -= line_height

    c.save()