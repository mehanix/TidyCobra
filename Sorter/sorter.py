from Sorter import configurator as config_module


class Sorter:
    def __init__(self):

        configurator = config_module.Configurator()
        self.config = configurator.load_config("../Sorter/config.json")
        self.path_downloads = self.config["path_downloads"]

        for rule in self.config["rules"]:
            path = rule[0]
            extensions = rule[1].split(' ')
            print(path,extensions)