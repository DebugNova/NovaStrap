"""
PathManager - Handles path resolution for Roblox ClientSettings
"""
import os
from pathlib import Path
from typing import Optional


class PathManager:
    """Manages paths for Roblox FFlag configuration files."""
    
    def __init__(self, filename: str = "IxpSettings.json"):
        """
        Initialize PathManager.
        
        Args:
            filename: Target filename (default: IxpSettings.json)
        """
        self.filename = filename
        self._local_appdata: Optional[str] = None
        self._roblox_path: Optional[Path] = None
        self._client_settings: Optional[Path] = None
        self._target_file: Optional[Path] = None
        
    def resolve_paths(self) -> bool:
        """
        Resolve all required paths.
        
        Returns:
            True if paths resolved successfully, False otherwise
        """
        try:
            self._local_appdata = os.getenv("LOCALAPPDATA")
            if not self._local_appdata:
                return False
                
            self._roblox_path = Path(self._local_appdata) / "Roblox"
            self._client_settings = self._roblox_path / "ClientSettings"
            self._target_file = self._client_settings / self.filename
            
            return True
        except Exception:
            return False
    
    def ensure_client_settings_exists(self) -> bool:
        """
        Ensure ClientSettings folder exists, create if missing.
        
        Returns:
            True if folder exists or was created successfully
        """
        try:
            if self._client_settings is None:
                return False
            self._client_settings.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @property
    def target_file(self) -> Optional[Path]:
        """Get the target file path."""
        return self._target_file
    
    @property
    def client_settings(self) -> Optional[Path]:
        """Get the ClientSettings folder path."""
        return self._client_settings
    
    @property
    def roblox_path(self) -> Optional[Path]:
        """Get the Roblox folder path."""
        return self._roblox_path
    
    def get_target_file_str(self) -> str:
        """Get target file path as string for display."""
        if self._target_file:
            return str(self._target_file)
        return "Path not resolved"


