"""
Main window for Kun text editor.
Contains menu bar, tab widget, and status bar.
"""
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QMenuBar, QMenu, QStatusBar,
                             QFileDialog, QMessageBox, QInputDialog, QDialog, QVBoxLayout,
                             QHBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton,
                             QCheckBox, QColorDialog, QLineEdit, QRadioButton, QButtonGroup, QWidget)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QAction, QKeySequence, QFont, QColor, QDragEnterEvent, QDropEvent, QTextCursor
import os
from pathlib import Path

from ui.editor_tab import EditorTab
from ui.theme_manager import ThemeManager
from core.file_ops import FileOperations
from core.text_analyzer import TextAnalyzer
from core.spell_checker import BasicSpellChecker


class FindReplaceDialog(QDialog):
    """Dialog for Find & Replace functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find and Replace")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Find field
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)
        
        # Replace field
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)
        
        # Options
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_words = QCheckBox("Match whole words")
        self.wrap_around = QCheckBox("Wrap around")
        self.wrap_around.setChecked(True)
        
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.whole_words)
        layout.addWidget(self.wrap_around)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.find_prev_btn = QPushButton("Find Previous")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        
        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.find_prev_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Kun")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize managers
        self.file_ops = FileOperations()
        self.theme_manager = ThemeManager()
        self.spell_checker = BasicSpellChecker()
        self.text_analyzer = TextAnalyzer()
        
        # Untitled counter
        self.untitled_counter = 1
        
        # Find state
        self.find_matches = []
        self.current_match_index = -1
        self.find_widget = None
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_all)
        
        # Character count mode
        self.char_count_with_spaces = self.file_ops.get_setting('char_count_mode', 'with_spaces') == 'with_spaces'
        
        # Setup UI
        self.setup_ui()
        self.setup_menus()
        self.setup_status_bar()
        self.apply_theme(self.file_ops.get_setting('theme', 'noir'))
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Restore session
        if self.file_ops.get_setting('restore_session', True):
            self.restore_session()
        
        # Create initial tab if none exist
        if self.tab_widget.count() == 0:
            self.new_tab()
    
    def setup_ui(self):
        """Setup main UI components."""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        
        # Connect tab signals
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)
        
        # Add '+' button for new tabs
        from PyQt6.QtWidgets import QPushButton
        self.new_tab_button = QPushButton("+")
        self.new_tab_button.setToolTip("New Tab (Ctrl+T)")
        self.new_tab_button.clicked.connect(self.new_tab)
        self.new_tab_button.setFixedSize(28, 28)
        self.new_tab_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_tab_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #aaa;
                border-radius: 4px;
                padding: 0px;
                margin: 2px 4px 2px 2px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #fff;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.18);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """)
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.Corner.TopRightCorner)
        
        self.setCentralWidget(self.tab_widget)
    
    def setup_menus(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("New Tab", self)
        new_action.setShortcut(QKeySequence("Ctrl+T"))
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Open Recent submenu
        self.recent_menu = file_menu.addMenu("Open Recent")
        self.update_recent_menu()
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        undo_action.triggered.connect(lambda: self.get_current_editor().undo())
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        redo_action.triggered.connect(lambda: self.get_current_editor().redo())
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence("Ctrl+X"))
        cut_action.triggered.connect(lambda: self.get_current_editor().cut())
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence("Ctrl+C"))
        copy_action.triggered.connect(lambda: self.get_current_editor().copy())
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence("Ctrl+V"))
        paste_action.triggered.connect(lambda: self.get_current_editor().paste())
        edit_menu.addAction(paste_action)
        
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence("Ctrl+A"))
        select_all_action.triggered.connect(lambda: self.get_current_editor().selectAll())
        edit_menu.addAction(select_all_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("Find...", self)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self.show_find_dialog)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("Replace...", self)
        replace_action.setShortcut(QKeySequence("Ctrl+H"))
        replace_action.triggered.connect(self.show_replace_dialog)
        edit_menu.addAction(replace_action)
        
        edit_menu.addSeparator()
        
        spell_check_action = QAction("Toggle Spell Check", self)
        spell_check_action.setCheckable(True)
        spell_check_action.setChecked(self.file_ops.get_setting('spell_check_enabled', True))
        spell_check_action.triggered.connect(self.toggle_spell_check)
        edit_menu.addAction(spell_check_action)
        
        # Format Menu
        format_menu = menubar.addMenu("F&ormat")
        
        font_action = QAction("✨ Font & Style Settings...", self)
        font_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        font_action.triggered.connect(self.show_font_dialog)
        format_menu.addAction(font_action)
        
        format_menu.addSeparator()
        
        # Quick format actions
        quick_format_label = QAction("Quick Format:", self)
        quick_format_label.setEnabled(False)
        format_menu.addAction(quick_format_label)
        
        bold_action = QAction("Bold", self)
        bold_action.setShortcut(QKeySequence("Ctrl+B"))
        bold_action.setCheckable(True)
        bold_action.triggered.connect(self.toggle_bold)
        format_menu.addAction(bold_action)
        
        italic_action = QAction("Italic", self)
        italic_action.setShortcut(QKeySequence("Ctrl+I"))
        italic_action.setCheckable(True)
        italic_action.triggered.connect(self.toggle_italic)
        format_menu.addAction(italic_action)
        
        underline_action = QAction("Underline", self)
        underline_action.setShortcut(QKeySequence("Ctrl+U"))
        underline_action.setCheckable(True)
        underline_action.triggered.connect(self.toggle_underline)
        format_menu.addAction(underline_action)
        
        format_menu.addSeparator()
        
        color_action = QAction("🎨 Text Color...", self)
        color_action.triggered.connect(self.choose_text_color)
        format_menu.addAction(color_action)
        
        format_menu.addSeparator()
        
        # Font size quick options
        size_menu = format_menu.addMenu("📏 Font Size")
        for size in [8, 10, 11, 12, 14, 16, 18, 20, 24]:
            size_action = QAction(f"{size} pt", self)
            size_action.triggered.connect(lambda checked, s=size: self.quick_font_size(s))
            size_menu.addAction(size_action)
        
        # Store actions for later updates
        self.bold_action = bold_action
        self.italic_action = italic_action
        self.underline_action = underline_action
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        
        # Theme submenu
        theme_submenu = view_menu.addMenu("🎨 Theme")
        for theme_id in self.theme_manager.get_theme_ids():
            theme_data = self.theme_manager.get_theme(theme_id)
            theme_name = theme_data.get('name', theme_id)
            theme_desc = theme_data.get('description', '')
            theme_action = QAction(theme_name, self)
            if theme_desc:
                theme_action.setToolTip(theme_desc)
            theme_action.triggered.connect(lambda checked, tid=theme_id: self.apply_theme(tid))
            theme_submenu.addAction(theme_action)
        
        view_menu.addSeparator()
        
        status_bar_action = QAction("Toggle Status Bar", self)
        status_bar_action.setCheckable(True)
        status_bar_action.setChecked(True)
        status_bar_action.triggered.connect(self.toggle_status_bar)
        view_menu.addAction(status_bar_action)
        
        line_numbers_action = QAction("Toggle Line Numbers", self)
        line_numbers_action.setCheckable(True)
        line_numbers_action.setChecked(self.file_ops.get_setting('show_line_numbers', False))
        line_numbers_action.triggered.connect(self.toggle_line_numbers)
        view_menu.addAction(line_numbers_action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction("Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About Kun", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def setup_status_bar(self):
        """Setup status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_words = QLabel("0 words")
        self.status_chars = QLabel("0 characters")
        self.status_position = QLabel("Ln 1, Col 1")
        self.status_encoding = QLabel("UTF-8")
        self.status_file_path = QLabel("")
        
        self.status_bar.addWidget(self.status_words)
        self.status_bar.addWidget(QLabel("|"))
        self.status_chars.mousePressEvent = lambda event: self.toggle_char_count_mode()
        self.status_chars.setToolTip("Click to toggle between with/without spaces")
        self.status_bar.addWidget(self.status_chars)
        self.status_bar.addWidget(QLabel("|"))
        self.status_bar.addWidget(self.status_position)
        self.status_bar.addWidget(QLabel("|"))
        self.status_bar.addWidget(self.status_encoding)
        self.status_bar.addPermanentWidget(self.status_file_path)
        
        self.update_status_bar()
    
    def get_current_editor(self) -> EditorTab:
        """Get current editor tab."""
        return self.tab_widget.currentWidget()
    
    def new_tab(self, file_path: str = None, content: str = ""):
        """Create a new tab."""
        editor = EditorTab()
        editor.set_spell_checker(self.spell_checker)
        editor.set_show_line_numbers(self.file_ops.get_setting('show_line_numbers', False))
        
        if file_path:
            editor.set_file_path(file_path)
            editor.set_content(content)
            tab_name = os.path.basename(file_path)
        else:
            tab_name = f"Untitled-{self.untitled_counter}"
            self.untitled_counter += 1
        
        # Connect editor signals
        editor.text_changed_signal.connect(self.on_editor_text_changed)
        editor.cursor_position_changed.connect(self.update_status_bar)
        
        index = self.tab_widget.addTab(editor, tab_name)
        self.tab_widget.setCurrentIndex(index)
        
        self.update_status_bar()
        return editor
    
    def close_tab(self, index: int = None):
        """Close a tab."""
        if index is None:
            index = self.tab_widget.currentIndex()
        
        if index < 0:
            return
        
        editor = self.tab_widget.widget(index)
        
        # Check for unsaved changes
        if editor.is_modified:
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                f'Save changes to {editor.get_display_name()}?',
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return
        
        self.tab_widget.removeTab(index)
        
        # Create new tab if none left
        if self.tab_widget.count() == 0:
            self.new_tab()
    
    def on_tab_changed(self, index: int):
        """Handle tab change."""
        if index >= 0:
            editor = self.tab_widget.widget(index)
            file_name = editor.get_display_name()
            self.setWindowTitle(f"{file_name} – Kun")
            self.update_status_bar()
    
    def on_editor_text_changed(self):
        """Handle editor text changes."""
        editor = self.get_current_editor()
        if editor:
            index = self.tab_widget.currentIndex()
            tab_name = editor.get_display_name()
            if editor.is_modified:
                tab_name += " *"
            self.tab_widget.setTabText(index, tab_name)
            self.update_status_bar()
    
    def rename_tab(self, index: int):
        """Rename tab (custom name only, doesn't affect file)."""
        if index < 0:
            return
        
        editor = self.tab_widget.widget(index)
        current_name = editor.get_display_name()
        
        name, ok = QInputDialog.getText(
            self, 'Rename Tab', 'Enter new tab name:',
            text=current_name
        )
        
        if ok and name:
            editor.set_custom_name(name)
            self.tab_widget.setTabText(index, name + (" *" if editor.is_modified else ""))
    
    def open_file(self):
        """Open file dialog."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open File", "", "Text Files (*.txt);;All Files (*.*)"
        )
        
        for file_path in file_paths:
            self.open_file_path(file_path)
    
    def open_file_path(self, file_path: str):
        """Open specific file."""
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "File Not Found", f"File not found: {file_path}")
            return
        
        content = self.file_ops.read_file(file_path)
        if content is not None:
            self.new_tab(file_path, content)
            self.file_ops.add_recent_file(file_path)
            self.update_recent_menu()
    
    def save_file(self):
        """Save current file."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        file_path = editor.get_file_path()
        
        # If no file path, use Save As with the renamed tab name as default
        if not file_path:
            self.save_file_as()
        else:
            content = editor.get_content()
            if self.file_ops.write_file(file_path, content):
                editor.mark_saved()
                self.file_ops.add_recent_file(file_path)
                self.update_recent_menu()
                self.on_editor_text_changed()
                self.statusBar().showMessage(f"Saved: {file_path}", 3000)
    
    def save_file_as(self):
        """Save file as new path."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        # Use custom tab name as default filename if available
        default_name = editor.get_display_name()
        if not default_name.endswith('.txt'):
            default_name += '.txt'
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save As", default_name, "Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_path:
            content = editor.get_content()
            if self.file_ops.write_file(file_path, content):
                editor.set_file_path(file_path)
                editor.mark_saved()
                self.file_ops.add_recent_file(file_path)
                self.update_recent_menu()
                
                # Update tab name
                index = self.tab_widget.currentIndex()
                self.tab_widget.setTabText(index, os.path.basename(file_path))
                self.setWindowTitle(f"{os.path.basename(file_path)} – Kun")
                self.statusBar().showMessage(f"Saved: {file_path}", 3000)
    
    def update_recent_menu(self):
        """Update recent files menu."""
        self.recent_menu.clear()
        
        recent_files = self.file_ops.get_recent_files()
        
        if not recent_files:
            no_recent = QAction("No recent files", self)
            no_recent.setEnabled(False)
            self.recent_menu.addAction(no_recent)
        else:
            for file_path in recent_files:
                action = QAction(os.path.basename(file_path), self)
                action.setToolTip(file_path)
                action.triggered.connect(lambda checked, fp=file_path: self.open_file_path(fp))
                self.recent_menu.addAction(action)
            
            self.recent_menu.addSeparator()
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self.clear_recent_files)
            self.recent_menu.addAction(clear_action)
    
    def clear_recent_files(self):
        """Clear recent files list."""
        self.file_ops.clear_recent_files()
        self.update_recent_menu()
    
    def update_status_bar(self):
        """Update status bar with current statistics."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        text = editor.get_content()
        cursor_pos = editor.get_cursor_position()
        
        stats = self.text_analyzer.get_statistics(text, cursor_pos, self.char_count_with_spaces)
        
        self.status_words.setText(f"{stats['words']:,} words")
        
        char_mode = "with spaces" if self.char_count_with_spaces else "without spaces"
        self.status_chars.setText(f"{stats['characters']:,} chars ({char_mode})")
        
        self.status_position.setText(f"Ln {stats['current_line']}, Col {stats['current_col']}")
        
        file_path = editor.get_file_path()
        if file_path:
            # Truncate long paths
            if len(file_path) > 60:
                display_path = "..." + file_path[-57:]
            else:
                display_path = file_path
            self.status_file_path.setText(display_path)
            self.status_file_path.setToolTip(file_path)
        else:
            self.status_file_path.setText("Unsaved")
    
    def toggle_char_count_mode(self):
        """Toggle character count between with/without spaces."""
        self.char_count_with_spaces = not self.char_count_with_spaces
        mode = 'with_spaces' if self.char_count_with_spaces else 'without_spaces'
        self.file_ops.set_setting('char_count_mode', mode)
        self.update_status_bar()
    
    def show_find_dialog(self):
        """Show find dialog with proper highlighting."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        # Create or show find dialog
        if not hasattr(self, 'find_widget') or self.find_widget is None:
            self.create_find_widget()
        
        self.find_widget.show()
        self.find_input.setFocus()
        self.find_input.selectAll()
    
    def create_find_widget(self):
        """Create inline find widget."""
        from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
        from PyQt6.QtGui import QShortcut, QKeySequence
        
        self.find_widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Add Escape key shortcut to close find widget
        escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self.find_widget)
        escape_shortcut.activated.connect(self.close_find_widget)
        
        layout.addWidget(QLabel("Find:"))
        
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Enter text to find...")
        self.find_input.returnPressed.connect(self.perform_find)
        layout.addWidget(self.find_input)
        
        # Search button
        search_btn = QPushButton("🔍 Search")
        search_btn.clicked.connect(self.perform_find)
        search_btn.setDefault(True)
        layout.addWidget(search_btn)
        
        # Navigation buttons
        prev_btn = QPushButton("◄ Previous")
        prev_btn.clicked.connect(self.find_previous)
        layout.addWidget(prev_btn)
        
        next_btn = QPushButton("Next ►")
        next_btn.clicked.connect(self.find_next)
        layout.addWidget(next_btn)
        
        # Case sensitive checkbox
        self.find_case_sensitive = QCheckBox("Match Case")
        layout.addWidget(self.find_case_sensitive)
        self.find_case_sensitive.stateChanged.connect(self.perform_find)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close_find_widget)
        layout.addWidget(close_btn)
        
        self.find_widget.setLayout(layout)
        
        # Add to status bar area
        self.statusBar().insertWidget(0, self.find_widget)
        self.find_widget.hide()
    
    def perform_find(self):
        """Perform find and highlight all matches."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        search_text = self.find_input.text().strip()
        if not search_text:
            self.statusBar().showMessage("Please enter text to search", 2000)
            return
        
        # Get document
        document = editor.document()
        
        # Set up search flags
        from PyQt6.QtGui import QTextDocument, QTextCharFormat
        flags = QTextDocument.FindFlag(0)
        if self.find_case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        
        # Clear previous selections
        extra_selections = []
        
        # Store all matches
        self.find_matches = []
        self.current_match_index = -1
        
        # Search from beginning
        cursor = QTextCursor(document)
        cursor.setPosition(0)
        
        # Create highlight format
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor(255, 255, 0, 120))  # Yellow highlight
        
        while True:
            cursor = document.find(search_text, cursor, flags)
            if cursor.isNull():
                break
            
            # Store match position
            self.find_matches.append(cursor.selectionStart())
            
            # Add to selections for highlighting
            from PyQt6.QtWidgets import QTextEdit
            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format = highlight_format
            extra_selections.append(selection)
        
        # Apply all highlights at once
        editor.setExtraSelections(extra_selections)
        
        # Move to first match
        if self.find_matches:
            self.current_match_index = 0
            self.jump_to_match(0)
            self.statusBar().showMessage(f"Found {len(self.find_matches)} matches", 3000)
        else:
            self.statusBar().showMessage("No matches found", 2000)
    
    def find_next(self):
        """Jump to next match."""
        if not hasattr(self, 'find_matches') or not self.find_matches:
            self.perform_find()
            return
        
        if self.find_matches:
            self.current_match_index = (self.current_match_index + 1) % len(self.find_matches)
            self.jump_to_match(self.current_match_index)
    
    def find_previous(self):
        """Jump to previous match."""
        if not hasattr(self, 'find_matches') or not self.find_matches:
            self.perform_find()
            return
        
        if self.find_matches:
            self.current_match_index = (self.current_match_index - 1) % len(self.find_matches)
            self.jump_to_match(self.current_match_index)
    
    def jump_to_match(self, index):
        """Jump to specific match."""
        editor = self.get_current_editor()
        if not editor or not self.find_matches:
            return
        
        position = self.find_matches[index]
        search_text = self.find_input.text()
        
        # Create cursor and select the match
        cursor = QTextCursor(editor.document())
        cursor.setPosition(position)
        cursor.setPosition(position + len(search_text), QTextCursor.MoveMode.KeepAnchor)
        
        editor.setTextCursor(cursor)
        editor.ensureCursorVisible()
        
        self.statusBar().showMessage(f"Match {index + 1} of {len(self.find_matches)}", 2000)
    
    def close_find_widget(self):
        """Close find widget and clear highlights."""
        editor = self.get_current_editor()
        if editor:
            editor.setExtraSelections([])  # Clear highlights
            # Clear any selection to return to normal view
            cursor = editor.textCursor()
            cursor.clearSelection()
            editor.setTextCursor(cursor)
            editor.setFocus()  # Return focus to editor
        self.find_widget.hide()
        self.find_matches = []
        self.current_match_index = -1
    
    def show_replace_dialog(self):
        """Show find & replace dialog."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        dialog = FindReplaceDialog(self)
        
        # Connect buttons
        dialog.find_next_btn.clicked.connect(lambda: self.dialog_find_next(dialog, editor))
        dialog.find_prev_btn.clicked.connect(lambda: self.dialog_find_prev(dialog, editor))
        dialog.replace_btn.clicked.connect(lambda: self.dialog_replace(dialog, editor))
        dialog.replace_all_btn.clicked.connect(lambda: self.dialog_replace_all(dialog, editor))
        
        dialog.exec()
    
    def dialog_find_next(self, dialog, editor):
        """Find next in dialog."""
        search_text = dialog.find_input.text()
        if not search_text:
            return
        
        from PyQt6.QtGui import QTextDocument
        flags = QTextDocument.FindFlag(0)
        if dialog.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if dialog.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
        
        cursor = editor.textCursor()
        found_cursor = editor.document().find(search_text, cursor, flags)
        
        if found_cursor.isNull() and dialog.wrap_around.isChecked():
            # Wrap around to beginning
            cursor.setPosition(0)
            found_cursor = editor.document().find(search_text, cursor, flags)
        
        if not found_cursor.isNull():
            editor.setTextCursor(found_cursor)
            editor.ensureCursorVisible()
        else:
            self.statusBar().showMessage("No more matches found", 2000)
    
    def dialog_find_prev(self, dialog, editor):
        """Find previous in dialog."""
        search_text = dialog.find_input.text()
        if not search_text:
            return
        
        from PyQt6.QtGui import QTextDocument
        flags = QTextDocument.FindFlag.FindBackward
        if dialog.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if dialog.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
        
        cursor = editor.textCursor()
        found_cursor = editor.document().find(search_text, cursor, flags)
        
        if found_cursor.isNull() and dialog.wrap_around.isChecked():
            # Wrap around to end
            cursor.movePosition(QTextCursor.MoveOperation.End)
            found_cursor = editor.document().find(search_text, cursor, flags)
        
        if not found_cursor.isNull():
            editor.setTextCursor(found_cursor)
            editor.ensureCursorVisible()
        else:
            self.statusBar().showMessage("No more matches found", 2000)
    
    def dialog_replace(self, dialog, editor):
        """Replace current selection."""
        search_text = dialog.find_input.text()
        replace_text = dialog.replace_input.text()
        
        if not search_text:
            return
        
        cursor = editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == search_text:
            cursor.insertText(replace_text)
            self.statusBar().showMessage("Replaced 1 occurrence", 2000)
        
        # Find next
        self.dialog_find_next(dialog, editor)
    
    def dialog_replace_all(self, dialog, editor):
        """Replace all occurrences."""
        search_text = dialog.find_input.text()
        replace_text = dialog.replace_input.text()
        
        if not search_text:
            return
        
        from PyQt6.QtGui import QTextDocument
        flags = QTextDocument.FindFlag(0)
        if dialog.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if dialog.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
        
        cursor = QTextCursor(editor.document())
        cursor.beginEditBlock()
        
        count = 0
        cursor.setPosition(0)
        
        while True:
            cursor = editor.document().find(search_text, cursor, flags)
            if cursor.isNull():
                break
            cursor.insertText(replace_text)
            count += 1
        
        cursor.endEditBlock()
        self.statusBar().showMessage(f"Replaced {count} occurrences", 3000)
    
    def toggle_spell_check(self, checked: bool):
        """Toggle spell checking."""
        self.spell_checker.set_enabled(checked)
        self.file_ops.set_setting('spell_check_enabled', checked)
        
        # Update all editors
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if checked:
                editor.check_spelling()
            else:
                # Clear spell check highlights
                pass
    
    def show_font_dialog(self):
        """Show font settings dialog."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("✨ Font & Style Settings")
        dialog.setMinimumWidth(450)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Customize Your Text Appearance")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Font family section
        family_group = QVBoxLayout()
        family_label = QLabel("📝 Font Family:")
        family_label.setStyleSheet("font-weight: bold;")
        family_group.addWidget(family_label)
        
        font_combo = QComboBox()
        font_combo.addItems([
            "Consolas", 
            "Courier New", 
            "Source Code Pro",
            "Fira Code",
            "JetBrains Mono",
            "Arial", 
            "Segoe UI",
            "Times New Roman",
            "Georgia",
            "Verdana"
        ])
        font_combo.setCurrentText(editor.current_font_family)
        font_combo.setStyleSheet("padding: 8px; font-size: 12px;")
        font_combo.currentTextChanged.connect(lambda: self.preview_font(editor, font_combo, size_spin))
        family_group.addWidget(font_combo)
        layout.addLayout(family_group)
        
        # Font size section
        size_group = QVBoxLayout()
        size_label = QLabel("📏 Font Size:")
        size_label.setStyleSheet("font-weight: bold;")
        size_group.addWidget(size_label)
        
        size_layout = QHBoxLayout()
        size_spin = QSpinBox()
        size_spin.setRange(8, 72)
        size_spin.setValue(editor.current_font_size)
        size_spin.setSuffix(" pt")
        size_spin.setStyleSheet("padding: 8px; font-size: 12px;")
        size_spin.valueChanged.connect(lambda: self.preview_font(editor, font_combo, size_spin))
        size_layout.addWidget(size_spin)
        
        # Quick size buttons
        for size in [10, 12, 14, 16, 18]:
            size_btn = QPushButton(str(size))
            size_btn.setFixedSize(40, 30)
            size_btn.clicked.connect(lambda checked, s=size: size_spin.setValue(s))
            size_layout.addWidget(size_btn)
        
        size_group.addLayout(size_layout)
        layout.addLayout(size_group)
        
        # Style section
        style_group = QVBoxLayout()
        style_label = QLabel("🎨 Text Style:")
        style_label.setStyleSheet("font-weight: bold;")
        style_group.addWidget(style_label)
        
        style_layout = QHBoxLayout()
        
        bold_check = QCheckBox("Bold")
        bold_check.setChecked(editor.current_font_bold)
        bold_check.setStyleSheet("font-weight: bold;")
        style_layout.addWidget(bold_check)
        
        italic_check = QCheckBox("Italic")
        italic_check.setChecked(editor.current_font_italic)
        italic_check.setStyleSheet("font-style: italic;")
        style_layout.addWidget(italic_check)
        
        underline_check = QCheckBox("Underline")
        underline_check.setChecked(editor.current_font_underline)
        underline_check.setStyleSheet("text-decoration: underline;")
        style_layout.addWidget(underline_check)
        
        style_group.addLayout(style_layout)
        layout.addLayout(style_group)
        
        # Color section
        color_group = QVBoxLayout()
        color_label = QLabel("🌈 Text Color:")
        color_label.setStyleSheet("font-weight: bold;")
        color_group.addWidget(color_label)
        
        color_layout = QHBoxLayout()
        
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(60, 30)
        self.color_preview.setStyleSheet(f"background-color: {editor.current_text_color.name()}; border: 2px solid #666; border-radius: 4px;")
        color_layout.addWidget(self.color_preview)
        
        color_btn = QPushButton("Choose Color...")
        color_btn.clicked.connect(lambda: self.dialog_choose_color(editor))
        color_layout.addWidget(color_btn)
        
        # Quick color presets
        preset_colors = ["#e0e0e0", "#ffffff", "#ff6b6b", "#4ecdc4", "#45b7d1", "#feca57", "#ee5a6f", "#c7ecee"]
        for color in preset_colors:
            preset_btn = QPushButton()
            preset_btn.setFixedSize(25, 25)
            preset_btn.setStyleSheet(f"background-color: {color}; border: 1px solid #666; border-radius: 3px;")
            preset_btn.clicked.connect(lambda checked, c=color: self.apply_preset_color(editor, c))
            color_layout.addWidget(preset_btn)
        
        color_group.addLayout(color_layout)
        layout.addLayout(color_group)
        
        # Separator
        separator = QLabel()
        separator.setStyleSheet("background-color: #444; min-height: 1px; max-height: 1px;")
        layout.addWidget(separator)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("🔄 Reset to Default")
        reset_btn.clicked.connect(lambda: self.reset_font_settings(editor, font_combo, size_spin, bold_check, italic_check, underline_check))
        button_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("✅ Apply")
        apply_btn.setDefault(True)
        apply_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px 16px;")
        apply_btn.clicked.connect(lambda: self.apply_font_settings(
            editor, font_combo, size_spin, bold_check, italic_check, underline_check, dialog
        ))
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def preview_font(self, editor, font_combo, size_spin):
        """Live preview of font changes."""
        editor.set_font_family(font_combo.currentText())
        editor.set_font_size(size_spin.value())
    
    def dialog_choose_color(self, editor):
        """Choose custom text color."""
        color = QColorDialog.getColor(editor.current_text_color, self, "Choose Text Color")
        if color.isValid():
            editor.set_text_color(color)
            self.color_preview.setStyleSheet(f"background-color: {color.name()}; border: 2px solid #666; border-radius: 4px;")
    
    def apply_preset_color(self, editor, color_hex):
        """Apply preset color."""
        color = QColor(color_hex)
        editor.set_text_color(color)
        self.color_preview.setStyleSheet(f"background-color: {color_hex}; border: 2px solid #666; border-radius: 4px;")
    
    def reset_font_settings(self, editor, font_combo, size_spin, bold_check, italic_check, underline_check):
        """Reset to default font settings."""
        font_combo.setCurrentText("Consolas")
        size_spin.setValue(11)
        bold_check.setChecked(False)
        italic_check.setChecked(False)
        underline_check.setChecked(False)
        editor.set_font_family("Consolas")
        editor.set_font_size(11)
        editor.set_font_bold(False)
        editor.set_font_italic(False)
        editor.set_font_underline(False)
        editor.set_text_color(QColor("#e0e0e0"))
        self.color_preview.setStyleSheet(f"background-color: #e0e0e0; border: 2px solid #666; border-radius: 4px;")
    
    def apply_font_settings(self, editor, font_combo, size_spin, bold_check, italic_check, underline_check, dialog):
        """Apply all font settings."""
        editor.set_font_family(font_combo.currentText())
        editor.set_font_size(size_spin.value())
        editor.set_font_bold(bold_check.isChecked())
        editor.set_font_italic(italic_check.isChecked())
        editor.set_font_underline(underline_check.isChecked())
        dialog.accept()
    
    def toggle_bold(self, checked):
        """Toggle bold formatting."""
        editor = self.get_current_editor()
        if editor:
            editor.set_font_bold(checked)
    
    def toggle_italic(self, checked):
        """Toggle italic formatting."""
        editor = self.get_current_editor()
        if editor:
            editor.set_font_italic(checked)
    
    def toggle_underline(self, checked):
        """Toggle underline formatting."""
        editor = self.get_current_editor()
        if editor:
            editor.set_font_underline(checked)
    
    def quick_font_size(self, size):
        """Quickly change font size."""
        editor = self.get_current_editor()
        if editor:
            editor.set_font_size(size)
            self.statusBar().showMessage(f"Font size: {size}pt", 2000)
    
    def choose_text_color(self):
        """Choose text color."""
        editor = self.get_current_editor()
        if not editor:
            return
        
        color = QColorDialog.getColor(editor.current_text_color, self, "Choose Text Color")
        if color.isValid():
            editor.set_text_color(color)
    
    def apply_theme(self, theme_id: str):
        """Apply theme to application."""
        if self.theme_manager.set_current_theme(theme_id):
            stylesheet = self.theme_manager.generate_stylesheet()
            self.setStyleSheet(stylesheet)
            self.file_ops.set_setting('theme', theme_id)
            
            # Show friendly notification
            theme_data = self.theme_manager.get_theme(theme_id)
            theme_name = theme_data.get('name', theme_id)
            self.statusBar().showMessage(f"✨ Applied theme: {theme_name}", 3000)
    
    def toggle_status_bar(self, checked: bool):
        """Toggle status bar visibility."""
        self.status_bar.setVisible(checked)
    
    def toggle_line_numbers(self, checked: bool):
        """Toggle line numbers for all tabs."""
        self.file_ops.set_setting('show_line_numbers', checked)
        
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            editor.set_show_line_numbers(checked)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About Kun",
            "<h2>Kun Text Editor</h2>"
            "<p>Version 1.0.0</p>"
            "<p>A lightweight, aesthetically-driven text editor.</p>"
            "<p>Built with PyQt6</p>"
        )
    
    def show_shortcuts(self):
        """Show keyboard shortcuts dialog."""
        shortcuts_text = """
        <h3>Keyboard Shortcuts</h3>
        <table>
        <tr><td><b>Ctrl+T</b></td><td>New Tab</td></tr>
        <tr><td><b>Ctrl+O</b></td><td>Open</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>Save</td></tr>
        <tr><td><b>Ctrl+Shift+S</b></td><td>Save As</td></tr>
        <tr><td><b>Ctrl+W</b></td><td>Close Tab</td></tr>
        <tr><td><b>Ctrl+Tab</b></td><td>Next Tab</td></tr>
        <tr><td><b>Ctrl+Shift+Tab</b></td><td>Previous Tab</td></tr>
        <tr><td><b>Ctrl+F</b></td><td>Find</td></tr>
        <tr><td><b>Ctrl+H</b></td><td>Replace</td></tr>
        <tr><td><b>Ctrl+Z</b></td><td>Undo</td></tr>
        <tr><td><b>Ctrl+Y</b></td><td>Redo</td></tr>
        <tr><td><b>Ctrl+A</b></td><td>Select All</td></tr>
        <tr><td><b>F11</b></td><td>Fullscreen</td></tr>
        <tr><td><b>F2</b></td><td>Rename Tab</td></tr>
        </table>
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def auto_save_all(self):
        """Auto-save all modified tabs."""
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            if editor.is_modified and editor.get_file_path():
                content = editor.get_content()
                self.file_ops.write_file(editor.get_file_path(), content)
                editor.mark_saved()
    
    def save_session(self):
        """Save current session."""
        tabs = []
        for i in range(self.tab_widget.count()):
            editor = self.tab_widget.widget(i)
            tab_data = {
                'file_path': editor.get_file_path(),
                'content': editor.get_content() if not editor.get_file_path() else None,
                'custom_name': editor.custom_tab_name
            }
            tabs.append(tab_data)
        
        self.file_ops.save_session(tabs)
    
    def restore_session(self):
        """Restore previous session."""
        tabs = self.file_ops.restore_session()
        
        for tab_data in tabs:
            file_path = tab_data.get('file_path')
            content = tab_data.get('content', '')
            custom_name = tab_data.get('custom_name')
            
            if file_path and os.path.exists(file_path):
                content = self.file_ops.read_file(file_path)
                editor = self.new_tab(file_path, content)
            elif content:
                editor = self.new_tab(content=content)
            
            if custom_name:
                editor.set_custom_name(custom_name)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.txt'):
                self.open_file_path(file_path)
    
    def closeEvent(self, event):
        """Handle window close."""
        # Save session
        self.save_session()
        
        # Check for unsaved changes
        has_unsaved = False
        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i).is_modified:
                has_unsaved = True
                break
        
        if has_unsaved:
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                'You have unsaved changes. Save before closing?',
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                # Save all modified tabs
                for i in range(self.tab_widget.count()):
                    self.tab_widget.setCurrentIndex(i)
                    self.save_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
