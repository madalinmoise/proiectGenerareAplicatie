# web_api.py
from flask import Flask, jsonify, request, render_template, send_from_directory
import threading
import os
import psutil
import pandas as pd
from pathlib import Path

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')
app.config['JSON_SORT_KEYS'] = False
main_app = None

def start_server(app_instance):
    global main_app
    main_app = app_instance
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/wizard/preview-excel')
def api_preview_excel():
    if not main_app:
        return jsonify({'error': 'App not initialized'}), 500

    file_path = main_app.data_file_path.get()
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Niciun fișier Excel selectat în Desktop.'})

    try:
        df = pd.read_excel(file_path, sheet_name=0, nrows=50)
        return jsonify({
            'columns': list(df.columns),
            'rows': df.fillna('').to_dict(orient='records'),
            'file': os.path.basename(file_path)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/wizard/upload-excel', methods=['POST'])
def api_upload_excel():
    if not main_app: return jsonify({'error': 'App not init'}), 500
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save to a temp location so pandas can read it
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / file.filename
    file.save(temp_path)

    # Update main_app
    main_app.data_file_path.set(str(temp_path.absolute()))
    main_app.load_excel_columns()
    main_app.incarca_previzualizare_excel_async()
    main_app.load_global_excel_df(str(temp_path.absolute()))

    return jsonify({'status': 'success', 'file': file.filename})

@app.route('/api/wizard/templates')
def api_templates():
    if not main_app:
        return jsonify({'templates': [], 'count': 0})
    return jsonify({
        'templates': main_app.template_files,
        'count': len(main_app.template_files)
    })

@app.route('/api/wizard/upload-template', methods=['POST'])
def api_upload_template():
    if not main_app: return jsonify({'error': 'App not init'}), 500
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files'})

    files = request.files.getlist('files[]')
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)

    paths = []
    for file in files:
        if file.filename:
            temp_path = temp_dir / file.filename
            file.save(temp_path)
            paths.append(str(temp_path.absolute()))

    if paths:
        main_app.add_template_files(paths)

    return jsonify({'status': 'success', 'count': len(paths)})

@app.route('/api/wizard/options', methods=['GET'])
def api_get_options():
    if not main_app: return jsonify({'error': 'App not init'}), 500
    try:
        opts = {
            'folder_column': main_app.folder_column.get(),
            'output_dir': main_app.output_dir_path.get(),
            'filename_pattern': main_app.filename_pattern.get(),
            'multiprocessing': main_app.multiprocessing_var.get(),
            'pdf_gen': main_app.pdf_var.get(),
            'zip_per_row': main_app.zip_per_row_var.get(),
            'available_columns': list(main_app.global_excel_df.columns) if main_app.global_excel_df is not None else []
        }
        return jsonify(opts)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/wizard/options', methods=['POST'])
def api_set_options():
    if not main_app: return jsonify({'error': 'App not init'}), 500
    data = request.json
    try:
        if 'folder_column' in data: main_app.folder_column.set(data['folder_column'])
        if 'output_dir' in data: main_app.output_dir_path.set(data['output_dir'])
        if 'filename_pattern' in data: main_app.filename_pattern.set(data['filename_pattern'])
        if 'multiprocessing' in data: main_app.multiprocessing_var.set(bool(data['multiprocessing']))
        if 'pdf_gen' in data: main_app.pdf_var.set(bool(data['pdf_gen']))
        if 'zip_per_row' in data: main_app.zip_per_row_var.set(bool(data['zip_per_row']))
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/wizard/stats')
def api_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    stats = {
        'percent': getattr(main_app, 'progress_val', 0),
        'success': getattr(main_app, 'success_count', 0),
        'errors': getattr(main_app, 'error_count', 0),
        'pending': max(0, 100 - getattr(main_app, 'progress_val', 0)),
        'cpu': cpu,
        'ram': ram
    }
    return jsonify(stats)

@app.route('/api/wizard/start', methods=['POST'])
def api_start():
    if not main_app:
        return jsonify({'error': 'App not initialized'}), 500
    print("DEBUG: api_start called in web_api", flush=True)
    main_app.after(0, lambda: main_app.start_render())
    return jsonify({'status': 'started'})

@app.route('/api/wizard/stop', methods=['POST'])
def api_stop():
    if not main_app:
        return jsonify({'error': 'App not initialized'}), 500
    main_app.after(0, lambda: main_app.stop_operation())
    return jsonify({'status': 'stopped'})

@app.route('/api/wizard/recent-excel')
def api_recent_excel():
    return jsonify({'recent': getattr(main_app, 'recent_files', [])})

@app.route('/api/debug/state')
def api_debug_state():
    if not main_app: return jsonify({'error': 'no app'})
    return jsonify({
        'data_file': main_app.data_file_path.get(),
        'template_files': main_app.template_files,
        'output_dir': main_app.output_dir_path.get(),
        'folder_column': main_app.folder_column.get(),
        'is_generating': getattr(main_app, 'is_generating', False)
    })