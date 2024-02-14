<div align="center">
<img align="center" src="https://i.imgur.com/xIFQWXg.png">
</div>

# TidyCobra

TidyCobra is a Python-based utility that automates the sorting of downloaded files into designated folders like Pictures, Music, Documents, etc., keeping your Downloads folder organized.
<p>🐍 Includes configuration tool, as well as a script to be set to run on startup, in order to periodically reroute your downloaded files to their respective folders.</p>
<p> 🐍 Written in Python. GUI created using wxPython.</p>

## Features

- **Automatic Sorting**: Redirect files to specific folders based on file type.
- **Custom Rules**: Configure your own sorting criteria.
- **Startup Script**: Set up TidyCobra to run on system startup.

## Requirements

- Python 3.x
- wxPython (for GUI)

## Installation

```bash
git clone https://github.com/mehanix/TidyCobra.git
cd TidyCobra
pip install -r requirements.txt
```

## Usage

To start TidyCobra, run:

```bash
python TidyCobra.py
```

Follow the GUI prompts to configure your sorting rules.

## Configuration

Use the provided GUI to create rules for sorting your downloads. These rules determine the destination folder for each file type.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)

## Acknowledgments

Thanks to all the contributors who have helped with this project. Special thanks to the wxPython project for the GUI toolkit.
