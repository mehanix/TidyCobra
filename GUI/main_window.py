import wx


def render_GUI():
    app = wx.App()
    frame = wx.Frame(None, title='Tidy Cobra',size=(500,500))
    frame.Center()
    frame.Show()
    app.MainLoop()

render_GUI()