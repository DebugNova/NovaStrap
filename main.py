"""
NovaStrap - Main Application
Made by Nova

A beautiful, modern Windows desktop utility for editing Roblox ClientSettings FFlags.
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QMessageBox, QFileDialog,
    QDialog, QDialogButtonBox, QListWidget, QStatusBar, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QTextCursor, QTextCharFormat, QColor

from path_manager import PathManager
from file_manager import FileManager
from json_validator import JsonValidator
from process_watcher import ProcessWatcher
from logger import AppLogger
from roblox_launcher import RobloxLauncher


class DisclaimerDialog(QDialog):
    """First-run disclaimer dialog."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NovaStrap - Important Notice")
        self.setModal(True)
        self.setMinimumWidth(550)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #00d9ff;
                color: #000000;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b8e6;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # NovaStrap branding
        brand_label = QLabel("NovaStrap")
        brand_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00d9ff;
            padding-bottom: 5px;
        """)
        layout.addWidget(brand_label)
        
        credit_label = QLabel("Made by Nova")
        credit_label.setStyleSheet("""
            font-size: 10px;
            color: #888888;
            font-style: italic;
            padding-bottom: 15px;
        """)
        layout.addWidget(credit_label)
        
        # Disclaimer text
        disclaimer = QLabel(
            "<h3 style='color: #00d9ff;'>⚠️ Important Disclaimer</h3>"
            "<p>This tool modifies Roblox client configuration files. Please note:</p>"
            "<ul>"
            "<li>Modifying FFlags may violate Roblox Terms of Service</li>"
            "<li>Incorrect FFlags can cause client instability or crashes</li>"
            "<li>Always backup your settings before making changes</li>"
            "<li>Close Roblox completely before applying changes</li>"
            "<li>Use at your own risk - this tool is provided AS-IS</li>"
            "</ul>"
            "<p><b>By continuing, you acknowledge these risks.</b></p>"
        )
        disclaimer.setWordWrap(True)
        disclaimer.setStyleSheet("color: #cccccc;")
        layout.addWidget(disclaimer)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)


class BackupDialog(QDialog):
    """Dialog to select and restore a backup."""
    
    def __init__(self, backups, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NovaStrap - Restore Backup")
        self.setModal(True)
        self.setMinimumSize(650, 450)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
        """)
        
        self.selected_backup = None
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Info label
        info = QLabel("<b style='color: #00d9ff;'>Select a backup to restore:</b>")
        layout.addWidget(info)
        
        # List of backups
        self.backup_list = QListWidget()
        for backup in backups:
            self.backup_list.addItem(backup.name)
        layout.addWidget(self.backup_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet("""
            QPushButton {
                background-color: #00d9ff;
                color: #000000;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b8e6;
            }
        """)
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.backups = backups
    
    def accept(self):
        """Accept and store selected backup."""
        current_row = self.backup_list.currentRow()
        if current_row >= 0:
            self.selected_backup = self.backups[current_row]
        super().accept()


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.path_manager = PathManager()
        self.file_manager = None
        self.logger = AppLogger()
        self.validator = JsonValidator()
        
        # Setup UI
        self.setWindowTitle("NovaStrap")
        self.setMinimumSize(900, 700)
        
        # Show disclaimer on first run
        if not self.show_disclaimer():
            sys.exit(0)
        
        # Initialize paths
        if not self.initialize_paths():
            QMessageBox.critical(
                self,
                "Error",
                "Failed to resolve Roblox paths. Ensure Roblox is installed."
            )
            sys.exit(1)
        
        self.setup_ui()
        self.setup_status_checker()
        self.load_existing_content()
        
        self.logger.info("Application started")
    
    def show_disclaimer(self) -> bool:
        """Show disclaimer dialog."""
        dialog = DisclaimerDialog(self)
        return dialog.exec() == QDialog.DialogCode.Accepted
    
    def initialize_paths(self) -> bool:
        """Initialize and resolve all paths."""
        if not self.path_manager.resolve_paths():
            return False
        
        if not self.path_manager.ensure_client_settings_exists():
            return False
        
        self.file_manager = FileManager(self.path_manager.target_file)
        return True
    
    def setup_ui(self):
        """Setup the user interface."""
        # Apply modern dark theme
        self.apply_dark_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        central_widget.setLayout(main_layout)
        
        # Header section with branding
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # NovaStrap branding
        brand_label = QLabel("NovaStrap")
        brand_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #00d9ff;
                padding: 10px 0;
                letter-spacing: 2px;
            }
        """)
        header_layout.addWidget(brand_label)
        
        # Made by Nova
        credit_label = QLabel("Made by Nova")
        credit_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #888888;
                font-style: italic;
                padding-bottom: 10px;
            }
        """)
        header_layout.addWidget(credit_label)
        
        main_layout.addLayout(header_layout)
        
        # Top info section with modern styling
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        # Path display with modern card style
        path_container = QWidget()
        path_container.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 12px;
                border: 1px solid #2a2a2a;
            }
        """)
        path_layout = QVBoxLayout(path_container)
        path_layout.setContentsMargins(0, 0, 0, 0)
        
        path_label = QLabel(f"<b style='color: #00d9ff;'>Target File:</b> <span style='color: #cccccc;'>{self.path_manager.get_target_file_str()}</span>")
        path_label.setWordWrap(True)
        path_layout.addWidget(path_label)
        
        info_layout.addWidget(path_container)
        
        # Status row with modern styling
        status_container = QWidget()
        status_container.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 12px;
                border: 1px solid #2a2a2a;
            }
        """)
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #cccccc;")
        self.roblox_status_label = QLabel()
        self.update_roblox_status()
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.roblox_status_label)
        
        info_layout.addWidget(status_container)
        main_layout.addLayout(info_layout)
        
        # Editor label and search bar
        editor_header_layout = QHBoxLayout()
        
        editor_label = QLabel("Paste your JSON FFlags here:")
        editor_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #00d9ff;
                padding-top: 10px;
            }
        """)
        editor_header_layout.addWidget(editor_label)
        
        editor_header_layout.addStretch()
        
        # Search functionality
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(8)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search FFlags...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 2px solid #2a2a2a;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                min-width: 200px;
            }
            QLineEdit:focus {
                border-color: #00d9ff;
            }
        """)
        self.search_input.returnPressed.connect(self.search_next)
        search_layout.addWidget(self.search_input)
        
        self.find_next_btn = QPushButton("▼ Next")
        self.find_next_btn.clicked.connect(self.search_next)
        self.find_next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #00d9ff;
            }
        """)
        search_layout.addWidget(self.find_next_btn)
        
        self.find_prev_btn = QPushButton("▲ Prev")
        self.find_prev_btn.clicked.connect(self.search_previous)
        self.find_prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                color: #00d9ff;
            }
        """)
        search_layout.addWidget(self.find_prev_btn)
        
        self.search_count_label = QLabel("")
        self.search_count_label.setStyleSheet("color: #888888; font-size: 11px; padding-left: 8px;")
        search_layout.addWidget(self.search_count_label)
        
        editor_header_layout.addWidget(search_container)
        
        main_layout.addLayout(editor_header_layout)
        
        # JSON editor with modern dark theme
        self.editor = QTextEdit()
        self.editor.setPlaceholderText(
            "{\n"
            '  "FFlagSomeFeature": "True",\n'
            '  "DFIntSomeValue": "0"\n'
            "}"
        )
        
        # Set monospaced font
        font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)
        self.editor.setFont(font)
        
        # Modern editor styling
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #0d0d0d;
                color: #e0e0e0;
                border: 2px solid #2a2a2a;
                border-radius: 8px;
                padding: 15px;
                selection-background-color: #00d9ff;
                selection-color: #000000;
            }
            QTextEdit:focus {
                border: 2px solid #00d9ff;
            }
        """)
        
        # Enable line wrap off for better JSON viewing
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        main_layout.addWidget(self.editor, stretch=1)
        
        # Validation status with modern styling
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 6px;
                font-size: 12px;
            }
        """)
        main_layout.addWidget(self.validation_label)
        
        # Primary action buttons (Save & Launch)
        primary_button_layout = QHBoxLayout()
        primary_button_layout.setSpacing(15)
        
        self.save_btn = QPushButton("💾 Save & Apply")
        self.save_btn.clicked.connect(self.save_and_apply)
        self.style_button(self.save_btn, primary=True)
        primary_button_layout.addWidget(self.save_btn)
        
        self.launch_btn = QPushButton("🚀 Launch Roblox")
        self.launch_btn.clicked.connect(self.launch_roblox)
        self.style_button(self.launch_btn, launch=True)
        primary_button_layout.addWidget(self.launch_btn)
        
        main_layout.addLayout(primary_button_layout)
        
        # Secondary action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.validate_btn = QPushButton("🔍 Validate")
        self.validate_btn.clicked.connect(self.validate_json)
        self.style_button(self.validate_btn, secondary=True)
        button_layout.addWidget(self.validate_btn)
        
        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.clicked.connect(self.clear_editor)
        self.style_button(self.clear_btn, secondary=True)
        button_layout.addWidget(self.clear_btn)
        
        self.import_btn = QPushButton("📁 Import")
        self.import_btn.clicked.connect(self.import_file)
        self.style_button(self.import_btn, secondary=True)
        button_layout.addWidget(self.import_btn)
        
        self.export_btn = QPushButton("💾 Export")
        self.export_btn.clicked.connect(self.export_file)
        self.style_button(self.export_btn, secondary=True)
        button_layout.addWidget(self.export_btn)
        
        self.restore_btn = QPushButton("⏮️ Restore")
        self.restore_btn.clicked.connect(self.restore_backup)
        self.style_button(self.restore_btn, secondary=True)
        button_layout.addWidget(self.restore_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status bar with modern styling
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background-color: #0a0a0a;
                color: #888888;
                border-top: 1px solid #2a2a2a;
                padding: 5px;
            }
        """)
        self.statusBar.showMessage("Ready")
        
        # Connect editor changes to clear validation and update search
        self.editor.textChanged.connect(self.on_editor_changed)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        # Initialize search state
        self.current_search_matches = []
        self.current_match_index = -1
    
    def apply_dark_theme(self):
        """Apply modern dark theme to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QMessageBox {
                background-color: #1a1a1a;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
            }
            QDialog {
                background-color: #1a1a1a;
            }
            QListWidget {
                background-color: #0d0d0d;
                color: #e0e0e0;
                border: 2px solid #2a2a2a;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #00d9ff;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #0d0d0d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #2a2a2a;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3a3a3a;
            }
            QScrollBar:horizontal {
                background-color: #0d0d0d;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #2a2a2a;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #3a3a3a;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }
        """)
    
    def style_button(self, button, primary=False, secondary=False, launch=False):
        """Apply modern styling to buttons."""
        if primary:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #00d9ff;
                    color: #000000;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #00b8e6;
                }
                QPushButton:pressed {
                    background-color: #0099cc;
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    color: #666666;
                }
            """)
        elif launch:
            button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #00ff88, stop:1 #00d9ff);
                    color: #000000;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #00e67a, stop:1 #00b8e6);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #00cc6f, stop:1 #0099cc);
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    color: #666666;
                }
            """)
        elif secondary:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 2px solid #2a2a2a;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-weight: 500;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2a2a2a;
                    border-color: #00d9ff;
                    color: #00d9ff;
                }
                QPushButton:pressed {
                    background-color: #0d0d0d;
                }
                QPushButton:disabled {
                    background-color: #0d0d0d;
                    color: #666666;
                    border-color: #1a1a1a;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: #e0e0e0;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
                QPushButton:pressed {
                    background-color: #1a1a1a;
                }
            """)
    
    def setup_status_checker(self):
        """Setup timer to periodically check Roblox status."""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_roblox_status)
        self.status_timer.start(3000)  # Check every 3 seconds
    
    def update_roblox_status(self):
        """Update Roblox process status display."""
        is_running = ProcessWatcher.is_roblox_running()
        if is_running:
            self.roblox_status_label.setText("⚠️ <b style='color: #ff4444;'>Roblox Running</b>")
            self.roblox_status_label.setToolTip(
                "Warning: Roblox is currently running.\n"
                "Close it before saving for changes to take effect."
            )
        else:
            self.roblox_status_label.setText("✓ <b style='color: #00d9ff;'>Roblox Not Running</b>")
            self.roblox_status_label.setToolTip("Roblox is not running")
    
    def load_existing_content(self):
        """Load existing content from target file if it exists."""
        content = self.file_manager.read_current_content()
        if content:
            try:
                # Format the JSON for display
                formatted = self.validator.format_json(content)
                self.editor.setPlainText(formatted)
                self.logger.info("Loaded existing IxpSettings.json content")
            except Exception:
                self.editor.setPlainText(content)
    
    def on_editor_changed(self):
        """Handle editor text changes."""
        # Clear validation message when user types
        self.validation_label.setText("")
        self.validation_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 6px;
                font-size: 12px;
            }
        """)
        # Reset search when content changes
        if hasattr(self, 'search_input') and self.search_input.text():
            self.highlight_all_matches()
    
    def on_search_changed(self):
        """Handle search input changes."""
        self.highlight_all_matches()
    
    def highlight_all_matches(self):
        """Highlight all search matches in the editor."""
        search_text = self.search_input.text()
        
        if not search_text:
            # Clear highlights
            self.editor.setExtraSelections([])
            self.search_count_label.setText("")
            self.current_search_matches = []
            self.current_match_index = -1
            return
        
        # Get editor content
        content = self.editor.toPlainText()
        
        # Find all matches (case-insensitive)
        self.current_search_matches = []
        search_lower = search_text.lower()
        start = 0
        
        while True:
            index = content.lower().find(search_lower, start)
            if index == -1:
                break
            self.current_search_matches.append(index)
            start = index + 1
        
        # Create extra selections for highlights
        extra_selections = []
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("#00d9ff"))
        highlight_format.setForeground(QColor("#000000"))
        
        for match_pos in self.current_search_matches:
            selection = QTextEdit.ExtraSelection()
            cursor = self.editor.textCursor()
            cursor.setPosition(match_pos)
            cursor.movePosition(QTextCursor.MoveOperation.Right, 
                              QTextCursor.MoveMode.KeepAnchor, 
                              len(search_text))
            selection.cursor = cursor
            selection.format = highlight_format
            extra_selections.append(selection)
        
        # Apply all highlights
        self.editor.setExtraSelections(extra_selections)
        
        # Update count label
        if self.current_search_matches:
            self.search_count_label.setText(f"{len(self.current_search_matches)} found")
            self.current_match_index = 0
            self.jump_to_match(0)
        else:
            self.search_count_label.setText("Not found")
            self.current_match_index = -1
    
    def search_next(self):
        """Jump to next search match."""
        if not self.current_search_matches:
            return
        
        self.current_match_index = (self.current_match_index + 1) % len(self.current_search_matches)
        self.jump_to_match(self.current_match_index)
        self.update_search_position_label()
    
    def search_previous(self):
        """Jump to previous search match."""
        if not self.current_search_matches:
            return
        
        self.current_match_index = (self.current_match_index - 1) % len(self.current_search_matches)
        self.jump_to_match(self.current_match_index)
        self.update_search_position_label()
    
    def jump_to_match(self, index):
        """Jump to a specific match index."""
        if index < 0 or index >= len(self.current_search_matches):
            return
        
        match_pos = self.current_search_matches[index]
        search_text = self.search_input.text()
        
        # Create cursor and move to the match
        cursor = self.editor.textCursor()
        cursor.setPosition(match_pos)
        cursor.movePosition(QTextCursor.MoveOperation.Right, 
                          QTextCursor.MoveMode.KeepAnchor, 
                          len(search_text))
        
        # Set the cursor (this will scroll to it)
        self.editor.setTextCursor(cursor)
        
        # Ensure it's visible
        self.editor.ensureCursorVisible()
    
    def update_search_position_label(self):
        """Update the search position label."""
        if self.current_search_matches:
            self.search_count_label.setText(
                f"{self.current_match_index + 1}/{len(self.current_search_matches)}"
            )
    
    def validate_json(self):
        """Validate JSON in editor."""
        text = self.editor.toPlainText()
        is_valid, error_msg, data = self.validator.validate(text)
        
        if is_valid:
            self.validation_label.setText("✓ <span style='color: #00d9ff; font-weight: bold;'>Valid JSON</span>")
            self.validation_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 217, 255, 0.1);
                    border: 1px solid #00d9ff;
                    border-radius: 6px;
                    padding: 8px;
                }
            """)
            self.statusBar.showMessage("✓ JSON is valid", 3000)
            self.logger.info("JSON validation passed")
        else:
            self.validation_label.setText(f"✗ <span style='color: #ff4444; font-weight: bold;'>{error_msg}</span>")
            self.validation_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 68, 68, 0.1);
                    border: 1px solid #ff4444;
                    border-radius: 6px;
                    padding: 8px;
                }
            """)
            self.statusBar.showMessage("✗ JSON validation failed", 3000)
            self.logger.warning(f"JSON validation failed: {error_msg}")
        
        return is_valid, error_msg, data
    
    def save_and_apply(self):
        """Save JSON to target file and apply settings."""
        # Validate first
        is_valid, error_msg, data = self.validate_json()
        if not is_valid:
            QMessageBox.warning(
                self,
                "Validation Error",
                f"Cannot save invalid JSON:\n\n{error_msg}"
            )
            return
        
        # Check if Roblox is running
        if ProcessWatcher.is_roblox_running():
            reply = QMessageBox.question(
                self,
                "Roblox Running",
                "Roblox is currently running. Changes will not take effect until you restart Roblox.\n\n"
                "It's recommended to close Roblox before saving.\n\n"
                "Continue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        try:
            # Create backup
            backup = self.file_manager.backup_file()
            if backup:
                self.logger.info(f"Created backup: {backup.name}")
            
            # Write file atomically
            self.file_manager.atomic_write_json(data)
            self.logger.info("Wrote JSON to target file")
            
            # Set read-only
            self.file_manager.set_readonly()
            self.logger.success("Set file to read-only")
            
            # Update status
            self.statusBar.showMessage("✓ Saved and applied successfully!", 5000)
            self.status_label.setText(f"Status: Saved successfully at {self.get_timestamp()}")
            
            QMessageBox.information(
                self,
                "Success",
                "FFlags saved successfully!\n\n"
                f"File: {self.path_manager.target_file}\n"
                "Attribute: Read-Only\n\n"
                "Restart Roblox for changes to take effect."
            )
            
        except Exception as e:
            error_text = str(e)
            self.logger.error(f"Save failed: {error_text}")
            self.statusBar.showMessage("✗ Save failed", 5000)
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save file:\n\n{error_text}"
            )
    
    def clear_editor(self):
        """Clear the editor content."""
        reply = QMessageBox.question(
            self,
            "Clear Editor",
            "Are you sure you want to clear the editor?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.editor.clear()
            self.validation_label.setText("")
            self.logger.info("Editor cleared")
    
    def import_file(self):
        """Import JSON from file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import JSON",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Validate before importing
                is_valid, error_msg, data = self.validator.validate(content)
                if not is_valid:
                    QMessageBox.warning(
                        self,
                        "Invalid JSON",
                        f"The selected file contains invalid JSON:\n\n{error_msg}"
                    )
                    return
                
                # Format and load
                formatted = self.validator.format_json(content)
                self.editor.setPlainText(formatted)
                self.logger.info(f"Imported JSON from: {file_path}")
                self.statusBar.showMessage("✓ Imported successfully", 3000)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Import Error",
                    f"Failed to import file:\n\n{str(e)}"
                )
                self.logger.error(f"Import failed: {str(e)}")
    
    def export_file(self):
        """Export current editor content to file."""
        # Validate first
        is_valid, error_msg, data = self.validate_json()
        if not is_valid:
            reply = QMessageBox.question(
                self,
                "Export Invalid JSON?",
                "The current content is not valid JSON. Export anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export JSON",
            "IxpSettings.json",
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            try:
                content = self.editor.toPlainText()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.logger.info(f"Exported JSON to: {file_path}")
                self.statusBar.showMessage("✓ Exported successfully", 3000)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export file:\n\n{str(e)}"
                )
                self.logger.error(f"Export failed: {str(e)}")
    
    def restore_backup(self):
        """Restore from a previous backup."""
        backups = self.file_manager.get_backup_files()
        
        if not backups:
            QMessageBox.information(
                self,
                "No Backups",
                "No backup files found."
            )
            return
        
        # Show backup selection dialog
        dialog = BackupDialog(backups, self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_backup:
            try:
                # Restore the backup
                self.file_manager.restore_backup(dialog.selected_backup)
                
                # Reload content
                self.load_existing_content()
                
                # Set read-only again
                self.file_manager.set_readonly()
                
                self.logger.success(f"Restored backup: {dialog.selected_backup.name}")
                self.statusBar.showMessage("✓ Backup restored successfully", 5000)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Backup restored successfully:\n\n{dialog.selected_backup.name}"
                )
                
            except Exception as e:
                self.logger.error(f"Restore failed: {str(e)}")
                QMessageBox.critical(
                    self,
                    "Restore Error",
                    f"Failed to restore backup:\n\n{str(e)}"
                )
    
    def launch_roblox(self):
        """Launch Roblox with current settings."""
        # Check if there are unsaved changes
        text = self.editor.toPlainText().strip()
        
        if text:
            # Ask user if they want to save first
            reply = QMessageBox.question(
                self,
                "Save Settings?",
                "Would you like to save your FFlags before launching Roblox?\n\n"
                "Select 'Yes' to save and launch\n"
                "Select 'No' to launch without saving\n"
                "Select 'Cancel' to abort",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                # Validate and save first
                is_valid, error_msg, data = self.validate_json()
                if not is_valid:
                    retry = QMessageBox.question(
                        self,
                        "Invalid JSON",
                        f"Your JSON is invalid:\n\n{error_msg}\n\n"
                        "Launch Roblox anyway without saving?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if retry == QMessageBox.StandardButton.No:
                        return
                else:
                    # Save the settings
                    try:
                        backup = self.file_manager.backup_file()
                        if backup:
                            self.logger.info(f"Created backup: {backup.name}")
                        
                        self.file_manager.atomic_write_json(data)
                        self.file_manager.set_readonly()
                        self.logger.success("Saved settings before launch")
                        self.statusBar.showMessage("✓ Settings saved", 3000)
                    except Exception as e:
                        QMessageBox.warning(
                            self,
                            "Save Failed",
                            f"Failed to save settings:\n\n{str(e)}\n\nLaunching anyway..."
                        )
        
        # Check if Roblox is already running
        if ProcessWatcher.is_roblox_running():
            reply = QMessageBox.question(
                self,
                "Roblox Already Running",
                "Roblox is already running. Your new settings won't take effect until you restart Roblox.\n\n"
                "Would you like to continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Launch Roblox
        self.statusBar.showMessage("Launching Roblox...", 2000)
        success, message = RobloxLauncher.launch_roblox()
        
        if success:
            self.logger.success(f"Launched Roblox: {message}")
            self.statusBar.showMessage(f"✓ {message}", 5000)
            QMessageBox.information(
                self,
                "Roblox Launched",
                f"{message}\n\n"
                "Your FFlags are now active!\n"
                "Enjoy your enhanced Roblox experience."
            )
        else:
            self.logger.error(f"Launch failed: {message}")
            self.statusBar.showMessage("✗ Launch failed", 5000)
            QMessageBox.critical(
                self,
                "Launch Failed",
                f"Failed to launch Roblox:\n\n{message}\n\n"
                "Please make sure Roblox is installed in the default location."
            )
    
    def get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.logger.info("Application closed")
        event.accept()


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("NovaStrap")
    app.setOrganizationName("Nova")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

