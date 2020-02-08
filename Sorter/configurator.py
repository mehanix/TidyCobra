''' Manipulates configuration files for TidyCobra '''
from wx.lib.pubsub import pub
import json
class Configurator():


    def listener_configurator(self, message, arg2=None):
        print(message)

        ### Save config ###
        if message == "save_config":
            print("received=",arg2)
            with open('../Sorter/config.json', 'w+') as f:
                json.dump(arg2,f)
            print("done")
        ### Load config ###
        elif message == "import_config":
            #TODO:implement
            return -1

    def load_config(self,path):
        with open(path) as f:
            config = json.load(f)
            return config

    def __init__(self):

        data = []
        pub.subscribe(self.listener_configurator, "configuratorListener")


