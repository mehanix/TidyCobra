from Utils.config import Config
from glob import glob
from shutil import move
from os import path

def sortFolderByExtensions(rule: dict) -> dict:

    successCount:int = 0
    failCount:int = 0
    message:str = "Success!"

    #  rule format:
    #  {
    #      "sourceFolder": "<path to source folder>",
    #      "destinationFolders": [
    #           {
    #               "extensions": [<file extensions like pdf, png, ...>],
    #               "destinationPath": "<path where file should go>"
    #           },
    #           ...
    #      ]
    #  }, ...

    sourceFolder:str = rule["sourceFolder"]
    if not sourceFolder or not path.isdir(sourceFolder):
        return {
            "successCount": successCount,
            "failCount": failCount,
            "message": f"Failed! The source folder ({sourceFolder}) does not exist."
        }
        
    extensionsMapping:dict = {}
    for folder in rule["destinationFolders"]:
        for extension in folder["extensions"]:

            if extension in extensionsMapping.keys():
                continue

            if not path.isdir(folder["destinationPath"]):
                continue

            extensionsMapping[extension] = folder["destinationPath"]

    files:list = glob(f'{sourceFolder}/*')
    for file in files:
        fileExtension:str = "."+file.split('.')[-1]

        if not fileExtension in extensionsMapping.keys():
            continue
        
        fileName:str = path.basename(file)
        newFilePath:str = f'{extensionsMapping[fileExtension]}/{fileName}'

        i:int = 1
        while path.isfile(newFilePath):
            newFilePath = f'{extensionsMapping[fileExtension]}/d{i}_{fileName}'
            i += 1

        try:
            move(file,newFilePath)
            successCount += 1
        except PermissionError:
            message = "Access denied for some files!"
            failCount += 1
        except OSError as e:
            message = f"Failed to move some files: {str(e)}"
            failCount += 1
#new except added to the try-except block to handle OSError better and avoid corrupting files
    return {
        "successCount": successCount,
        "failCount": failCount,
        "message": message
    }

class Sorter:

    def sortAll(self) -> dict:

        successCount:int = 0
        failCount:int = 0

        areAllEndSuccessfully:bool = True
        ruleFailMessage:str 

        for rule in self.ruleList:
            result = sortFolderByExtensions(rule)
            successCount += result['successCount']
            failCount += result['failCount']
            if result['message'] != "Success!":
                areAllEndSuccessfully = False
                ruleFailMessage = result['message']

        if areAllEndSuccessfully:
            return {
                    "successCount": successCount,
                    "failCount": failCount,
                    "message": "Success!"
                }
        else:
            return {
                    "successCount": successCount,
                    "failCount": failCount,
                    "message": ruleFailMessage
                }

    def __init__(self, config: Config) -> None:
        self.ruleList: list = config.rulesList
