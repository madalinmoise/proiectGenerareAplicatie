import customtkinter as ctk

class EnterpriseTab(ctk.CTkFrame):
    """Base class for all enterprise tab components"""
    def __init__(self, master, engine, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.engine = engine
        self.engine.register_observer(self)
        self.setup_ui()

    def setup_ui(self):
        """Override this to build the UI"""
        pass

    def on_engine_event(self, event_type, data):
        """Handle events from the core engine"""
        pass
