import os
import re
import pandas as pd
import threading
import logging
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from template_utils import (
    extract_all_placeholders_from_files,
    render_documents,
    extract_placeholders_from_file
)

logger = logging.getLogger('HRAudit.Engine')

class DocumentEngine:
    """Headless engine for document processing and data management"""

    def __init__(self):
        self.template_files = []
        self.data_file = ""
        self.output_dir = "output"
        self.folder_column = ""
        self.filename_pattern = "{ID}_{template_name}.docx"
        self.scripts = []
        self.stop_event = threading.Event()
        self.is_running = False

        # Performance/State tracking
        self.success_count = 0
        self.error_count = 0
        self.total_count = 0
        self.progress = 0.0

    def set_config(self, config_dict: Dict[str, Any]):
        self.template_files = config_dict.get('template_files', self.template_files)
        self.data_file = config_dict.get('data_file', self.data_file)
        self.output_dir = config_dict.get('output_dir', self.output_dir)
        self.folder_column = config_dict.get('folder_column', self.folder_column)
        self.filename_pattern = config_dict.get('filename_pattern', self.filename_pattern)

    def extract_placeholders(self, callback: Optional[Callable] = None):
        """Extract placeholders from loaded template files"""
        if not self.template_files:
            return [], {}
        return extract_all_placeholders_from_files(self.template_files, progress_callback=callback)

    def start_rendering(self, progress_cb: Callable, log_queue: Any, options: Dict[str, Any]):
        """Initiate the rendering process"""
        if self.is_running:
            return

        self.is_running = True
        self.stop_event.clear()
        self.success_count = 0
        self.error_count = 0

        thread = threading.Thread(
            target=self._render_task,
            args=(progress_cb, log_queue, options),
            daemon=True
        )
        thread.start()
        return thread

    def stop_rendering(self):
        self.stop_event.set()

    def _render_task(self, progress_cb, log_queue, options):
        try:
            render_documents(
                template_files=self.template_files,
                data_file=self.data_file,
                output_folder=self.output_dir,
                folder_column=self.folder_column,
                log_queue=log_queue,
                progress_callback=progress_cb,
                stop_event=self.stop_event,
                filename_pattern=self.filename_pattern,
                **options
            )
        except Exception as e:
            if log_queue:
                log_queue.put(f"Engine Error: {str(e)}")
            logger.error(traceback.format_exc())
        finally:
            self.is_running = False

    def load_data(self) -> Optional[pd.DataFrame]:
        """Load the Excel data file"""
        if not self.data_file or not os.path.exists(self.data_file):
            return None
        try:
            return pd.read_excel(self.data_file).fillna('')
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return None

    def get_additional_stats(self) -> Dict[str, Any]:
        """Fetch all advanced analytics for the current dataset"""
        df = self.load_data()
        if df is None:
            return {}

        from services.analytics_service import AnalyticsService
        return {
            'research_grades': AnalyticsService.get_research_grades(df),
            'student_types': AnalyticsService.get_student_types(df),
            'integrity': AnalyticsService.get_integrity_audit(df)
        }
