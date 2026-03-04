import os
import re
import pandas as pd
import threading
import logging
import traceback
import queue
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from multiprocessing import Process, Queue, Event
from template_utils import (
    extract_all_placeholders_from_files,
    render_documents,
    extract_placeholders_from_file
)
from services.analytics_service import AnalyticsService

logger = logging.getLogger('HRAudit.Engine')

class DocumentEngine:
    """Enterprise Document Engine - Central logic hub"""

    def __init__(self):
        self.config = {
            'template_files': [],
            'data_file': '',
            'output_dir': 'output',
            'folder_column': 'ID',
            'filename_pattern': '{ID}_{template_name}.docx'
        }
        self.active_process = None
        self.status_queue = Queue()
        self.is_running = False
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def notify_observers(self, event_type, data):
        for obs in self._observers:
            if hasattr(obs, 'on_engine_event'):
                obs.on_engine_event(event_type, data)

    def set_config(self, config_dict: Dict[str, Any]):
        self.config.update(config_dict)
        self.notify_observers('config_updated', self.config)

    def load_data(self) -> Optional[pd.DataFrame]:
        path = self.config.get('data_file', '')
        if not path or not os.path.exists(path):
            return None
        try:
            return pd.read_excel(path).fillna('')
        except Exception as e:
            logger.error(f"Engine data load error: {e}")
            return None

    def get_stats(self) -> Dict[str, Any]:
        df = self.load_data()
        if df is None: return {}
        return {
            'research_grades': AnalyticsService.get_research_grades(df),
            'student_types': AnalyticsService.get_student_types(df),
            'integrity': AnalyticsService.get_integrity_audit(df),
            'summary': {
                'rows': len(df),
                'cols': len(df.columns)
            }
        }

    def start_rendering(self, options: Dict[str, Any]):
        """Compatibility wrapper for start_job"""
        return self.start_job(options)

    def start_job(self, options: Dict[str, Any]):
        if self.is_running:
            return False

        self.is_running = True
        self.active_process = Process(
            target=self._run_process,
            args=(self.config, options, self.status_queue)
        )
        self.active_process.start()

        threading.Thread(target=self._monitor_queue, daemon=True).start()
        self.notify_observers('job_started', {})
        return True

    def _monitor_queue(self):
        while self.is_running:
            try:
                msg = self.status_queue.get(timeout=0.1)
                if msg[0] == 'FINISH':
                    self.is_running = False
                    self.notify_observers('job_finished', msg[1])
                elif msg[0] == 'PROGRESS':
                    self.notify_observers('job_progress', msg[1])
                elif msg[0] == 'LOG':
                    self.notify_observers('engine_log', msg[1])
                elif msg[0] == 'SUCCESS':
                    self.notify_observers('success_count_inc', msg[1])
                elif msg[0] == 'ERROR':
                    self.notify_observers('error_count_inc', msg[1])
            except queue.Empty:
                continue

    @staticmethod
    def _run_process(config, options, status_q):
        try:
            def progress_cb(current, total):
                status_q.put(('PROGRESS', {'current': current, 'total': total}))

            class ProxyLogger:
                def put(self, msg):
                    if isinstance(msg, tuple):
                        status_q.put(msg)
                    else:
                        status_q.put(('LOG', msg))

            render_documents(
                template_files=config.get('template_files', []),
                data_file=config.get('data_file', ''),
                output_folder=config.get('output_dir', 'output'),
                folder_column=config.get('folder_column', 'ID'),
                log_queue=ProxyLogger(),
                progress_callback=progress_cb,
                filename_pattern=config.get('filename_pattern', '{ID}'),
                **options
            )
            status_q.put(('FINISH', {'status': 'success'}))
        except Exception as e:
            status_q.put(('FINISH', {'status': 'error', 'error': str(e)}))

    def stop_job(self):
        if self.active_process and self.active_process.is_alive():
            self.active_process.terminate()
            self.is_running = False
            self.notify_observers('job_stopped', {})

    def extract_placeholders(self, callback: Optional[Callable] = None):
        files = self.config.get('template_files', [])
        valid_files = [f for f in files if os.path.exists(f)]
        if not valid_files:
            return [], {}
        return extract_all_placeholders_from_files(valid_files, progress_callback=callback)
