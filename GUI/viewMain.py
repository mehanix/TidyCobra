import wx
from pubsub import pub
from wx.dataview import DataViewListCtrl
from Utils.config import Config
from Utils.sorter import Sorter
from GUI import viewRemove, viewRule, viewSettings


class MainWindow(wx.Frame):

    def onBtnSettings(self, event):
        self.SetStatusText("Settings opened.")
        viewSettings.renderGui()

    def onBtnRemoveItem(self, event):
        selectedRow: int = self.dataView.GetSelectedRow()
        if 0 <= selectedRow < len(self.config.rulesList):
            removeRuleWindow = viewRemove.RemoveRule(selectedRow, True)
            removeRuleWindow.Show()
        else:
            self.SetStatusText("No rule selected. Select a rule to remove.")

    def onBtnModifyItem(self, event):
        selectedRow: int = self.dataView.GetSelectedRow()
        if 0 <= selectedRow < len(self.config.rulesList):
            self.SetStatusText(f"Editing rule number {selectedRow}.")
            viewRule.renderGui(selectedRow)
        else:
            self.SetStatusText("No rule selected. Select a rule to modify.")

    def onBtnAddItem(self, event):
        newRuleIndex = len(self.config.rulesList)
        self.config.rulesList.append({
            "sourceFolder": "",
            "destinationFolders": [],
            "isIntervalRunning": False
        })
        self.config.saveConfig()
        self.SetStatusText(f"New rule number {newRuleIndex} created.")
        viewRule.renderGui(newRuleIndex)

    def onInterval(self, event):
        self.sorter.ruleList = self.config.rulesList
        result = self.sorter.sortAll()
        self.SetStatusText(
            f'Interval run: {result["successCount"]} succeeded, '
            f'{result["failCount"]} failed. {result["message"]}'
        )

    def listenerRemoveFolder(self, id):
        self.dataView.DeleteItem(id)
        self.config.rulesList.pop(id)
        self.config.saveConfig()
        self.SetStatusText(f"Rule number {id} has been removed.")

    def listenerSetStatus(self, message):
        self.SetStatusText(message)

    def render(self) -> None:

        self.panel.DestroyChildren()

        self.config = Config()
        self.sorter = Sorter(self.config)

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerModify = wx.BoxSizer(wx.HORIZONTAL)

        self.title = wx.StaticText(self.panel, label="TidyCobra")

        self.dataView = DataViewListCtrl(self.panel, size=(400, 200))
        self.dataView.AppendTextColumn("Folder", width=225)
        self.dataView.AppendTextColumn("Active")
        for rule in self.config.rulesList:
            self.dataView.AppendItem([rule["sourceFolder"], "yes" if rule["isIntervalRunning"] else "no"])

        self.btnAddItem = wx.Button(self.panel, label="Add")
        self.btnAddItem.Bind(wx.EVT_BUTTON, self.onBtnAddItem)
        self.btnRemoveItem = wx.Button(self.panel, label="Remove")
        self.btnRemoveItem.Bind(wx.EVT_BUTTON, self.onBtnRemoveItem)
        self.btnModifyItem = wx.Button(self.panel, label="Modify")
        self.btnModifyItem.Bind(wx.EVT_BUTTON, self.onBtnModifyItem)

        self.btnSettings = wx.Button(self.panel, label="Settings")
        self.btnSettings.Bind(wx.EVT_BUTTON, self.onBtnSettings)

        self.sizerModify.Add(self.btnAddItem, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.sizerModify.Add(self.btnRemoveItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))
        self.sizerModify.Add(self.btnModifyItem, wx.SizerFlags().Proportion(1).Border(wx.LEFT, 2))

        self.sizerMain.Add(self.title, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.dataView, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.sizerMain.Add(self.sizerModify, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.sizerMain.Add(self.btnSettings, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.Center()

    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.SetMinSize((200, 300))

        pub.subscribe(self.listenerRemoveFolder, "removeFolderListener")
        pub.subscribe(self.listenerSetStatus, "setStatusListener")
        pub.subscribe(self.render, "reRender")

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Ready!")

        self.render()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onInterval, self.timer)
        self.timer.Start(self.config.interval)

        self.Show(True)


def renderGui():
    app = wx.App()
    mainWindow = MainWindow()
    app.MainLoop()


if __name__ == "__main__":

    renderGui()