import wx

class MainWindow(wx.Frame):
    ''' Fereastra principala (sper eu ca si singura) '''

    def onBtnDownloadFolder(self,event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print ("You chose %s" % dlg.GetPath())
        dlg.Destroy()


    def __init__(self):
        wx.Frame.__init__(self,None,title="Tidy Cobra", size=(500,500))
        panel = wx.Panel(self)

        ''' Logo '''
        img_logo = wx.Image("../Resources/logo.png", wx.BITMAP_TYPE_ANY)
        sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img_logo))
        ''' Text labels '''
        text_step1 = wx.StaticText(panel, label = "Step 1: Choose your Downloads folder")
        text_step2 = wx.StaticText(panel, label = "Step 2: Set up destination folders & extensions")
        text_step3 = wx.StaticText(panel, label= "Step 3: Save/Run")


        ''' Dividers '''
        sizer_main = wx.BoxSizer(wx.VERTICAL) # main sizer
        hbox_downloads = wx.BoxSizer(wx.HORIZONTAL)


        ''' Dialogs '''
        dlg = wx.DirDialog(None, "Choose input directory", "",  wx.DD_DIR_MUST_EXIST)

        ''' Buttons '''
        btn_download_folder = wx.Button(panel, label = "Browse")
        btn_download_folder.Bind(wx.EVT_BUTTON, self.onBtnDownloadFolder)

        ''' Textboxes '''
        textbox_download_folder = wx.TextCtrl(panel)



        ''' Layout '''
        sizer_main.Add(sb1, wx.SizerFlags().Border(wx.TOP | wx.BOTTOM, 20).Center())

        ''' Step 1 : Select download folder'''
        sizer_main.Add(text_step1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        hbox_downloads.Add(textbox_download_folder,proportion=1)
        hbox_downloads.Add(btn_download_folder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))

        sizer_main.Add(hbox_downloads,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        sizer_main.Add(text_step2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        sizer_main.Add(text_step3, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        panel.SetSizer(sizer_main)

        self.Center()
        self.Show(True)
def render_GUI():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()

render_GUI()