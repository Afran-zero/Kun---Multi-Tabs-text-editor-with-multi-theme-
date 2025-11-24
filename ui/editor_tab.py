"""
Editor tab component for Kun text editor.
Provides text editing widget with line numbers and spell checking.
"""
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import QTextCursor, QTextFormat, QColor, QPainter, QTextCharFormat, QFont
from typing import Optional


class LineNumberArea(QWidget):
    """Widget for displaying line numbers."""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class EditorTab(QPlainTextEdit):
    """
    Enhanced text editor with spell checking and line numbers.
    """
    
    # Signals
    text_changed_signal = pyqtSignal()
    cursor_position_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Properties
        self.file_path: Optional[str] = None
        self.is_modified = False
        self.custom_tab_name: Optional[str] = None
        self.show_line_numbers = False
        self.spell_checker = None
        self.misspelled_words = []
        
        # Line number area
        self.line_number_area = LineNumberArea(self)
        
        # Connect signals
        self.textChanged.connect(self.on_text_changed)
        self.cursorPositionChanged.connect(self.on_cursor_changed)
        
        # Font settings
        self.current_font_family = "Consolas"
        self.current_font_size = 11
        self.current_font_bold = False
        self.current_font_italic = False
        self.current_font_underline = False
        self.current_text_color = QColor("#e0e0e0")
        
        self.apply_font_settings()
    
    def on_text_changed(self):
        """Handle text changes."""
        self.is_modified = True
        self.text_changed_signal.emit()
        
        # Update line numbers
        if self.show_line_numbers:
            self.update_line_number_area_width()
            self.update_line_number_area()
        
        # Update spell checking (disabled by default to prevent performance issues)
        # Uncomment to enable real-time spell checking:
        # if self.spell_checker and self.spell_checker.is_enabled():
        #     self.check_spelling()
    
    def on_cursor_changed(self):
        """Handle cursor position changes."""
        self.cursor_position_changed.emit()
    
    def get_content(self) -> str:
        """Get editor content."""
        return self.toPlainText()
    
    def set_content(self, content: str):
        """Set editor content."""
        self.setPlainText(content)
        self.is_modified = False
    
    def get_cursor_position(self) -> int:
        """Get current cursor position."""
        return self.textCursor().position()
    
    def set_file_path(self, path: str):
        """Set associated file path."""
        self.file_path = path
        self.is_modified = False
    
    def get_file_path(self) -> Optional[str]:
        """Get associated file path."""
        return self.file_path
    
    def set_custom_name(self, name: str):
        """Set custom tab name (doesn't affect file name)."""
        self.custom_tab_name = name
    
    def get_display_name(self) -> str:
        """Get display name for tab."""
        if self.custom_tab_name:
            return self.custom_tab_name
        if self.file_path:
            return self.file_path.split('/')[-1].split('\\')[-1]
        return "Untitled"
    
    def mark_saved(self):
        """Mark document as saved."""
        self.is_modified = False
    
    def apply_font_settings(self):
        """Apply current font settings to editor."""
        font = QFont(self.current_font_family, self.current_font_size)
        font.setBold(self.current_font_bold)
        font.setItalic(self.current_font_italic)
        font.setUnderline(self.current_font_underline)
        
        self.setFont(font)
        self.setStyleSheet(f"color: {self.current_text_color.name()};")
    
    def set_font_family(self, family: str):
        """Set font family."""
        self.current_font_family = family
        self.apply_font_settings()
    
    def set_font_size(self, size: int):
        """Set font size."""
        self.current_font_size = size
        self.apply_font_settings()
    
    def set_font_bold(self, bold: bool):
        """Set bold style."""
        self.current_font_bold = bold
        self.apply_font_settings()
    
    def set_font_italic(self, italic: bool):
        """Set italic style."""
        self.current_font_italic = italic
        self.apply_font_settings()
    
    def set_font_underline(self, underline: bool):
        """Set underline style."""
        self.current_font_underline = underline
        self.apply_font_settings()
    
    def set_text_color(self, color: QColor):
        """Set text color."""
        self.current_text_color = color
        self.apply_font_settings()
    
    def set_spell_checker(self, checker):
        """Set spell checker instance."""
        self.spell_checker = checker
        if checker and checker.is_enabled():
            self.check_spelling()
    
    def check_spelling(self):
        """Check spelling and highlight misspelled words."""
        if not self.spell_checker or not self.spell_checker.is_enabled():
            return
        
        text = self.get_content()
        self.misspelled_words = self.spell_checker.find_misspelled_words(text)
        
        # Highlight misspelled words
        self.highlight_misspelled_words()
    
    def highlight_misspelled_words(self):
        """Highlight misspelled words with red underline."""
        # Clear previous highlights
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        
        # Create format for misspelled words
        error_format = QTextCharFormat()
        error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        error_format.setUnderlineColor(QColor("#cc0000"))
        
        # Apply highlights
        for word, start, end in self.misspelled_words:
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            cursor.mergeCharFormat(error_format)
    
    def set_show_line_numbers(self, show: bool):
        """Toggle line number display."""
        self.show_line_numbers = show
        if show:
            self.update_line_number_area_width()
            self.line_number_area.show()
        else:
            self.setViewportMargins(0, 0, 0, 0)
            self.line_number_area.hide()
    
    def line_number_area_width(self) -> int:
        """Calculate width needed for line numbers."""
        if not self.show_line_numbers:
            return 0
        
        digits = len(str(max(1, self.document().blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self):
        """Update left margin for line numbers."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect=None, dy=0):
        """Update line number area when scrolling."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y() if rect else 0, 
                                        self.line_number_area.width(),
                                        rect.height() if rect else self.line_number_area.height())
        
        if rect and rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()
    
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        
        if self.show_line_numbers:
            cr = self.contentsRect()
            self.line_number_area.setGeometry(
                QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
            )
    
    def line_number_area_paint_event(self, event):
        """Paint line numbers."""
        if not self.show_line_numbers:
            return
        
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#1a1a1a"))
        painter.setPen(QColor("#808080"))
        
        # Get the first visible block
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        
        # Get the top position of the first visible block
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        
        # Draw line numbers for all visible blocks
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 5,
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
