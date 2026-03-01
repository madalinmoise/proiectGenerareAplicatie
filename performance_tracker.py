# performance_tracker.py
import time
from typing import Optional, Dict

class PerformanceTracker:
    """Track and analyze performance metrics"""
    
    def __init__(self):
        self.metrics_history = []
        self.current_job = None
    
    def start_job(self, job_id: str, total_items: int):
        """Start tracking a job"""
        self.current_job = {
            'job_id': job_id,
            'total_items': total_items,
            'start_time': time.time(),
            'completed_items': 0,
            'errors': 0,
            'avg_time_per_item': 0
        }
    
    def update_progress(self, completed: int):
        """Update job progress"""
        if self.current_job:
            self.current_job['completed_items'] = completed
            elapsed = time.time() - self.current_job['start_time']
            if completed > 0:
                self.current_job['avg_time_per_item'] = elapsed / completed
    
    def add_error(self):
        """Record an error"""
        if self.current_job:
            self.current_job['errors'] += 1
    
    def finish_job(self):
        """Finish tracking current job"""
        if self.current_job:
            self.current_job['end_time'] = time.time()
            self.current_job['duration'] = self.current_job['end_time'] - self.current_job['start_time']
            self.metrics_history.append(self.current_job.copy())
            self.current_job = None
    
    def get_eta(self) -> Optional[float]:
        """Calculate estimated time to completion"""
        if not self.current_job:
            return None
        completed = self.current_job['completed_items']
        total = self.current_job['total_items']
        avg_time = self.current_job['avg_time_per_item']
        if completed == 0 or avg_time == 0:
            return None
        remaining = total - completed
        return remaining * avg_time
    
    def get_summary(self) -> dict:
        """Get performance summary"""
        if not self.metrics_history:
            return {}
        total_jobs = len(self.metrics_history)
        total_items = sum(j['total_items'] for j in self.metrics_history)
        total_time = sum(j['duration'] for j in self.metrics_history)
        total_errors = sum(j['errors'] for j in self.metrics_history)
        return {
            'total_jobs': total_jobs,
            'total_items': total_items,
            'total_time': total_time,
            'total_errors': total_errors,
            'avg_items_per_job': total_items / total_jobs if total_jobs > 0 else 0,
            'avg_time_per_job': total_time / total_jobs if total_jobs > 0 else 0
        }