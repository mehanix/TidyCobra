from json import load, dump
from os import path

configTemplate: dict = {
    "version": "0.0.1",
    "startup": False,
    "interval": 15000,
    "rulesList": [
        {
            "sourceFolder": path.join(path.expanduser("~"), "Downloads"),
            "destinationFolders": [
                {
                    "extensions": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
                    "destinationPath": path.join(path.expanduser("~"), "Pictures")
                },
                {
                    "extensions": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
                    "destinationPath": path.join(path.expanduser("~"), "Documents")
                },
                {
                    "extensions": [".mp3", ".wav", ".flac", ".aac"],
                    "destinationPath": path.join(path.expanduser("~"), "Music")
                },
                {
                    "extensions": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
                    "destinationPath": path.join(path.expanduser("~"), "Videos")
                },
                {
                    "extensions": [".zip", ".rar", ".7z", ".tar", ".gz"],
                    "destinationPath": path.join(path.expanduser("~"), "Documents")
                }
            ],
            "isIntervalRunning": False
        }
    ]
}


class Config:

    def saveConfig(self) -> None:
        
        with open(self.configFilePath, 'w') as configFile:
            dump({
                    "version":"0.0.1",
                    "interval":self.interval,
                    "startup": self.startup,
                    "rulesList": self.rulesList
                }, configFile)


    def loadConfig(self,configFilePath:str) -> None:

        with open(configFilePath, 'r') as configFile:
            dummy:dict = load(configFile)

        if "rules" in dummy.keys():
            # old config format support
            self.isIntervalRunning: bool = False
            self.interval: int = 15000
            self.startup: bool = False
            self.rulesList: list = [
                {
                    "sourceFolder": dummy["path_downloads"],
                    "destinationFolders": [
                        {
                            "destinationPath": rule[0],
                            "extensions": rule[1].split(" ")
                        }
                        for rule in dummy["rules"]
                    ],
                    "isIntervalRunning": False
                }
            ]
        elif not "version" in dummy:
            # support for before versioning
            self.interval: int = dummy["interval"]
            self.startup: bool = dummy["startup"]
            self.rulesList: list = dummy["rulesList"]
            for rule in self.rulesList: rule["isIntervalRunning"] = False
        else:
            self.interval: int = dummy["interval"]
            self.startup: bool = dummy["startup"]
            self.rulesList: list = dummy["rulesList"]
            

    def __init__(self, configFilePath: str = "./config.json") -> None:

        if not path.isfile(configFilePath):

            with open(configFilePath, 'w+') as configFile:
                dump(configTemplate, configFile)
        self.configFilePath = configFilePath
        self.loadConfig(self.configFilePath)