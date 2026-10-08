import wx
from pubsub import pub

class RemoveRule(wx.Frame):

    def onBtnConfirm(self,event) -> None:

        pub.sendMessage(
            "removeFolderListener" if self.folder else "removeRuleListener",
            id=self.id
        )
        self.Destroy()

    def onBtnCancel(self,event) -> None:

        self.Destroy()
    
    def __init__(self, id:int,folder:bool=False) -> None:
        wx.Frame.__init__(self, None, title="Remove rule", style=wx.DEFAULT_DIALOG_STYLE & ~wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)
        self.id: int = id
        self.folder: bool = folder

        '''Sizers'''
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.operationsBox = wx.BoxSizer(wx.HORIZONTAL)

        '''Labels'''
        self.message= wx.StaticText(self.panel, label=f"Are you sure you want to delete this {"folder" if self.folder else "rule"}?")
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



        self.Show(True)