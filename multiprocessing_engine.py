# multiprocessing_engine.py
import multiprocessing as mp
import pickle
import time
import os
from pathlib import Path
from typing import Optional, Dict, List
from docxtpl import DocxTemplate
import io
import datetime
import json

class MultiprocessingEngine:
    """Advanced multiprocessing engine for parallel document generation"""
    
    def __init__(self, num_workers: Optional[int] = None):
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        self.manager = None
        self.progress_queue = None
        self.checkpoint_dir = Path("checkpoints")
        self.checkpoint_dir.mkdir(exist_ok=True)

    def ensure_manager(self):
        """Ensure Manager and progress_queue are initialized (lazy)."""
        if self.manager is None:
            try:
                self.manager = mp.Manager()
                self.progress_queue = self.manager.Queue()
            except Exception:
                # Fallback to multiprocessing.Queue if Manager can't be created
                from multiprocessing import Queue
                self.progress_queue = Queue()
    
    @staticmethod
    def process_single_document(args):
        """Worker function for processing a single document"""
        try:
            idx, row_data, template_data, config = args
            
            # Create context
            context = row_data.copy()
            
            # Parse JSON in cells
            final_context = {}
            for k, v in context.items():
                try:
                    if isinstance(v, str) and (v.strip().startswith('[') or v.strip().startswith('{')):
                        final_context[k] = json.loads(v)
                    else:
                        final_context[k] = v
                except:
                    final_context[k] = v
            
            # Determine entity name
            nume_entitate = "Necunoscut"
            for k in final_context.keys():
                if "nume" in k.lower():
                    nume_entitate = str(final_context[k])
                    break
            
            if nume_entitate == "Necunoscut":
                nume_entitate = f"ID_{idx+1}"
            
            nume_safe = MultiprocessingEngine.sanitize_name(nume_entitate)
            
            results = []
            
            # Process each template
            for tpl in template_data:
                try:
                    # Generate document
                    mem_file = io.BytesIO(tpl['content'])
                    doc = DocxTemplate(mem_file)
                    doc.render(final_context)
                    
                    # Generate filename
                    fname_res = f"{tpl['name_prefix']}_{nume_safe}"
                    
                    # Determine output directory
                    final_out_dir = config['output_folder']
                    sub_col = config.get('subfolder_col')
                    
                    if sub_col and sub_col != "(Niciunul)" and sub_col in final_context:
                        val_sub = MultiprocessingEngine.sanitize_name(final_context[sub_col])
                        if val_sub:
                            final_out_dir = os.path.join(final_out_dir, val_sub)
                            os.makedirs(final_out_dir, exist_ok=True)
                    
                    fname_res = MultiprocessingEngine.sanitize_name(fname_res)
                    if not fname_res:
                        fname_res = f"Doc_{idx}"
                    
                    fname = f"{fname_res}.docx"
                    out_path = os.path.join(final_out_dir, fname)
                    
                    # Save document
                    doc.save(out_path)
                    
                    results.append({
                        'status': 'SUCCESS',
                        'path': out_path,
                        'filename': fname,
                        'entity': nume_entitate
                    })
                    
                except Exception as e:
                    results.append({
                        'status': 'ERROR',
                        'error': str(e),
                        'filename': fname if 'fname' in locals() else 'Unknown',
                        'entity': nume_entitate
                    })
            
            return {
                'idx': idx,
                'results': results,
                'status': 'COMPLETED'
            }
            
        except Exception as e:
            return {
                'idx': idx,
                'results': [],
                'status': 'FAILED',
                'error': str(e)
            }
    
    @staticmethod
    def sanitize_name(name):
        """Clean filename"""
        if not name:
            return "Document"
        allowed_chars = ('_', '-', ' ', 'ă', 'â', 'î', 'ș', 'ț', 'Ă', 'Â', 'Î', 'Ș', 'Ț')
        return "".join([c for c in str(name) if c.isalnum() or c in allowed_chars]).strip()
    
    def create_checkpoint(self, job_id: str, completed_indices: set, total: int):
        """Save checkpoint for recovery"""
        checkpoint_data = {
            'job_id': job_id,
            'completed': list(completed_indices),
            'total': total,
            'timestamp': datetime.datetime.now().isoformat()
        }
        checkpoint_file = self.checkpoint_dir / f"{job_id}.checkpoint"
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(checkpoint_data, f)
    
    def load_checkpoint(self, job_id: str) -> Optional[dict]:
        """Load checkpoint if exists"""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.checkpoint"
        if checkpoint_file.exists():
            try:
                with open(checkpoint_file, 'rb') as f:
                    return pickle.load(f)
            except:
                return None
        return None
    
    def cleanup_checkpoint(self, job_id: str):
        """Remove checkpoint after successful completion"""
        checkpoint_file = self.checkpoint_dir / f"{job_id}.checkpoint"
        if checkpoint_file.exists():
            checkpoint_file.unlink()