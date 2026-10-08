import wx
from pubsub import pub
from wx.dataview import DataViewListCtrl
from Utils.config import Config
from Utils.sorter import Sorter
from GUI import viewModifyRule, viewRemove, viewAddRule


class RuleWindow(wx.Frame):

    @property
    def currentRule(self) -> dict:
        return self.config.rulesList[self.ruleIndex]

    def onBtnDownloadFolder(self, event) -> None:

        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            selectedPath = dlg.GetPath()
            self.textBoxDownloadFolder.SetValue(selectedPath)
            self.currentRule["sourceFolder"] = selectedPath
            self.SetStatusText("Source folder set. Save to keep changes.")
        else:
            self.SetStatusText("Source folder selection cancelled.")
        dlg.Destroy()

    def onBtnAddItem(self, event) -> None:

        addRuleWindow = viewAddRule.AddRuleWindow()
        addRuleWindow.Show()
        self.SetStatusText("Add a destination folder.")

    def onBtnRemoveItem(self, event) -> None:

        selectedRow: int = self.dataView.GetSelectedRow()
        if 0 <= selectedRow < len(self.currentRule["destinationFolders"]):
            removeRuleWindow = viewRemove.RemoveRule(selectedRow)
            removeRuleWindow.Show()
        else:
            self.SetStatusText("No destination selected. Select one to remove.")

    def onBtnModifyItem(self, event) -> None:

        selectedRow: int = self.dataView.GetSelectedRow()
        if 0 <= selectedRow < len(self.currentRule["destinationFolders"]):
            modifyRuleWindow = viewModifyRule.ModifyRuleWindow(selectedRow, self.currentRule["destinationFolders"][selectedRow])
            modifyRuleWindow.Show()
        else:
            self.SetStatusText("No destination selected. Select one to modify.")

    def onBtnRunManual(self, event) -> None:

        self.sorter.ruleList = self.config.rulesList
        result = self.sorter.sortAll()
        self.SetStatusText(
            f'Manual run: {result["successCount"]} succeeded, '
            f'{result["failCount"]} failed. {result["message"]}'
        )

    def onBtnStartInterval(self, event) -> None:

        self.currentRule["isIntervalRunning"] = not self.currentRule["isIntervalRunning"]
        self.updateStatusLabel()

        state = "enabled" if self.currentRule["isIntervalRunning"] else "disabled"
        self.SetStatusText(f"Background run {state}. Save to apply.")

    def onBtnSave(self, event) -> None:

        self.config.saveConfig()
        pub.sendMessage("setStatusListener", message="Rule saved.")
        pub.sendMessage("reRender")
        self.Destroy()

    def listenerAddRule(self, data) -> None:

        self.dataView.AppendItem([data["destinationPath"], " ".join(data["extensions"])])
        self.currentRule["destinationFolders"].append(data)

        self.SetStatusText(f'Destination folder added: {data["destinationPath"]}')

    def listenerModifyRule(self, data) -> None:

        ruleId = data["id"]
        self.dataView.SetValue(data["destinationPath"], ruleId, 0)
        self.dataView.SetValue(" ".join(data["extensions"]), ruleId, 1)
        self.currentRule["destinationFolders"][ruleId] = data

        self.SetStatusText(f"Destination number {ruleId} has been changed.")

    def listenerRemoveRule(self, id) -> None:

        self.dataView.DeleteItem(id)
        self.currentRule["destinationFolders"].pop(id)

        self.SetStatusText(f"Destination number {id} has been removed.")

    def updateStatusLabel(self) -> None:
        if self.currentRule["isIntervalRunning"]:
            self.lblStatus.SetLabel("Background: ON")
            self.lblStatus.SetForegroundColour(wx.Colour(0, 150, 0))
        else:
            self.lblStatus.SetLabel("Background: OFF")
            self.lblStatus.SetForegroundColour(wx.Colour(200, 0, 0))
        self.lblStatus.Refresh()

    def render(self) -> None:

        self.panel.DestroyChildren()

        self.textStep1 = wx.StaticText(self.panel, label="Step 1: Choose your Downloads folder")
        self.textStep2 = wx.StaticText(self.panel, label="Step 2: Set up destination folders and their extensions")
        self.textStep3 = wx.StaticText(self.panel, label="Step 3: Run")

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)

        self.hboxDownloads = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxDataViewControls = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxStep3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxSaveControls = wx.BoxSizer(wx.HORIZONTAL)

        self.btnDownloadFolder = wx.Button(self.panel, label="Browse")
        self.btnDownloadFolder.Bind(wx.EVT_BUTTON, self.onBtnDownloadFolder)

        self.btnAddItem = wx.Button(self.panel, label="Add")
        self.btnAddItem.Bind(wx.EVT_BUTTON, self.onBtnAddItem)

        self.btnRemoveItem = wx.Button(self.panel, label="Remove")
        self.btnRemoveItem.Bind(wx.EVT_BUTTON, self.onBtnRemoveItem)

        self.btnModifyItem = wx.Button(self.panel, label="Modify")
        self.btnModifyItem.Bind(wx.EVT_BUTTON, self.onBtnModifyItem)

        self.btnSave = wx.Button(self.panel, label="Save")
        self.btnSave.Bind(wx.EVT_BUTTON, self.onBtnSave)

        self.btnInterval = wx.Button(self.panel, label="Toggle Background")
        self.btnInterval.Bind(wx.EVT_BUTTON, self.onBtnStartInterval)

        self.btnRunManual = wx.Button(self.panel, label="Run once")
        self.btnRunManual.Bind(wx.EVT_BUTTON, self.onBtnRunManual)

        self.textBoxDownloadFolder = wx.TextCtrl(self.panel)
        self.textBoxDownloadFolder.SetValue(self.currentRule["sourceFolder"])

        self.dataView = DataViewListCtrl(self.panel, size=(400, 200))
        self.dataView.AppendTextColumn("Folder Path", width=225)
        self.dataView.AppendTextColumn("Extensions")
        for destinationFolder in self.currentRule["destinationFolders"]:
            self.dataView.AppendItem([destinationFolder["destinationPath"], " ".join(destinationFolder["extensions"])])

        # Step 1
        self.sizerMain.Add(self.textStep1, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))

        self.hboxDownloads.Add(self.textBoxDownloadFolder, proportion=1)
        self.hboxDownloads.Add(self.btnDownloadFolder, wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5))
        self.sizerMain.Add(self.hboxDownloads, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        # Step 2
        self.sizerMain.Add(self.textStep2, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.dataView, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.hboxDataViewControls.Add(self.btnAddItem, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxDataViewControls.Add(self.btnRemoveItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxDataViewControls.Add(self.btnModifyItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxDataViewControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # Step 3
        self.hboxStep3.Add(self.textStep3, flag=wx.ALIGN_CENTER_VERTICAL)
        self.hboxStep3.AddStretchSpacer(1)
        self.lblStatus = wx.StaticText(self.panel, label="")
        font = self.lblStatus.GetFont()
        font.MakeBold()
        self.lblStatus.SetFont(font)
        self.hboxStep3.Add(self.lblStatus, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizerMain.Add(self.hboxStep3, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.hboxSaveControls.Add(self.btnSave, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.hboxSaveControls.Add(self.btnInterval, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.hboxSaveControls.Add(self.btnRunManual, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))
        self.sizerMain.Add(self.hboxSaveControls, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.updateStatusLabel()
        self.Center()

    def __init__(self, ruleIndex: int) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.SetMinSize((200, 300))

        self.ruleIndex = ruleIndex

        self.config = Config()
        self.sorter = Sorter(self.config)

        pub.subscribe(self.listenerAddRule, "addRuleListener")
        pub.subscribe(self.listenerModifyRule, "modifyRuleListener")
        pub.subscribe(self.listenerRemoveRule, "removeRuleListener")

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")

        self.render()

        self.Show(True)


def renderGui(ruleIndex: int):
    app = wx.App()
    ruleWindow = RuleWindow(ruleIndex)
    app.MainLoop()


if __name__ == "__main__":

    renderGui()