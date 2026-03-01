# audit.py
import json
import threading
from datetime import datetime

class AuditLogger:
    def __init__(self, filename='audit.jsonl'):
        self.filename = filename
        self.lock = threading.Lock()

    def log(self, user='system', action='', details=None):
        try:
            with self.lock:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    record = {
                        'timestamp': datetime.now().isoformat(),
                        'user': user,
                        'action': action,
                        'details': details or {}
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Eroare audit log: {e}")

audit = AuditLogger()