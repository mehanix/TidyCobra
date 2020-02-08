''' Manipulates configuration files for TidyCobra '''
from wx.lib.pubsub import pub
import wx
class Configurator():


    def listener_configurator(self, message, arg2=None):
        print(message)
        if message == "save_config":
            print("received=",arg2)
            return -1 #save configuration
        elif message == "import_config":
            return -1


    def __init__(self):

        data = []
        pub.subscribe(self.listener_configurator, "configuratorListener")


