"""
Installation and Module Test Script
Run this to verify all components are working correctly.
"""
import sys
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    errors = []
    
    # Test standard library
    try:
        import json
        import os
        import time
        import logging
        import ctypes
        print("  ✓ Standard library modules OK")
    except ImportError as e:
        errors.append(f"Standard library: {e}")
        print(f"  ✗ Standard library error: {e}")
    
    # Test PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        print("  ✓ PyQt6 OK")
    except ImportError as e:
        errors.append(f"PyQt6: {e}")
        print(f"  ✗ PyQt6 not installed: {e}")
        print("    Install with: pip install PyQt6")
    
    # Test psutil
    try:
        import psutil
        print("  ✓ psutil OK")
    except ImportError as e:
        errors.append(f"psutil: {e}")
        print(f"  ✗ psutil not installed: {e}")
        print("    Install with: pip install psutil")
    
    # Test pywin32
    try:
        import win32api
        import win32con
        print("  ✓ pywin32 OK")
    except ImportError as e:
        errors.append(f"pywin32: {e}")
        print(f"  ✗ pywin32 not installed: {e}")
        print("    Install with: pip install pywin32")
    
    return len(errors) == 0, errors


def test_modules():
    """Test if all application modules can be imported."""
    print("\nTesting application modules...")
    errors = []
    
    try:
        from path_manager import PathManager
        print("  ✓ PathManager OK")
    except ImportError as e:
        errors.append(f"PathManager: {e}")
        print(f"  ✗ PathManager error: {e}")
    
    try:
        from file_manager import FileManager
        print("  ✓ FileManager OK")
    except ImportError as e:
        errors.append(f"FileManager: {e}")
        print(f"  ✗ FileManager error: {e}")
    
    try:
        from json_validator import JsonValidator
        print("  ✓ JsonValidator OK")
    except ImportError as e:
        errors.append(f"JsonValidator: {e}")
        print(f"  ✗ JsonValidator error: {e}")
    
    try:
        from process_watcher import ProcessWatcher
        print("  ✓ ProcessWatcher OK")
    except ImportError as e:
        errors.append(f"ProcessWatcher: {e}")
        print(f"  ✗ ProcessWatcher error: {e}")
    
    try:
        from logger import AppLogger
        print("  ✓ Logger OK")
    except ImportError as e:
        errors.append(f"Logger: {e}")
        print(f"  ✗ Logger error: {e}")
    
    try:
        from roblox_launcher import RobloxLauncher
        print("  ✓ RobloxLauncher OK")
    except ImportError as e:
        errors.append(f"RobloxLauncher: {e}")
        print(f"  ✗ RobloxLauncher error: {e}")
    
    return len(errors) == 0, errors


def test_path_manager():
    """Test PathManager functionality."""
    print("\nTesting PathManager...")
    
    try:
        from path_manager import PathManager
        pm = PathManager()
        
        if pm.resolve_paths():
            print(f"  ✓ Paths resolved")
            print(f"    Target: {pm.get_target_file_str()}")
            
            if pm.ensure_client_settings_exists():
                print(f"  ✓ ClientSettings folder verified")
            else:
                print(f"  ✗ Failed to create ClientSettings folder")
                return False
        else:
            print(f"  ✗ Failed to resolve paths")
            print(f"    Is Roblox installed?")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ PathManager test failed: {e}")
        return False


def test_json_validator():
    """Test JsonValidator functionality."""
    print("\nTesting JsonValidator...")
    
    try:
        from json_validator import JsonValidator
        
        # Test valid JSON
        valid_json = '{"test": "value"}'
        is_valid, msg, data = JsonValidator.validate(valid_json)
        if is_valid:
            print("  ✓ Valid JSON accepted")
        else:
            print(f"  ✗ Valid JSON rejected: {msg}")
            return False
        
        # Test invalid JSON
        invalid_json = '{"test": invalid}'
        is_valid, msg, data = JsonValidator.validate(invalid_json)
        if not is_valid:
            print("  ✓ Invalid JSON rejected")
        else:
            print(f"  ✗ Invalid JSON accepted")
            return False
        
        # Test non-object JSON
        array_json = '["test"]'
        is_valid, msg, data = JsonValidator.validate(array_json)
        if not is_valid:
            print("  ✓ Non-object JSON rejected")
        else:
            print(f"  ✗ Array JSON accepted (should be object only)")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ JsonValidator test failed: {e}")
        return False


def test_process_watcher():
    """Test ProcessWatcher functionality."""
    print("\nTesting ProcessWatcher...")
    
    try:
        from process_watcher import ProcessWatcher
        
        is_running = ProcessWatcher.is_roblox_running()
        processes = ProcessWatcher.get_running_roblox_processes()
        
        if is_running:
            print(f"  ✓ Process detection working (Roblox IS running)")
            print(f"    Detected: {', '.join(processes)}")
        else:
            print(f"  ✓ Process detection working (Roblox NOT running)")
        
        return True
    except Exception as e:
        print(f"  ✗ ProcessWatcher test failed: {e}")
        return False


def test_roblox_launcher():
    """Test RobloxLauncher functionality."""
    print("\nTesting RobloxLauncher...")
    
    try:
        from roblox_launcher import RobloxLauncher
        
        player_exe = RobloxLauncher.find_roblox_player()
        
        if player_exe:
            print(f"  ✓ Roblox player found: {player_exe}")
            version = RobloxLauncher.get_roblox_version()
            if version:
                print(f"    Version: {version}")
        else:
            print(f"  ⚠️  Roblox player not found (is Roblox installed?)")
        
        return True
    except Exception as e:
        print(f"  ✗ RobloxLauncher test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Roblox FFlag Editor - Installation Test")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test imports
    passed, errors = test_imports()
    if not passed:
        all_passed = False
        print("\n⚠️  Some dependencies are missing!")
        print("Run: pip install -r requirements.txt")
    
    # Test modules
    passed, errors = test_modules()
    if not passed:
        all_passed = False
        print("\n⚠️  Some application modules failed to load!")
    
    # Only run functional tests if imports worked
    if all_passed:
        # Test PathManager
        if not test_path_manager():
            all_passed = False
        
        # Test JsonValidator
        if not test_json_validator():
            all_passed = False
        
        # Test ProcessWatcher
        if not test_process_watcher():
            all_passed = False
        
        # Test RobloxLauncher
        if not test_roblox_launcher():
            all_passed = False
    
    # Final result
    print()
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed! The application is ready to use.")
        print()
        print("Run the application with: python main.py")
        print("Or double-click: run.bat")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Ensure Roblox is installed")
        print("  - Run as normal user (not admin)")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

