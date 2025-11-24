# 🌙 Kun Text Editor

> **A lightweight, aesthetically-driven desktop text editor built with Python and PyQt6**

Kun combines powerful editing features with beautiful visual themes and an intuitive interface. Whether you're writing notes, code, or prose, Kun provides a distraction-free environment with all the tools you need.

---

## ✨ Key Features

### 📝 **Core Editing**
- **Multi-Tab Interface** - Work on multiple documents simultaneously with easy tab management
- **Smart Tab Renaming** - Double-click or press F2 to rename tabs without affecting file names
- **Drag & Drop Support** - Simply drop .txt files into the editor to open them
- **Auto-Save & Session Restore** - Never lose your work; automatically restores your previous session
- **Undo/Redo** - Full undo/redo support with `Ctrl+Z` and `Ctrl+Y`

### 🎨 **Visual Themes**
Choose from three beautifully crafted themes:

- **🌑 Noir Minimal** - Sleek dark theme with glass effects and high contrast
- **🎮 PixelPop Retro** - Vibrant cyberpunk theme with neon colors and 80s vibe
- **🌸 CuteBlush** - Soft pastel theme with gentle colors and cozy feel

Switch themes instantly from `View > Theme` menu with live preview and descriptions.

### 🔍 **Search & Replace**
- **Inline Find Widget** - Press `Ctrl+F` for quick search with yellow highlighting
- **Advanced Find & Replace** - Press `Ctrl+H` for full find/replace dialog
- **Match Options** - Case sensitive, whole words, and wrap around support
- **Navigation** - Jump between matches with Previous/Next buttons
- **Replace All** - Replace all occurrences with a single click

### 📊 **Real-Time Statistics**
Live statistics displayed in the status bar:
- **Word Count** - Real-time word counting
- **Character Count** - With/without spaces (click to toggle)
- **Line & Column** - Current cursor position (Ln X, Col Y)
- **File Path** - Full path with tooltip for long paths
- **Encoding** - UTF-8 encoding indicator

### ✍️ **Font & Formatting**
Comprehensive font customization dialog (`Ctrl+Shift+F`):
- **10 Font Families** - Consolas, Courier New, Source Code Pro, Fira Code, JetBrains Mono, Arial, Segoe UI, Times New Roman, Georgia, Verdana
- **Live Preview** - See changes as you adjust settings
- **Quick Size Buttons** - Instant access to common sizes (10-18pt)
- **Text Styles** - Bold, Italic, Underline with `Ctrl+B`, `Ctrl+I`, `Ctrl+U`
- **Color Presets** - 8 pre-defined colors plus custom color picker
- **Reset Option** - One-click reset to defaults

### 📋 **File Management**
- **New, Open, Save, Save As** - Standard file operations with keyboard shortcuts
- **Recent Files** - Access your last 15 opened files quickly
- **Smart Save As** - Uses custom tab name as default filename
- **Multiple File Open** - Select multiple files to open at once
- **File Type Filter** - .txt files and all files support

### 🔤 **Additional Features**
- **Line Numbers** - Toggle line numbers on/off (`View > Toggle Line Numbers`)
- **Spell Checking** - Basic spell checking (toggle in Edit menu)
- **Fullscreen Mode** - Distraction-free editing with `F11`
- **Status Bar Toggle** - Hide/show status bar for more space
- **Quick Font Size Menu** - Instant size changes (8-24pt)

---

## 🚀 Installation

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package installer)

### Steps

1. **Clone or download** the Kun repository to your local machine

2. **Navigate to the Kun directory:**
   ```powershell
   cd X:\Kun
   ```

3. **Install required dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

   This installs:
   - `PyQt6` >= 6.6.0 - GUI framework
   - `pyspellchecker` >= 0.7.2 - Spell checking

---

## 🎯 Quick Start

### Running Kun

**Basic launch:**
```powershell
python main.py
```

**Open a specific file:**
```powershell
python main.py document.txt
```

**Open multiple files:**
```powershell
python main.py file1.txt file2.txt file3.txt
```

### First Steps

1. **Create a new document** - Click the `+` button or press `Ctrl+T`
2. **Choose your theme** - Go to `View > 🎨 Theme` and select your favorite
3. **Customize fonts** - Press `Ctrl+Shift+F` to open Font & Style Settings
4. **Start writing** - Your work is automatically saved when you hit `Ctrl+S`

---

## ⌨️ Keyboard Shortcuts

### File Operations
| Action | Shortcut |
|--------|----------|
| New Tab | `Ctrl+T` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Close Tab | `Ctrl+W` |
| Exit | `Alt+F4` |

### Editing
| Action | Shortcut |
|--------|----------|
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Cut | `Ctrl+X` |
| Copy | `Ctrl+C` |
| Paste | `Ctrl+V` |
| Select All | `Ctrl+A` |

### Search & Replace
| Action | Shortcut |
|--------|----------|
| Find | `Ctrl+F` |
| Replace | `Ctrl+H` |
| Close Find | `Esc` |

### Formatting
| Action | Shortcut |
|--------|----------|
| Font Settings | `Ctrl+Shift+F` |
| Bold | `Ctrl+B` |
| Italic | `Ctrl+I` |
| Underline | `Ctrl+U` |

### Navigation
| Action | Shortcut |
|--------|----------|
| Next Tab | `Ctrl+Tab` |
| Previous Tab | `Ctrl+Shift+Tab` |
| Rename Tab | `F2` or Double-click |
| Fullscreen | `F11` |

---

## 📁 Project Structure

