"""
FileManager - Handles file operations including atomic writes, backups, and read-only attributes
"""
import json
import time
import os
import ctypes
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional, Dict, Any, List


class FileManager:
    """Manages file operations for FFlag configuration."""
    
    FILE_ATTRIBUTE_READONLY = 0x01
    FILE_ATTRIBUTE_NORMAL = 0x80
    
    def __init__(self, target_path: Path):
        """
        Initialize FileManager.
        
        Args:
            target_path: Path to the target file
        """
        self.target_path = target_path
    
    def backup_file(self) -> Optional[Path]:
        """
        Create a timestamped backup of the target file if it exists.
        
        Returns:
            Path to backup file if created, None otherwise
        """
        if not self.target_path.exists():
            return None
        
        try:
            # Remove read-only attribute before backing up
            self._clear_readonly()
            
            stamp = time.strftime("%Y%m%d_%H%M%S")
            bak = self.target_path.with_name(
                f"{self.target_path.stem}.bak.{stamp}{self.target_path.suffix}"
            )
            
            # Copy content to backup
            bak.write_bytes(self.target_path.read_bytes())
            return bak
        except Exception as e:
            raise Exception(f"Failed to create backup: {e}")
    
    def atomic_write_json(self, data: Dict[str, Any]) -> None:
        """
        Atomically write JSON data to target file.
        
        Args:
            data: Dictionary to write as JSON
        
        Raises:
            Exception: If write fails
        """
        try:
            # Ensure parent directory exists
            self.target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove read-only attribute if file exists
            if self.target_path.exists():
                self._clear_readonly()
            
            # Write to temporary file first
            with NamedTemporaryFile(
                mode="w",
                dir=str(self.target_path.parent),
                delete=False,
                encoding="utf-8",
                suffix=".tmp"
            ) as tf:
                json.dump(data, tf, indent=2, ensure_ascii=False)
                tf.flush()
                os.fsync(tf.fileno())
                tmpname = Path(tf.name)
            
            # Atomic replace
            tmpname.replace(self.target_path)
            
        except Exception as e:
            raise Exception(f"Failed to write file: {e}")
    
    def set_readonly(self) -> None:
        """Set the target file to read-only."""
        try:
            ctypes.windll.kernel32.SetFileAttributesW(
                str(self.target_path),
                self.FILE_ATTRIBUTE_READONLY
            )
        except Exception as e:
            raise Exception(f"Failed to set read-only attribute: {e}")
    
    def _clear_readonly(self) -> None:
        """Clear the read-only attribute from the target file."""
        try:
            if self.target_path.exists():
                ctypes.windll.kernel32.SetFileAttributesW(
                    str(self.target_path),
                    self.FILE_ATTRIBUTE_NORMAL
                )
        except Exception:
            pass
    
    def read_current_content(self) -> Optional[str]:
        """
        Read current content of target file.
        
        Returns:
            File content as string, or None if file doesn't exist
        """
        try:
            if self.target_path.exists():
                # Temporarily clear read-only to read
                return self.target_path.read_text(encoding="utf-8")
            return None
        except Exception:
            return None
    
    def get_backup_files(self) -> List[Path]:
        """
        Get list of backup files for the target file.
        
        Returns:
            List of backup file paths, sorted by modification time (newest first)
        """
        try:
            pattern = f"{self.target_path.stem}.bak.*{self.target_path.suffix}"
            backups = list(self.target_path.parent.glob(pattern))
            backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return backups
        except Exception:
            return []
    
    def restore_backup(self, backup_path: Path) -> None:
        """
        Restore a backup file to the target file.
        
        Args:
            backup_path: Path to the backup file to restore
        
        Raises:
            Exception: If restore fails
        """
        try:
            if not backup_path.exists():
                raise Exception("Backup file not found")
            
            # Remove read-only from target if exists
            if self.target_path.exists():
                self._clear_readonly()
            
            # Copy backup to target
            content = backup_path.read_text(encoding="utf-8")
            data = json.loads(content)  # Validate it's valid JSON
            self.atomic_write_json(data)
            
        except Exception as e:
            raise Exception(f"Failed to restore backup: {e}")

