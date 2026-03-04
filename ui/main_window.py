import customtkinter as ctk
from ui.components.sidebar import EnterpriseSidebar
from ui.components.dashboard import DashboardTab
from ui.components.render_tab import RenderTab
from ui.components.reports_tab import ReportsTab
from ui.components.audit_tab import AuditTab
from ui.components.extract_tab import ExtractTab
from ui.components.settings_tab import SettingsTab
from ui.components.excel_viewer import ExcelViewerTab
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
            "Rapoarte": ReportsTab,
            "Audit Log": AuditTab,
            "Setări": SettingsTab,
            "4. Vizualizare Excel": ExcelViewerTab
        }
        self.tabs = {}
        self.current_tab = None

        # Initial Tab
        self.set_tab("Dashboard")

    def set_tab(self, name):
        if name not in self.tab_classes:
            print(f"Tab {name} not implemented in modern UI yet.")
            return

        if self.current_tab:
            self.current_tab.grid_forget()

        if name not in self.tabs:
            self.tabs[name] = self.tab_classes[name](self.main_container, self.engine)

        self.tabs[name].grid(row=0, column=0, sticky="nsew")
        self.current_tab = self.tabs[name]

    def start_render(self):
        """Backward compatibility for Web API"""
        if hasattr(self, 'engine'):
            # Fetch options from config or UI state
            options = {
                'parallel': self.config_mgr.get('multiprocessing', True),
                'pdf_gen': self.config_mgr.get('pdf_gen', False)
            }
            return self.engine.start_job(options)

    def stop_operation(self):
        """Backward compatibility for Web API"""
        if hasattr(self, 'engine'):
            self.engine.stop_job()

    @property
    def template_files(self):
        return self.engine.config.get('template_files', [])

    @property
    def data_file_path(self):
        # Return a mock object that has a .get() method to match current app structure if needed
        class MockVar:
            def __init__(self, val): self.val = val
            def get(self): return self.val
            def set(self, v): pass
        return MockVar(self.engine.config.get('data_file', ''))

if __name__ == "__main__":
    app = EnterpriseApp()
    app.mainloop()
