"""
Application class for Kun text editor.
"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import sys


class KunApplication(QApplication):
    """Main application class for Kun."""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application metadata
        self.setApplicationName("Kun")
        self.setApplicationDisplayName("Kun Text Editor")
        self.setOrganizationName("Kun")
        self.setApplicationVersion("1.0.0")
        
        # Enable high DPI scaling
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            self.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            self.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
