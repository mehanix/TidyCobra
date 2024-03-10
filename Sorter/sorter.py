from Sorter import configurator as config_module
import glob, os

class Sorter:

    def sort(self,path_destination,extensions):
        if self.path_downloads != "" and os.path.exists(self.path_downloads):
            if not os.path.exists(path_destination):
                os.mkdir(path_destination)
            for extension in extensions:
                for file_path in glob.glob(self.path_downloads+"/*"+extension):
                    os.system(f'move {file_path} {path_destination}')
            print("done!")
        else:
            print("something goes wrong!")


    def __init__(self):
        configurator = config_module.Configurator()
        self.config = configurator.load_config("Sorter/config.json")
        self.path_downloads = self.config["path_downloads"]
        for rule in self.config["rules"]:
            self.sort(rule[0], rule[1:])
