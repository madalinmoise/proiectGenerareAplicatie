# plugin_manager.py
import importlib.util
import logging
from pathlib import Path

logger = logging.getLogger('HRAudit')

class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir()
            return
        for pyfile in self.plugin_dir.glob('*.py'):
            if pyfile.name.startswith('_'):
                continue
            try:
                spec = importlib.util.spec_from_file_location(pyfile.stem, pyfile)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register'):
                    module.register(self)
                    logger.info(f"Plugin încărcat: {pyfile.name}")
            except Exception as e:
                logger.error(f"Eroare la încărcarea pluginului {pyfile.name}: {e}")

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        logger.info(f"Plugin înregistrat: {plugin}")

    def get_export_formats(self):
        formats = []
        for p in self.plugins:
            if hasattr(p, 'export_formats'):
                formats.extend(p.export_formats())
        return formats

    def export_document(self, docx_path, format_name, output_path):
        for p in self.plugins:
            if hasattr(p, 'export') and p.can_export(format_name):
                p.export(docx_path, format_name, output_path)
                return True
        return False

plugin_manager = PluginManager()