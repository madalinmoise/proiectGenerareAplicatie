# macro.py
class MacroRecorder:
    def __init__(self):
        self.recording = False
        self.actions = []
        self.code = ""

    def start(self):
        self.recording = True
        self.actions = []
        self.code = "# Macro înregistrat\nimport time\n\ndef run(app):\n"

    def stop(self):
        self.recording = False
        return self.code

    def record(self, description, code_line=None):
        if self.recording:
            self.actions.append(description)
            if code_line:
                self.code += "    " + code_line + "\n"
            else:
                self.code += "    # " + description + "\n"