```
Kun/
├── main.py                 # Application entry point
├── app.py                  # Main application class
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DESKTOP_APP_GUIDE.md   # Guide to create desktop app
│
├── core/                  # Core functionality
│   ├── file_ops.py       # File I/O, recent files, config
│   ├── text_analyzer.py  # Word/char counting, statistics
│   └── spell_checker.py  # Spell checking integration
│
├── ui/                    # User interface components
│   ├── main_window.py    # Main window with menus, tabs
│   ├── editor_tab.py     # Text editor with line numbers
│   └── theme_manager.py  # Theme loading and stylesheet generation
│
├── assets/               # Visual assets
│   └── themes/          # Theme JSON files
│       ├── noir.json    # Dark glass theme
│       ├── pixelpop.json # Neon retro theme
│       └── cuteblush.json # Soft pastel theme
│
└── config/              # User configuration
    └── kun_config.json  # Settings, recent files, session data
```

---

## 🎨 Theme Customization

Kun uses JSON-based themes stored in `assets/themes/`. Each theme defines:

- **Colors** - Background, foreground, borders, highlights
- **Fonts** - Default font family and size
- **Effects** - Glass effects, transparency, rounded corners

### Creating Your Own Theme

1. Copy an existing theme file (e.g., `noir.json`)
2. Modify the colors and settings
3. Save with a unique name in `assets/themes/`
4. Restart Kun - your theme will appear in the View menu

---

## 🔧 Configuration

User settings are stored in `config/kun_config.json`:

- **Theme preference** - Your selected theme
- **Recent files** - Last 15 opened files
- **Session data** - Open tabs and their content
- **UI preferences** - Line numbers, spell check, char count mode
- **Window geometry** - Last window size and position

---

## 💡 Usage Tips

### Workflow Tips
- **Use Tab Renaming** - Name tabs descriptively without affecting file names
- **Toggle Character Count** - Click the character count in status bar to toggle with/without spaces
- **Quick Theme Switching** - Hover over theme names to see descriptions
- **Recent Files** - Access your most recent files from `File > Open Recent`

### Productivity Tips
- **Keyboard First** - Learn the shortcuts for faster editing
- **Split Your Work** - Use multiple tabs for different sections
- **Save Often** - Use `Ctrl+S` frequently (or enable auto-save)
- **Find Workflow** - Use `Ctrl+F` for quick searches, `Esc` to close

### Customization Tips
- **Font Preview** - The font dialog shows live preview as you adjust
- **Color Presets** - Use preset colors for quick color changes
- **Line Numbers** - Enable for code editing, disable for prose

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Check for error messages in the terminal

### Themes not loading
- Verify theme files exist in `assets/themes/`
- Check JSON syntax in theme files
- Try deleting `config/kun_config.json` to reset settings

### Files not saving
- Check write permissions in the target directory
- Verify disk space availability
- Try "Save As" to a different location

### Font not displaying
- Ensure the selected font is installed on your system
- Try a different font from the Font Settings dialog
- Reset to default font (Consolas)

---

## 🤝 Contributing

Kun is a personal project, but suggestions and feedback are welcome!

### Feature Requests
- Consider the MVP philosophy - simple and elegant
- Focus on text editing core functionality
- Maintain the aesthetic-driven design

### Bug Reports
Include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Error messages (if any)
4. Python version and OS

---

## 📜 License

This project is provided as-is for personal and educational use.

---

## 🙏 Acknowledgments

- **PyQt6** - Powerful GUI framework
- **pyspellchecker** - Spell checking functionality
- **Python** - Foundation of the project

---

## 📞 Support

For questions, issues, or suggestions:
1. Check the troubleshooting section
2. Review the `DESKTOP_APP_GUIDE.md` for desktop app creation
3. Consult the inline code documentation

---

**Made with ❤️ for writers, coders, and note-takers**

*Version 1.0.0 - November 2025*
| Previous Tab | `Ctrl+Shift+Tab` |
| Find | `Ctrl+F` |
| Replace | `Ctrl+H` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Select All | `Ctrl+A` |
| Fullscreen | `F11` |
| Rename Tab | `F2` or Double-click tab |

## Themes

### Noir Minimal
Dark, minimalist theme with high contrast for distraction-free writing.

### PixelPop
Vibrant retro theme with neon colors and 8-bit style aesthetics.

### CuteBlush
Soft, pastel theme with rounded corners and playful design elements.

Switch themes via **View > Theme** menu.

## Configuration

Settings are automatically saved to `config/kun_config.json`:
- Recent files list
- Current theme
- Auto-save preferences
- Line number display
- Spell check settings
- Session data (open tabs)

## Project Structure

```
kun/
├── main.py                 # Entry point
├── app.py                  # Application class
├── ui/
│   ├── main_window.py      # Main window with menus and tabs
│   ├── editor_tab.py       # Text editor component
│   └── theme_manager.py    # Theme loading and styling
├── core/
│   ├── file_ops.py         # File I/O and session management
│   ├── text_analyzer.py    # Text statistics
│   └── spell_checker.py    # Spell checking
├── assets/
│   └── themes/             # Theme JSON files
└── config/
    └── kun_config.json     # User settings
```

## Requirements

- Python 3.8+
- PyQt6 >= 6.6.0
- pyspellchecker >= 0.7.2

## License

MIT License - Feel free to use, modify, and distribute.

## About

Kun is designed for writers, coders, and anyone who appreciates clean, functional software with beautiful design. The name "Kun" (君) means "you" or "lord" in Japanese - because this editor is built for you.

Enjoy writing! ✨
