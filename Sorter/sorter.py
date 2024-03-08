from Sorter import configurator as config_module
import glob, os

class Sorter:

    def sort(self,path_destination,extensions):
        if os.path.exists(self.path_downloads):
            if not os.path.exists(path_destination):
                os.mkdir(path_destination)
            for extension in extensions:
                for file_path in glob.glob(self.path_downloads+"/*"+extension):
                    os.system(f'move {file_path} {self.path_destination}')
            print("done!")


    def __init__(self):
        configurator = config_module.Configurator()
        self.config = configurator.load_config("../Sorter/config.json")
        self.path_downloads = self.config["path_downloads"]
        old_path = os.getcwd()
        os.chdir(self.path_downloads)
        print("path_dw:",self.path_downloads,"current dir",os.getcwd())
        for rule in self.config["rules"]:
            path_destination = rule[0]
            extensions = rule[1].split(' ')
            print(path_destination, extensions)
            self.sort(path_destination, extensions)
        os.chdir(old_path)
