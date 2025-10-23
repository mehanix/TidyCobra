<div align="center">

# 🐍 TidyCobra

**Automated File Organization Made Simple**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/mehanix/TidyCobra)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GUI](https://img.shields.io/badge/GUI-wxPython-orange.svg)](https://wxpython.org/)

<img src="https://i.imgur.com/xIFQWXg.png" alt="TidyCobra Logo" width="200"/>

> **Never worry about a cluttered Downloads folder again!** TidyCobra automatically sorts your downloaded files into organized folders based on file type, keeping your workspace clean and efficient.

</div>

---

## ✨ Features

<table>
<tr>
<td>

### 🚀 **Smart File Sorting**
Automatically categorize files by type (Images, Documents, Videos, Music, Archives, etc.) and move them to appropriate folders.

</td>
<td>

### ⚙️ **Customizable Rules**
Create personalized sorting rules through an intuitive GUI. Define exactly where each file type should go.

</td>
</tr>
<tr>
<td>

### 🔄 **Real-time Monitoring**
Set up background monitoring to automatically sort files as soon as they're downloaded.

</td>
<td>

### 🎯 **Startup Integration**
Configure TidyCobra to run automatically when your system starts, ensuring continuous organization.

</td>
</tr>
<tr>
<td>

### 📁 **Smart Folder Detection**
Automatically detects and uses your system's standard folders (Documents, Pictures, Music, etc.).

</td>
<td>

### 🖥️ **Cross-Platform GUI**
Beautiful, responsive interface built with wxPython that works seamlessly across all supported platforms.

</td>
</tr>
</table>

## 🖥️ Platform Support

TidyCobra runs on all major desktop operating systems:

| Platform | Support | Status |
|----------|---------|---------|
| **Windows** | ✅ Full Support | Windows 10/11 |
| **macOS** | ✅ Full Support | macOS 10.15+ |
| **Linux** | ✅ Full Support | Ubuntu, Fedora, CentOS, etc. |

*Requires Python 3.7 or higher*

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **wxPython** (for GUI functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mehanix/TidyCobra.git
   cd TidyCobra
   ```

2. **Install dependencies**
   ```bash
   pip install wxpython
   ```

3. **Run TidyCobra**
   ```bash
   python TidyCobra.py
   ```

### 🎨 First Time Setup

1. Launch the application using the command above
2. The GUI will guide you through the initial configuration
3. Set up your sorting rules and folder preferences
4. Choose whether to enable startup monitoring

## 📖 Usage Examples

### Basic File Organization
Once configured, TidyCobra will automatically:
- Move `.jpg`, `.png`, `.gif` files to your Pictures folder
- Sort `.pdf`, `.docx`, `.txt` files to your Documents folder
- Organize `.mp3`, `.wav`, `.flac` files in your Music folder
- Place `.zip`, `.rar`, `.7z` files in your Archives folder

### Advanced Configuration
- Create custom file type rules
- Set up multiple destination folders
- Configure file name patterns and exclusions
- Schedule automatic cleanup intervals

## 🛠️ Configuration Options

### Default Folder Mappings
```
📸 Images → ~/Pictures
📄 Documents → ~/Documents
🎵 Music → ~/Music
🎬 Videos → ~/Videos
📦 Archives → ~/Archives
```

### Custom Rules
Use the built-in GUI to create custom sorting rules:
- File extensions (`.psd`, `.raw`, etc.)
- File patterns (`screenshot_*`, `backup_*`)
- Size-based sorting
- Date-based organization

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TidyCobra.git
cd TidyCobra

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install wxpython

# Run in development mode
python TidyCobra.py
```

## 📝 Changelog

### Version 1.0.0
- ✅ Initial release
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ GUI-based configuration
- ✅ Automatic file sorting
- ✅ Startup integration

## 🐛 Issues & Support

- **Bug Reports**: [Open an issue](https://github.com/mehanix/TidyCobra/issues)
- **Feature Requests**: [Start a discussion](https://github.com/mehanix/TidyCobra/discussions)
- **Documentation**: Check the [Wiki](https://github.com/mehanix/TidyCobra/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **wxPython** - For the excellent GUI toolkit
- **Python Community** - For the amazing ecosystem
- **All Contributors** - For making this project better

---

<div align="center">

**Made with ❤️ for developers who love clean workspaces**

[⭐ Star us on GitHub](https://github.com/mehanix/TidyCobra) • [🐛 Report Issues](https://github.com/mehanix/TidyCobra/issues) • [💬 Join Discussions](https://github.com/mehanix/TidyCobra/discussions)

</div>
