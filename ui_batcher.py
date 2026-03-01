# ui_batcher.py
import time
import threading

class UIUpdateBatcher:
    """Batch UI updates to reduce overhead"""
    def __init__(self, min_interval_ms: int = 100):
        self.min_interval_ms = min_interval_ms
        self.last_update = 0
        self.pending_updates = []
        self._lock = threading.Lock()
    
    def should_update(self) -> bool:
        """Check if enough time has passed for update"""
        current = time.time() * 1000  # Convert to ms
        if current - self.last_update >= self.min_interval_ms:
            self.last_update = current
            return True
        return False
    
    def add_update(self, update_func):
        """Add update to pending queue"""
        with self._lock:
            self.pending_updates.append(update_func)
    
    def flush(self):
        """Execute all pending updates"""
        with self._lock:
            updates = self.pending_updates[:]
            self.pending_updates.clear()
        for upd in updates:
            try:
                upd()
            except Exception as e:
                print(f"Update error: {e}")