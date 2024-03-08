import wx
from pubsub import pub

class AddRuleWindow(wx.Frame):
    def OnBtnBrowse(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.textbox_folder_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def OnBtnSave(self, event):
        data = [self.textbox_folder_path.GetValue(), self.textbox_extensions.GetValue()]

        # send data
        pub.sendMessage("addRuleListener", message=data)
        self.Destroy()

    def __init__(self):
        super().__init__(None, title="Add rule", style=wx.DEFAULT_DIALOG_STYLE & ~wx.RESIZE_BORDER)
        self.panel = wx.Panel(self)

        '''Sizers'''
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox_path = wx.BoxSizer(wx.HORIZONTAL)

        '''Labels'''
        self.label_folder_path = wx.StaticText(self.panel, label="Select folder path:")
        self.label_extensions = wx.StaticText(self.panel, label="Specify file extensions to reroute: (separated by spaces)")

        '''Textboxes'''
        self.textbox_folder_path = wx.TextCtrl(self.panel, size=(300, -1))
        self.textbox_extensions = wx.TextCtrl(self.panel)

        '''Buttons'''
        self.btn_browse_folder = wx.Button(self.panel, label="Browse")
        self.btn_browse_folder.Bind(wx.EVT_BUTTON, self.OnBtnBrowse)
        self.btn_save = wx.Button(self.panel, label="Save")
        self.btn_save.Bind(wx.EVT_BUTTON, self.OnBtnSave)

        '''Layout'''
        # Select path
        self.vbox.Add(self.label_folder_path, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.hbox_path.Add(self.textbox_folder_path, proportion=1)
        self.hbox_path.Add(self.btn_browse_folder, wx.SizerFlags().Border(wx.LEFT, 5))
        self.vbox.Add(self.hbox_path, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        # Set extensions
        self.vbox.Add(self.label_extensions, flag=wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.vbox.Add(self.textbox_extensions, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        # Save
        self.vbox.Add(self.btn_save, flag=wx.CENTER|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        self.panel.SetSizer(self.vbox)
        self.Center()
        self.SetSize(self.GetBestSize())
        self.vbox.Fit(self)
        self.vbox.Layout()
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

        self.Show(True)

if __name__ == "__main__":
    app = wx.App()
    frame = AddRuleWindow()
    app.MainLoop()
