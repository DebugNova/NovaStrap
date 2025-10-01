"""
RobloxLauncher - Handles launching Roblox with applied FFlags
"""
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple


class RobloxLauncher:
    """Launches Roblox player after applying FFlags."""
    
    @staticmethod
    def find_roblox_player() -> Optional[Path]:
        """
        Find the Roblox player executable.
        
        Returns:
            Path to RobloxPlayerBeta.exe if found, None otherwise
        """
        try:
            local_appdata = os.getenv("LOCALAPPDATA")
            if not local_appdata:
                return None
            
            roblox_path = Path(local_appdata) / "Roblox"
            if not roblox_path.exists():
                return None
            
            # Look for RobloxPlayerBeta.exe in Versions folders
            versions_path = roblox_path / "Versions"
            if not versions_path.exists():
                return None
            
            # Find the most recent version folder
            version_folders = [f for f in versions_path.iterdir() if f.is_dir()]
            
            for version_folder in sorted(version_folders, reverse=True):
                player_exe = version_folder / "RobloxPlayerBeta.exe"
                if player_exe.exists():
                    return player_exe
            
            return None
            
        except Exception:
            return None
    
    @staticmethod
    def launch_roblox() -> Tuple[bool, str]:
        """
        Launch Roblox player.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            player_exe = RobloxLauncher.find_roblox_player()
            
            if not player_exe:
                return False, "Roblox player executable not found. Please ensure Roblox is installed."
            
            # Launch Roblox
            subprocess.Popen([str(player_exe)], shell=False)
            
            return True, f"Launched Roblox from {player_exe.parent.name}"
            
        except Exception as e:
            return False, f"Failed to launch Roblox: {str(e)}"
    
    @staticmethod
    def launch_roblox_with_game(place_id: Optional[int] = None) -> Tuple[bool, str]:
        """
        Launch Roblox with a specific game.
        
        Args:
            place_id: Roblox place ID to join (optional)
        
        Returns:
            Tuple of (success, message)
        """
        try:
            player_exe = RobloxLauncher.find_roblox_player()
            
            if not player_exe:
                return False, "Roblox player executable not found. Please ensure Roblox is installed."
            
            if place_id:
                # Launch with deep link
                roblox_url = f"roblox://placeid={place_id}"
                subprocess.Popen([str(player_exe), roblox_url], shell=False)
                return True, f"Launching Roblox and joining place {place_id}"
            else:
                # Launch normally
                subprocess.Popen([str(player_exe)], shell=False)
                return True, f"Launched Roblox from {player_exe.parent.name}"
            
        except Exception as e:
            return False, f"Failed to launch Roblox: {str(e)}"
    
    @staticmethod
    def get_roblox_version() -> Optional[str]:
        """
        Get the installed Roblox version.
        
        Returns:
            Version string if found, None otherwise
        """
        try:
            player_exe = RobloxLauncher.find_roblox_player()
            if not player_exe:
                return None
            
            return player_exe.parent.name
            
        except Exception:
            return None

