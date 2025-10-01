"""
ProcessWatcher - Detects if Roblox processes are running
"""
import psutil
from typing import List


class ProcessWatcher:
    """Watches for Roblox processes."""
    
    ROBLOX_PROCESS_NAMES = [
        "RobloxPlayerBeta.exe",
        "RobloxPlayerLauncher.exe",
        "RobloxPlayer.exe",
        "RobloxStudioBeta.exe",
        "RobloxStudio.exe"
    ]
    
    @staticmethod
    def is_roblox_running() -> bool:
        """
        Check if any Roblox process is running.
        
        Returns:
            True if Roblox is running, False otherwise
        """
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] in ProcessWatcher.ROBLOX_PROCESS_NAMES:
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_running_roblox_processes() -> List[str]:
        """
        Get list of running Roblox process names.
        
        Returns:
            List of process names
        """
        running = []
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] in ProcessWatcher.ROBLOX_PROCESS_NAMES:
                        running.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass
        return running

