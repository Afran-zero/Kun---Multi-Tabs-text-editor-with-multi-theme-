"""
File operations module for Kun text editor.
Handles saving, opening, recent files, and session management.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class FileOperations:
    """Manages all file I/O operations and session persistence."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "kun_config.json"
        self.config_path = Path(config_path)
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Return default config
        return {
            "recent_files": [],
            "theme": "noir",
            "auto_save": False,
            "auto_save_interval": 60,
            "restore_session": True,
            "show_line_numbers": False,
            "spell_check_enabled": True,
            "char_count_mode": "with_spaces",
            "last_session": {"tabs": []}
        }
    
    def save_config(self):
        """Persist configuration to disk."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def add_recent_file(self, file_path: str):
        """Add file to recent files list (max 15)."""
        if not file_path:
            return
            
        recent = self.config.get("recent_files", [])
        
        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)
        
        # Add to front
        recent.insert(0, file_path)
        
        # Keep only 15 most recent
        self.config["recent_files"] = recent[:15]
        self.save_config()
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files (filters out non-existent files)."""
        recent = self.config.get("recent_files", [])
        # Filter out files that no longer exist
        existing = [f for f in recent if os.path.exists(f)]
        if len(existing) != len(recent):
            self.config["recent_files"] = existing
            self.save_config()
        return existing
    
    def clear_recent_files(self):
        """Clear all recent files."""
        self.config["recent_files"] = []
        self.save_config()
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Read text file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to text file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    def save_session(self, tabs: List[Dict]):
        """Save current session (open tabs) to config."""
        self.config["last_session"] = {"tabs": tabs}
        self.save_config()
    
    def restore_session(self) -> List[Dict]:
        """Restore last session tabs."""
        if self.config.get("restore_session", True):
            return self.config.get("last_session", {}).get("tabs", [])
        return []
    
    def get_setting(self, key: str, default=None):
        """Get a configuration setting."""
        return self.config.get(key, default)
    
    def set_setting(self, key: str, value):
        """Set a configuration setting and save."""
        self.config[key] = value
        self.save_config()
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path) if file_path else False
