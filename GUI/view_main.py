import wx
import wx.dataview
from GUI import view_addrule
from wx.lib.pubsub import pub
from Sorter import configurator as config_tool
from Sorter import sorter as sorter_tool
import os.path

class MainWindow(wx.Frame):
    ''' Fereastra principala '''
    config = config_tool.Configurator()

    def getSetupData(self):
        data = dict()
        data["path_downloads"]=self.textbox_download_folder.GetValue()
        rules = []
        for row in range(self.dataview.GetItemCount()):
            temp_row = []
            for col in range(2):
                temp_row.append(self.dataview.GetValue(row,col))

            rules.append(temp_row)

        data["rules"]=rules
        print(data)
        return data

    def OnBtnDownloadFolder(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.textbox_download_folder.SetValue(dlg.GetPath())
        dlg.Destroy()

    def OnBtnAddItem(self, event):
        add_rule_window = view_addrule.AddRuleWindow()
        add_rule_window.Show()

    def OnBtnRemoveItem(self, event):
        selected_item = self.dataview.GetSelectedRow()
        self.dataview.DeleteItem(selected_item)



    def OnBtnImportConfig(self, event):
        return -1  # not implemented

    def OnBtnSaveConfig(self, event):
        data = self.getSetupData()
        pub.sendMessage("configuratorListener", message="save_config", arg2=data)
        self.SetStatusText("Configuration saved!")


    def OnBtnRunManual(self, event):
        sorter = sorter_tool.Sorter()


        return -1  # not implemented

    def OnBtnRunAuto(self, event):
        return -1  # not implemented


    '''Listeners!'''
    def listener_addrule(self, message, arg2=None):
        self.dataview.AppendItem(message)



    def __init__(self):
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER
                                                                                           | wx.MAXIMIZE_BOX))

        self.payload = []
        self.SetMinSize(self.GetSize())
        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")
        pub.subscribe(self.listener_addrule, "addRuleListener")



        ''' Logo '''
        self.img_logo = wx.Image("../Resources/logo.png", wx.BITMAP_TYPE_ANY)
        self.sb1 = wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(self.img_logo))
        ''' Text labels '''

        self.text_step1 = wx.StaticText(self.panel, label="Step 1: Choose your Downloads folder")
        self.text_step2 = wx.StaticText(self.panel, label="Step 2: Set up destination folders and their extensions")
        self.text_step3 = wx.StaticText(self.panel, label="Step 3: Save/Run")

        ''' Dividers '''
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)  # main sizer

        '''horizontal boxes'''
        self.hbox_downloads = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_dataview_controls = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_save_controls = wx.BoxSizer(wx.HORIZONTAL)

        ''' Dialogs '''
        self.dialog_step1 = wx.DirDialog(None, "Choose input directory", "", wx.DD_DIR_MUST_EXIST)

        ''' Buttons '''
        self.btn_download_folder = wx.Button(self.panel, label="Browse")
        self.btn_download_folder.Bind(wx.EVT_BUTTON, self.OnBtnDownloadFolder)

        self.btn_add_item = wx.Button(self.panel, label="Add rule")
        self.btn_add_item.Bind(wx.EVT_BUTTON, self.OnBtnAddItem)

        self.btn_remove_item = wx.Button(self.panel, label="Remove selected")
        self.btn_remove_item.Bind(wx.EVT_BUTTON, self.OnBtnRemoveItem)

        self.btn_import_config = wx.Button(self.panel, label="Import configuration")
        self.btn_import_config.Bind(wx.EVT_BUTTON, self.OnBtnImportConfig)

        self.btn_save_config = wx.Button(self.panel, label="Save configuration file")
        self.btn_save_config.Bind(wx.EVT_BUTTON, self.OnBtnSaveConfig)

        self.btn_run_manual = wx.Button(self.panel, label="Run sorter")
        self.btn_run_manual.Bind(wx.EVT_BUTTON, self.OnBtnRunManual)

        self.btn_run_auto = wx.Button(self.panel, label="Run on startup")
        self.btn_run_auto.Bind(wx.EVT_BUTTON, self.OnBtnRunAuto)

        ''' Textboxes '''
        self.textbox_download_folder = wx.TextCtrl(self.panel)

        ''' DataView '''
        self.dataview = wx.dataview.DataViewListCtrl(self.panel, size=(200, 200))

        self.dataview.AppendTextColumn("Folder Path", width=225)
        self.dataview.AppendTextColumn("Extensions")



        ''' Layout '''
        self.sizer_main.Add(self.sb1, wx.SizerFlags().Border(wx.TOP | wx.BOTTOM, 20).Center())

        ''' Step 1 : Select download folder'''
        self.sizer_main.Add(self.text_step1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        self.hbox_downloads.Add(self.textbox_download_folder, proportion=1)
        self.hbox_downloads.Add(self.btn_download_folder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))
        self.sizer_main.Add(self.hbox_downloads, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        ''' Step 2: Set up rules '''
        self.sizer_main.Add(self.text_step2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizer_main.Add(self.dataview, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.hbox_dataview_controls.Add(self.btn_add_item, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hbox_dataview_controls.Add(self.btn_remove_item, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hbox_dataview_controls.Add(self.btn_import_config, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizer_main.Add(self.hbox_dataview_controls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        ''' Step 3: Save/Run '''
        self.sizer_main.Add(self.text_step3, wx.SizerFlags().Border(wx.TOP | wx.LEFT | wx.BOTTOM, 10))

        self.hbox_save_controls.Add(self.btn_save_config, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hbox_save_controls.Add(self.btn_run_manual, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hbox_save_controls.Add(self.btn_run_auto, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizer_main.Add(self.hbox_save_controls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizer_main)

        self.panel.SetSizer(self.sizer_main)
        self.Center()
        self.SetSize(self.GetBestSize())
        self.sizer_main.Fit(self)
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.Center()

        self.default_config_path = '../Sorter/config.json'
        if os.path.isfile(self.default_config_path):
            config_display_data = self.config.load_config(self.default_config_path)
            self.textbox_download_folder.SetValue(config_display_data["path_downloads"])
            for rule in config_display_data["rules"]:
                print(rule)
                self.dataview.AppendItem(rule)
                self.SetStatusText("Loaded pre-existent configuration. Ready!")
        else:
            self.SetStatusText("Ready!")
        self.Show(True)


def render_GUI():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()


render_GUI()
