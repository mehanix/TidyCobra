from os.path import expanduser
from pathlib import Path
import folder_paths
from GUI import view_main
import glob
home_path = ""
downloads_path = ""

def run():
    print("Welcome to TidyCobra!")
    home_path = str(Path().home())
    downloads_path = home_path + "/Downloads"
    print("Downloads path is:",__name__)
    print(glob.glob("./*.txt"))
    view_main.render_GUI()