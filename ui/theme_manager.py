"""
Theme management module for Kun text editor.
Loads and applies visual themes from JSON files.
"""
import json
from pathlib import Path
from typing import Dict, Optional


class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self, themes_dir: str = None):
        if themes_dir is None:
            themes_dir = Path(__file__).parent.parent / "assets" / "themes"
        self.themes_dir = Path(themes_dir)
        self.current_theme = None
        self.available_themes = self.load_available_themes()
    
    def load_available_themes(self) -> Dict[str, dict]:
        """Load all available theme files."""
        themes = {}
        if not self.themes_dir.exists():
            return themes
        
        for theme_file in self.themes_dir.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                    theme_id = theme_file.stem
                    themes[theme_id] = theme_data
            except Exception as e:
                print(f"Error loading theme {theme_file}: {e}")
        
        return themes
    
    def get_theme(self, theme_id: str) -> Optional[dict]:
        """Get theme data by ID."""
        return self.available_themes.get(theme_id)
    
    def set_current_theme(self, theme_id: str) -> bool:
        """Set the current active theme."""
        theme = self.get_theme(theme_id)
        if theme:
            self.current_theme = theme
            return True
        return False
    
    def get_current_theme(self) -> Optional[dict]:
        """Get the currently active theme."""
        return self.current_theme
    
    def get_theme_names(self) -> list:
        """Get list of available theme names."""
        return [theme.get('name', tid) for tid, theme in self.available_themes.items()]
    
    def get_theme_ids(self) -> list:
        """Get list of available theme IDs."""
        return list(self.available_themes.keys())
    
    def generate_stylesheet(self, theme: dict = None) -> str:
        """Generate Qt stylesheet from theme data."""
        if theme is None:
            theme = self.current_theme
        
        if not theme:
            return ""
        
        colors = theme.get('colors', {})
        
        # Check if theme has glass effects
        has_glass = theme.get('effects', {}).get('glass', False)
        
        stylesheet = f"""
            QMainWindow {{
                background-color: {colors.get('window_bg', '#1a1a1a')};
            }}
            
            QTextEdit, QPlainTextEdit {{
                background-color: {colors.get('editor_bg', '#0d0d0d')};
                color: {colors.get('editor_fg', '#e0e0e0')};
                border: 1px solid {colors.get('border', '#2a2a2a')};
                border-radius: {'6px' if has_glass else '2px'};
                selection-background-color: {colors.get('selection_bg', '#404040')};
                selection-color: {colors.get('selection_fg', '#ffffff')};
                font-family: {theme.get('font', {}).get('family', 'Consolas')};
                font-size: {theme.get('font', {}).get('size', 11)}pt;
                padding: {'4px' if has_glass else '2px'};
            }}
            
            QTabWidget::pane {{
                border: none;
                background-color: {colors.get('window_bg', '#1a1a1a')};
            }}
            
            QTabBar::tab {{
                background-color: {colors.get('tab_inactive_bg', '#1a1a1a')};
                color: {colors.get('tab_text', '#c0c0c0')};
                padding: 8px 16px;
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.1)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
                border-bottom: none;
                border-top-left-radius: {'8px' if has_glass else '4px'};
                border-top-right-radius: {'8px' if has_glass else '4px'};
                margin-right: 2px;
                margin-top: {'2px' if has_glass else '0px'};
            }}
            
            QTabBar::tab:selected {{
                background-color: {colors.get('tab_active_bg', '#2a2a2a')};
                color: {colors.get('tab_text_active', '#ffffff')};
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.2)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
                border-bottom: none;
                padding-bottom: {'10px' if has_glass else '8px'};
            }}
            
            QTabBar::tab:hover {{
                background-color: {colors.get('button_hover_bg', '#3a3a3a')};
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.25)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
                border-bottom: none;
            }}
            
            QStatusBar {{
                background-color: {colors.get('status_bar_bg', '#0d0d0d')};
                color: {colors.get('status_bar_fg', '#808080')};
                border-top: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.1)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
            }}
            
            QMenuBar {{
                background-color: {colors.get('menu_bg', '#1a1a1a')};
                color: {colors.get('menu_fg', '#e0e0e0')};
                padding: 4px;
                border-bottom: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.12)') if has_glass else 'none'};
            }}
            
            QMenuBar::item {{
                background-color: transparent;
                padding: 4px 12px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {colors.get('menu_hover_bg', '#2a2a2a')};
            }}
            
            QMenu {{
                background-color: {colors.get('menu_bg', '#1a1a1a')};
                color: {colors.get('menu_fg', '#e0e0e0')};
                border: 1px solid {colors.get('border', '#2a2a2a')};
            }}
            
            QMenu::item {{
                padding: 6px 24px;
            }}
            
            QMenu::item:selected {{
                background-color: {colors.get('menu_hover_bg', '#2a2a2a')};
            }}
            
            QPushButton, QToolButton {{
                background-color: {colors.get('button_bg', '#2a2a2a')};
                color: {colors.get('button_fg', '#e0e0e0')};
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.15)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
                padding: 6px 12px;
                border-radius: {'8px' if has_glass else '3px'};
                font-weight: {'bold' if has_glass else 'normal'};
                min-height: {'22px' if has_glass else '18px'};
            }}
            
            QPushButton:hover, QToolButton:hover {{
                background-color: {colors.get('button_hover_bg', '#3a3a3a')};
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.3)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
            }}
            
            QPushButton:pressed, QToolButton:pressed {{
                background-color: {colors.get('highlight', '#4a4a4a')};
                border: {'2px solid ' + colors.get('glass_shine', 'rgba(255,255,255,0.35)') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
            }}
            
            QLineEdit {{
                background-color: {colors.get('editor_bg', '#0d0d0d')};
                color: {colors.get('editor_fg', '#e0e0e0')};
                border: {'2px solid ' + colors.get('border', '#2a2a2a') if has_glass else '1px solid ' + colors.get('border', '#2a2a2a')};
                padding: {'6px' if has_glass else '4px'};
                border-radius: {'6px' if has_glass else '2px'};
                selection-background-color: {colors.get('selection_bg', '#404040')};
            }}
            
            QLineEdit:focus {{
                border: {'2px solid ' + colors.get('accent', colors.get('selection_bg', '#404040')) if has_glass else '2px solid ' + colors.get('selection_bg', '#404040')};
            }}
            
            QLabel {{
                color: {colors.get('menu_fg', '#e0e0e0')};
            }}
            
            QDialog {{
                background-color: {colors.get('window_bg', '#1a1a1a')};
            }}
            
            QComboBox {{
                background-color: {colors.get('button_bg', '#2a2a2a')};
                color: {colors.get('button_fg', '#e0e0e0')};
                border: 1px solid {colors.get('border', '#2a2a2a')};
                padding: 4px;
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {colors.get('menu_bg', '#1a1a1a')};
                color: {colors.get('menu_fg', '#e0e0e0')};
                selection-background-color: {colors.get('selection_bg', '#404040')};
            }}
            
            QSpinBox {{
                background-color: {colors.get('editor_bg', '#0d0d0d')};
                color: {colors.get('editor_fg', '#e0e0e0')};
                border: 1px solid {colors.get('border', '#2a2a2a')};
                padding: 4px;
            }}
            
            QCheckBox {{
                color: {colors.get('menu_fg', '#e0e0e0')};
                spacing: 8px;
            }}
            
            QRadioButton {{
                color: {colors.get('menu_fg', '#e0e0e0')};
                spacing: 8px;
            }}
        """
        
        return stylesheet
    
    def get_color(self, color_key: str, default: str = '#000000') -> str:
        """Get a specific color from current theme."""
        if not self.current_theme:
            return default
        return self.current_theme.get('colors', {}).get(color_key, default)
