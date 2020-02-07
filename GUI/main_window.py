import wx
import wx.dataview
class MainWindow(wx.Frame):
    ''' Fereastra principala (sper eu ca si singura) '''

    def onBtnDownloadFolder(self,event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print ("You chose %s" % dlg.GetPath())
        dlg.Destroy()


    def __init__(self):
        wx.Frame.__init__(self,None,title="Tidy Cobra", size=(500,700))
        self.SetMinSize(self.GetSize())
        panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")

        ''' Logo '''
        img_logo = wx.Image("../Resources/logo.png", wx.BITMAP_TYPE_ANY)
        sb1 = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(img_logo))
        ''' Text labels '''
        text_step1 = wx.StaticText(panel, label = "Step 1: Choose your Downloads folder")
        text_step2 = wx.StaticText(panel, label = "Step 2: Set up destination folders and their extensions")
        text_step3 = wx.StaticText(panel, label= "Step 3: Save/Run")


        ''' Dividers '''
        sizer_main = wx.BoxSizer(wx.VERTICAL) # main sizer

        '''horizontal boxes'''
        hbox_downloads = wx.BoxSizer(wx.HORIZONTAL)
        hbox_dataview_controls = wx.BoxSizer(wx.HORIZONTAL)
        hbox_save_controls = wx.BoxSizer(wx.HORIZONTAL)

        ''' Dialogs '''
        dlg = wx.DirDialog(None, "Choose input directory", "",  wx.DD_DIR_MUST_EXIST)

        ''' Buttons '''
        btn_download_folder = wx.Button(panel, label = "Browse")
        btn_download_folder.Bind(wx.EVT_BUTTON, self.onBtnDownloadFolder)
        btn_add_item = wx.Button(panel, label = "Add rule")
        btn_remove_item = wx.Button(panel, label = "Remove selected")
        btn_import_config = wx.Button(panel, label = "Import configuration")


        btn_save_config = wx.Button(panel, label = "Save configuration file")
        btn_run_manual = wx.Button(panel, label = "Run sorter")
        btn_run_auto = wx.Button(panel, label = "Run on startup")




        ''' Textboxes '''
        textbox_download_folder = wx.TextCtrl(panel)

        ''' DataView '''
        dataview = wx.dataview.DataViewListCtrl(panel,size=(200,200))

        dataview.AppendTextColumn("Folder Path",width=225)
        dataview.AppendTextColumn("Extensions")

        data = ["/home/nix/Documents", ".txt .pdf"]
        dataview.AppendItem(data)

        data = ["/home/nix/Pictures", ".jpg .png"]
        dataview.AppendItem(data)

        ''' Layout '''
        sizer_main.Add(sb1, wx.SizerFlags().Border(wx.TOP | wx.BOTTOM, 20).Center())

        ''' Step 1 : Select download folder'''
        sizer_main.Add(text_step1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        hbox_downloads.Add(textbox_download_folder,proportion=1)
        hbox_downloads.Add(btn_download_folder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))
        sizer_main.Add(hbox_downloads,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP | wx.BOTTOM, border=10)

        ''' Step 2: Set up rules '''
        sizer_main.Add(text_step2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        sizer_main.Add(dataview, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)
        hbox_dataview_controls.Add(btn_add_item, wx.SizerFlags().Border( wx.RIGHT, 2).Proportion(1))
        hbox_dataview_controls.Add(btn_remove_item, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        hbox_dataview_controls.Add(btn_import_config, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        sizer_main.Add(hbox_dataview_controls,flag=wx.EXPAND|wx.LEFT|wx.RIGHT| wx.BOTTOM, border=10)

        ''' Step 3: Save/Run '''
        sizer_main.Add(text_step3, wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.BOTTOM, 10))

        hbox_save_controls.Add(btn_save_config, wx.SizerFlags().Border( wx.RIGHT, 2).Proportion(1))
        hbox_save_controls.Add(btn_run_manual, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        hbox_save_controls.Add(btn_run_auto, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        sizer_main.Add(hbox_save_controls,flag=wx.EXPAND|wx.LEFT|wx.RIGHT| wx.BOTTOM, border=10)


        panel.SetSizer(sizer_main)

        self.Center()
        self.Show(True)
def render_GUI():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()

render_GUI()