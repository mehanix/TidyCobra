import wx
import wx.dataview
from pubsub import pub
from Utils.config import Config
from Utils.sorter import Sorter
from GUI import viewModifyRule,viewRemove,viewAddRule

class MainWindow(wx.Frame):

    def onBtnDownloadFolder(self, event) -> None:

        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.textBoxDownloadFolder.SetValue(dlg.GetPath())
            self.config.rulesList[0]["sourceFolder"] = dlg.GetPath()
        dlg.Destroy()

    def onBtnAddItem(self, event) -> None:

        addRuleWindow = viewAddRule.AddRuleWindow()
        addRuleWindow.Show()

    def onBtnRemoveItem(self, event) -> None:

        selectedItem:int = self.dataView.GetSelectedRow()
        selectedItem:int = self.dataView.GetSelectedRow()
        rules_list = self.config.rulesList[0]["destinationFolders"]
        if 0 <= selectedItem <= len(rules_list):
            # Get the selected to be removed rule's data for display in the confirmation dialog
            ruleData = rules_list[selectedItem]
            removeRuleWindow = viewRemove.RemoveRule(selectedItem, ruleData)
            removeRuleWindow.Show()
        else:
            wx.MessageBox("Please select a folder to remove!","Error",wx.OK| wx.ICON_WARNING)
            self.SetStatusText("No selected item.")

    def onBtnModifyItem(self, event) -> None:
        
        selectedItem:int = self.dataView.GetSelectedRow()
        if 0 <= selectedItem <= len(self.config.rulesList[0]["destinationFolders"]):
            modifyRuleWindow = viewModifyRule.ModifyRuleWindow(selectedItem,self.config.rulesList[0]["destinationFolders"][selectedItem])
            modifyRuleWindow.Show()
        else:
            wx.MessageBox("Please select a rule to modify!","Error",wx.OK|wx.ICON_WARNING)
            self.SetStatusText("No selected item.")

    def onBtnRunManual(self, event) -> None:
        
        self.sorter.ruleList = self.config.rulesList
        result = self.sorter.sortAll()

        self.SetStatusText(f's:{result["successCount"]} f:{result["failCount"]} {result["message"]}')

    def onBtnStartInterval(self,event) -> None:
        
        if self.config.isIntervalRunning:
            self.config.isIntervalRunning = False
            if hasattr(self, "timer"):
                self.timer.Stop()
        else:
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onInterval, self.timer)
            self.timer.Start(self.config.interval)
            self.config.isIntervalRunning = True
        
        self.updateStatusLabel()

    def onBtnLoadConfig(self,event) -> None:
        dlg = wx.FileDialog(self, "Choose a file:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            filePath = dlg.GetPath()
            try:
                self.config.loadConfig(filePath)
                self.SetStatusText(f"{filePath} config file loaded.")
            except:
                self.SetStatusText(f"Failed to load config.")
            self.render()
        else:
            self.SetStatusText(f"Failed to load config.")

    def onInterval(self,event) -> None:

        self.sorter.ruleList = self.config.rulesList
        result = self.sorter.sortAll()

        self.SetStatusText(f'Interval: s:{result["successCount"]} f:{result["failCount"]} {result["message"]}')

    def onClose(self,event) -> None:

        self.config.saveConfig()
        self.Destroy()

    def listenerAddRule(self, data) -> None:

        self.dataView.AppendItem([data["destinationPath"]," ".join(data["extensions"])])
        self.config.rulesList[0]["destinationFolders"].append(data)

        self.SetStatusText('New element has been added.')

    def listenerModifyRule(self, data) -> None:
 
        self.dataView.SetValue(data["destinationPath"],data["id"],0)
        self.dataView.SetValue(" ".join(data["extensions"]),data["id"],1)
        self.config.rulesList[0]["destinationFolders"][data["id"]] = data

        self.SetStatusText(f'Item number {data['id']} has been changed.')

    def listenerRemoveRule(self, id) -> None:

        self.dataView.DeleteItem(id)
        self.config.rulesList[0]["destinationFolders"].pop(id)

        self.SetStatusText(f'Item number {id} has been removed.')

    def updateStatusLabel(self) -> None:
        if self.config.isIntervalRunning:
            self.lblStatus.SetLabel("Background Sorting: ON")
            self.lblStatus.SetForegroundColour(wx.Colour(0, 150, 0))
        else:
            self.lblStatus.SetLabel("Background Sorting: OFF")
            self.lblStatus.SetForegroundColour(wx.Colour(200, 0, 0))
        self.lblStatus.Refresh()

    def render(self) -> None:

        self.panel.DestroyChildren()
        if hasattr(self, "timer"):
            self.timer.Stop()
            
        ''' Text labels '''
        self.textStep1 = wx.StaticText(self.panel, label="Step 1: Choose your Downloads folder")
        self.textStep2 = wx.StaticText(self.panel, label="Step 2: Set up destination folders and their extensions")
        self.textStep3 = wx.StaticText(self.panel, label="Step 3: Run")
        headerFont = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.textStep1.SetFont(headerFont)
        self.textStep2.SetFont(headerFont)
        self.textStep3.SetFont(headerFont)

        ''' Dividers '''
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)  # main sizer
        
        ''' Banner Image '''
        try:
            image = wx.Image("Assets/banner.png", wx.BITMAP_TYPE_PNG)
            image = image.Scale(600, 100, wx.IMAGE_QUALITY_HIGH)
            bannerBitmap = wx.Bitmap(image)
            self.bannerCtrl = wx.StaticBitmap(self.panel, bitmap=bannerBitmap)
            self.sizerMain.Add(self.bannerCtrl, flag=wx.TOP |  wx.ALIGN_CENTER_HORIZONTAL, border=10)
        except Exception as e:
            print("Could not load banner image:", e)
        

        ''' Horizontal boxes '''
        self.hboxDownloads = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxDataViewControls = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxSaveControls = wx.BoxSizer(wx.HORIZONTAL)

        ''' Dialogs '''
        self.dialogStep1 = wx.DirDialog(None, "Choose input directory", "", wx.DD_DIR_MUST_EXIST)

        ''' Buttons '''
        self.btnDownloadFolder = wx.Button(self.panel, label="Browse")
        self.btnDownloadFolder.Bind(wx.EVT_BUTTON, self.onBtnDownloadFolder)

        self.btnAddItem = wx.Button(self.panel, label="Add")
        self.btnAddItem.Bind(wx.EVT_BUTTON, self.onBtnAddItem)

        self.btnRemoveItem = wx.Button(self.panel, label="Remove")
        self.btnRemoveItem.Bind(wx.EVT_BUTTON, self.onBtnRemoveItem)

        self.btnModifyItem = wx.Button(self.panel, label="Modify")
        self.btnModifyItem.Bind(wx.EVT_BUTTON, self.onBtnModifyItem)
        
        if self.config.isIntervalRunning:
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onInterval, self.timer)
            self.timer.Start(self.config.interval)

        self.btnInterval = wx.Button(self.panel, label="Toggle Background")
        self.btnInterval.Bind(wx.EVT_BUTTON, self.onBtnStartInterval)

        self.btnRunManual = wx.Button(self.panel, label="Run once")
        self.btnRunManual.Bind(wx.EVT_BUTTON, self.onBtnRunManual)

        self.btnLoadConfig = wx.Button(self.panel, label="Load Config")
        self.btnLoadConfig.Bind(wx.EVT_BUTTON, self.onBtnLoadConfig)
        
        ''' Hover Tooltips for buttons '''
        self.btnAddItem.SetToolTip("Add a new destination folder and its extensions")
        self.btnModifyItem.SetToolTip("Modify the selected destination folder and its extensions")
        self.btnRemoveItem.SetToolTip("Remove the selected destination folder and its extensions")
        self.btnInterval.SetToolTip("Toggle background sorting on/off")
        self.btnRunManual.SetToolTip("Run sorting process once")
        self.btnLoadConfig.SetToolTip("Load a configuration file")
        
        ''' Textboxes '''
        self.textBoxDownloadFolder = wx.TextCtrl(self.panel)
        self.textBoxDownloadFolder.SetValue(self.config.rulesList[0]["sourceFolder"])

        ''' DataView '''
        # the data view to show rules list 
        self.dataView = wx.dataview.DataViewListCtrl(self.panel, style=wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES 
                                                     | wx.dataview.DV_HORIZ_RULES) #flexible size to fill space if user resizes window (before it was hardcoded and there would be empty spaces)
        self.dataView.SetMinSize((400, 200)) # minimum size to avoid being too small
        self.dataView.AppendTextColumn("Folder Path", width=225)
        self.dataView.AppendTextColumn("Extensions")
        for destinationFolder in self.config.rulesList[0]["destinationFolders"]:
            self.dataView.AppendItem([destinationFolder["destinationPath"]," ".join(destinationFolder["extensions"])])

        ''' Step 1 : Select download folder'''
        self.sizerMain.Add(self.textStep1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        self.hboxDownloads.Add(self.textBoxDownloadFolder, proportion=1)
        self.hboxDownloads.Add(self.btnDownloadFolder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))
        self.sizerMain.Add(self.hboxDownloads, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        ''' Step 2: Set up rules '''
        self.sizerMain.Add(self.textStep2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.dataView, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.hboxDataViewControls.Add(self.btnAddItem, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxDataViewControls.Add(self.btnRemoveItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxDataViewControls.Add(self.btnModifyItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxDataViewControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        ''' Step 3: Save/Run '''
        self.hboxStep3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxStep3.Add(self.textStep3, flag=wx.ALIGN_CENTER_VERTICAL)
        self.hboxStep3.AddStretchSpacer(1)
        self.lblStatus = wx.StaticText(self.panel, label="")
        font = self.lblStatus.GetFont()
        font.MakeBold()
        self.lblStatus.SetFont(font)
        self.hboxStep3.Add(self.lblStatus, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizerMain.Add(self.hboxStep3, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.hboxSaveControls.Add(self.btnInterval, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxSaveControls.Add(self.btnRunManual, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxSaveControls.Add(self.btnLoadConfig, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxSaveControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.updateStatusLabel() # moved this here to update after lblStatus creation so the label has text before we calculate its size and layout
        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.Center()

    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.config = Config()
        self.sorter = Sorter(self.config)

        pub.subscribe(self.listenerAddRule, "addRuleListener")
        pub.subscribe(self.listenerModifyRule, "modifyRuleListener")
        pub.subscribe(self.listenerRemoveRule, "removeRuleListener")

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        ''' Set Icon '''
        try:
            icon = wx.Icon("Assets/SNAKE.png", wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        except Exception as e:
            print("Could not load icon:", e)
            
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.SetStatusText("Ready!")
        
        self.render()
        self.SetMinSize(self.GetBestSize()) # set minimum size to best size (obtained after render) so that the user cannot resize it to be too small
        self.Show(True)

def renderGui():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()

if __name__ == "__main__":

    renderGui()
