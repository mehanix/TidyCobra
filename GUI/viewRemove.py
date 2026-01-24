import wx
from pubsub import pub

class RemoveRule(wx.Frame):

    def onBtnConfirm(self,event) -> None:

        pub.sendMessage("removeRuleListener",id=self.id)
        self.Destroy()

    def onBtnCancel(self,event) -> None:

        self.Destroy()
    
    def __init__(self, id:int, ruleData:dict) -> None:
        wx.Frame.__init__(self, None, title="Remove rule", style=wx.DEFAULT_DIALOG_STYLE & ~wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)
        self.id: int = id
        
        ''' Path and extensions info of the rule to be removed '''
        folder_pth = ruleData["destinationPath"]
        extensions = " ".join(ruleData["extensions"])

        '''Sizers'''
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.operationsBox = wx.BoxSizer(wx.HORIZONTAL)

        '''Labels'''
        infoText = f"You are about to remove the following rule:\n\nFolder Path: {folder_pth}\nExtensions: {extensions}\n\nAre you sure you want to proceed?"
        self.message= wx.StaticText(self.panel, label=infoText)
        self.vbox.Add(self.message, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        '''Buttons'''
        self.btnConfirm= wx.Button(self.panel, label="Yes")
        self.btnConfirm.Bind(wx.EVT_BUTTON, self.onBtnConfirm)
        self.btnCancel = wx.Button(self.panel, label="No")
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancel)
        self.operationsBox.Add(self.btnConfirm, flag=wx.RIGHT|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)
        self.operationsBox.Add(self.btnCancel, flag=wx.RIGHT|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)
        self.vbox.Add(self.operationsBox, flag=wx.CENTER|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        self.panel.SetSizer(self.vbox)
        self.Center()
        self.SetSize(self.GetBestSize())
        self.vbox.Fit(self)
        self.vbox.Layout()
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        
        try:
            icon = wx.Icon("Assets/SNAKE.png", wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        except Exception as e:
            print("Could not load icon:", e)



        self.Show(True)