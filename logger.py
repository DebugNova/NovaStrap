"""
Logger - Handles application logging
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


class AppLogger:
    """Application logger for FFlag Editor."""
    
    def __init__(self, log_file: Optional[Path] = None):
        """
        Initialize logger.
        
        Args:
            log_file: Path to log file (default: fflag_editor.log in current directory)
        """
        if log_file is None:
            log_file = Path("fflag_editor.log")
        
        self.log_file = log_file
        self.logger = logging.getLogger("FFlagEditor")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def info(self, message: str) -> None:
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message."""
        self.logger.error(message)
    
    def success(self, message: str) -> None:
        """Log success message (as info)."""
        self.logger.info(f"SUCCESS: {message}")
    
    def get_recent_logs(self, lines: int = 100) -> str:
        """
        Get recent log entries.
        
        Args:
            lines: Number of recent lines to retrieve
        
        Returns:
            Recent log content as string
        """
        try:
            if not self.log_file.exists():
                return "No logs available"
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent = all_lines[-lines:] if len(all_lines) > lines else all_lines
                return ''.join(recent)
        except Exception as e:
            return f"Error reading logs: {e}"
    
    def clear_logs(self) -> None:
        """Clear the log file."""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
                # Reinitialize logger
                self.__init__(self.log_file)
        except Exception:
            pass

