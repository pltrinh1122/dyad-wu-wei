import os
import shutil
import tempfile

class FlowTransaction:
    """Manages the transactional context and rollback logic for orchestration tasks."""
    
    def __init__(self, frontier_file: str = "artifacts/frontier_state.md"):
        self.frontier_file = frontier_file
        self.yml_file = frontier_file.replace(".md", ".yml")
        self.sha_file = frontier_file.replace(".md", ".yml.sha256")
        
        self.rollback_stack = []
        self.temp_dir = None
        self.backups = {}

    def __enter__(self):
        # Create temp dir for backups
        self.temp_dir = tempfile.mkdtemp()
        
        # Backup frontier state ledger files
        for path in [self.frontier_file, self.yml_file, self.sha_file]:
            if os.path.exists(path):
                backup_name = os.path.basename(path) + ".bak"
                backup_path = os.path.join(self.temp_dir, backup_name)
                shutil.copy2(path, backup_path)
                self.backups[path] = backup_path
                
        return self

    def register_rollback(self, func, *args, **kwargs):
        """Pushes a rollback action to the transaction stack."""
        self.rollback_stack.append((func, args, kwargs))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Transaction failed! Roll back mutations
            print(f"\n⚠️ FlowTransaction failed: {exc_val}")
            print("Initiating rollback actions...")
            
            # 1. Restore frontier state backup files
            for original, backup in self.backups.items():
                if os.path.exists(backup):
                    shutil.copy2(backup, original)
            
            # 2. Run registered cleanup/rollback calls in reverse order
            for func, args, kwargs in reversed(self.rollback_stack):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Error during rollback: {e}")
                    
        # Cleanup backup files
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
