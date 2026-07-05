<div align="center">
<img align="center" src="./Assets/banner.png">
</div>
<br/>
<p>🐍TidyCobra is a Python-based utility that automates the sorting of your files into designated folders like Pictures, Music, Documents, etc., keeping your folders organized.</p>
<p>🐍 Includes configuration tool, as well as a script to be set to run, in order to periodically reroute your files to their respective folders.</p>
<p> 🐍 Written in Python. GUI created using wxPython.</p>

## Features

- **Automatic Sorting**: Redirect files to specific folders based on file type.
- **Custom Rules**: Configure your own sorting criteria.

## Supported Platforms

| Platform | Status |
| --- | --- |
| Linux | Supported |
| Windows | Supported |
| macOS | Not currently documented as supported |

> **Note:** TidyCobra is a Python desktop app built with wxPython. Linux and
> Windows are the documented targets today; macOS may work if the dependencies
> install correctly, but it is not currently listed as an officially supported
> platform.

## Requirements

- Python 3.x
- wxPython (for GUI)
- pypubsub

## Installation

```bash
git clone https://github.com/mehanix/TidyCobra.git
cd TidyCobra
pip install -r requirements.txt
```

## Usage

To start TidyCobra, run:

```bash
python app.py
```

Follow the GUI prompts to configure your sorting rules.

## Configuration

Use the provided GUI to create rules for sorting your downloads. These rules determine the destination folder for each file type.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

Thanks to all the contributors who have helped with this project. Special thanks to the wxPython project for the GUI toolkit.
