from Sorter import configurator as config_module
import glob, os
from datetime import datetime

class Sorter:

    def path_check(self,file_path,path_destination):
        if ' ' in file_path:
            os.rename(file_path, file_path.replace(' ', '_'))
            file_path = file_path.replace(' ', '_')
        if ',' in file_path:
            os.rename(file_path, file_path.replace(',', ''))
            file_path = file_path.replace(',', '')
        file_name = file_path.split('\\')[-1]
        if os.path.isfile(path_destination+'\\'+file_name):
            os.rename(file_path, file_path.split('.')[0]+"_duplicate_"+str(int(datetime.timestamp(datetime.now()))%1000000)+"."+file_path.split('.')[1])
            file_path = file_path.split('.')[0]+"_duplicate_"+str(int(datetime.timestamp(datetime.now()))%1000000)+"."+file_path.split('.')[1]
        return file_path

    def sort(self,path_destination,extensions):
        if self.path_downloads != "" and os.path.exists(self.path_downloads):
            if not os.path.exists(path_destination):
                os.mkdir(path_destination)
            for extension in extensions.split(" "):
                for file_path in glob.glob(self.path_downloads+"/*"+extension):
                    file_path = self.path_check(file_path,path_destination)
                    os.system(f'move {file_path} {path_destination}')

    def __init__(self):
        configurator = config_module.Configurator()
        self.config = configurator.load_config("Sorter/config.json")
        self.path_downloads = self.config["path_downloads"]
        for rule in self.config["rules"]:
            self.sort(rule[0], rule[1])
