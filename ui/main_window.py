import customtkinter as ctk
from ui.components.sidebar import EnterpriseSidebar
from ui.components.dashboard import DashboardTab
from ui.components.render_tab import RenderTab
from ui.components.reports_tab import ReportsTab
from ui.components.audit_tab import AuditTab
from ui.components.extract_tab import ExtractTab
from ui.components.settings_tab import SettingsTab
from ui.components.excel_viewer import ExcelViewerTab
from ui.components.word_viewer import WordViewerTab
from core.engine import DocumentEngine
from core.config_manager import ConfigManager

class EnterpriseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Enterprise Document Hub v6.5")
        self.geometry("1280x850")

        # Core Components
        self.config_mgr = ConfigManager()
        self.engine = DocumentEngine()
        self.engine.set_config(self.config_mgr.config)

        # Main Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = EnterpriseSidebar(self, tab_callback=self.set_tab)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.tab_classes = {
            "Dashboard": DashboardTab,
            "Pasul 1: Extrage placeholders": ExtractTab,
            "Pasul 2: Generează documente": RenderTab,
            "Vizualizare Excel": ExcelViewerTab,
            "Vizualizare Word": WordViewerTab,
            "Rapoarte": ReportsTab,
            "Audit Log": AuditTab,
            "Setări": SettingsTab
        }
        self.tabs = {}
        self.current_tab = None

        self.progress_val = 0
        self.success_count = 0
        self.error_count = 0
        self.engine.register_observer(self)

        # Initial Tab
        self.set_tab("Dashboard")

    def on_engine_event(self, event_type, data):
        if event_type == 'job_progress':
            if data['total'] > 0:
                self.progress_val = (data['current'] / data['total']) * 100
        elif event_type == 'success_count_inc':
            self.success_count += 1
        elif event_type == 'error_count_inc':
            self.error_count += 1
        elif event_type == 'job_started':
            self.success_count = 0
            self.error_count = 0
            self.progress_val = 0

    def set_tab(self, name):
        if name not in self.tab_classes:
            return

        if self.current_tab:
            self.current_tab.grid_forget()

        if name not in self.tabs:
            self.tabs[name] = self.tab_classes[name](self.main_container, self.engine)

        self.tabs[name].grid(row=0, column=0, sticky="nsew")
        self.current_tab = self.tabs[name]

    def start_render(self):
        options = {
            'parallel': self.config_mgr.get('multiprocessing', True),
            'pdf_gen': self.config_mgr.get('pdf_gen', False)
        }
        return self.engine.start_job(options)

    def stop_operation(self):
        self.engine.stop_job()

    @property
    def template_files(self):
        return self.engine.config.get('template_files', [])

    @property
    def data_file_path(self):
        class ConfigVar:
            def __init__(self, mgr, key):
                self.mgr = mgr
                self.key = key
            def get(self): return self.mgr.get(self.key, '')
            def set(self, v): self.mgr.set(self.key, v)
        return ConfigVar(self.config_mgr, 'data_file')

    @property
    def folder_column(self):
        return self._get_config_var('folder_column')

    @property
    def output_dir_path(self):
        return self._get_config_var('output_dir')

    @property
    def filename_pattern(self):
        return self._get_config_var('filename_pattern')

    @property
    def multiprocessing_var(self):
        return self._get_config_var('multiprocessing')

    @property
    def pdf_var(self):
        return self._get_config_var('pdf_gen')

    @property
    def zip_per_row_var(self):
        return self._get_config_var('zip_per_row')

    def _get_config_var(self, key):
        class ConfigVar:
            def __init__(self, mgr, k):
                self.mgr = mgr
                self.k = k
            def get(self): return self.mgr.get(self.k)
            def set(self, v): self.mgr.set(self.k, v)
        return ConfigVar(self.config_mgr, key)

    def load_excel_columns(self):
        # Triggered by web_api, usually used to refresh UI components
        self.engine.notify_observers('config_updated', self.engine.config)

    def incarca_previzualizare_excel_async(self):
        # Logic is handled by observers (ExcelViewerTab)
        self.engine.notify_observers('data_loaded', self.engine.load_data())

    @property
    def global_excel_df(self):
        return self.engine.load_data()

    def load_global_excel_df(self, p):
        self.engine.set_config({'data_file': p})

    def add_template_files(self, p):
        current = self.engine.config.get('template_files', [])
        new_list = list(set(current + p))
        self.config_mgr.set('template_files', new_list)
        self.engine.set_config({'template_files': new_list})

if __name__ == "__main__":
    app = EnterpriseApp()
    app.mainloop()
