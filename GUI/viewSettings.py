import wx
from pubsub import pub
from Utils.config import Config

digitCharacters = "0123456789"


def removeNonDigits(text: str) -> str:
    return "".join(character for character in text if character in digitCharacters)


class SettingsWindow(wx.Frame):

    def onBtnCancel(self, event):

        self.Destroy()

    def onBtnSave(self, event):

        intervalText = self.intervalInput.GetValue()
        if not intervalText or int(intervalText) < 1:
            self.SetStatusText("Interval must be at least 1 second.")
            return

        intervalSeconds = int(intervalText)
        self.config.interval = intervalSeconds * 1000
        self.config.saveConfig()

        pub.sendMessage("setStatusListener", message=f"Interval saved: {intervalSeconds} s. Applies after restart.")
        self.Destroy()

    def onIntervalChange(self, event):

        self.intervalInput.ChangeValue(removeNonDigits(self.intervalInput.GetValue()))
        self.intervalInput.SetInsertionPointEnd()

        event.Skip()

    def render(self) -> None:

        self.panel.DestroyChildren()

        self.config = Config()

        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerOption = wx.BoxSizer(wx.HORIZONTAL)

        self.title = wx.StaticText(self.panel, label="Settings")

        self.intervalText = wx.StaticText(self.panel, label="Interval [s]:")
        self.intervalInput = wx.TextCtrl(self.panel, value=str(self.config.interval // 1000))
        self.intervalInput.Bind(wx.EVT_TEXT, self.onIntervalChange)

        self.btnSave = wx.Button(self.panel, label="Save")
        self.btnSave.Bind(wx.EVT_BUTTON, self.onBtnSave)
        self.btnCancel = wx.Button(self.panel, label="Cancel")
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancel)

        self.sizerMain.Add(self.title, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.intervalText, wx.SizerFlags().Border(wx.TOP | wx.LEFT, 10))
        self.sizerMain.Add(self.intervalInput, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        self.sizerOption.Add(self.btnSave, wx.SizerFlags().Border(wx.RIGHT, 2).Proportion(1))
        self.sizerOption.Add(self.btnCancel, wx.SizerFlags().Proportion(1).Border(wx.LEFT | wx.RIGHT, 2))

        self.sizerMain.AddStretchSpacer()
        self.sizerMain.Add(self.sizerOption, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        self.panel.SetSizer(self.sizerMain)
        self.sizerMain.Fit(self)
        self.Center()

    def __init__(self) -> None:
        wx.Frame.__init__(self, None, title="Tidy Cobra", style=wx.DEFAULT_FRAME_STYLE)

        self.SetMinSize((200, 300))

        self.panel = wx.Panel(self)
        self.CreateStatusBar()
        self.SetStatusText("Set the background run interval in seconds.")

        self.render()

        self.Show(True)


def renderGui():
    app = wx.App()
    settingsWindow = SettingsWindow()
    app.MainLoop()


if __name__ == "__main__":

    renderGui()