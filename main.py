"""
Main entry point for Kun text editor.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import KunApplication
from ui.main_window import MainWindow


def main():
    """Main entry point."""
    app = KunApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    window.show()
    
    # Open files passed as command line arguments
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.endswith('.txt'):
                window.open_file_path(arg)
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
