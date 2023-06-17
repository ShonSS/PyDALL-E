from PyQt6.QtGui import QPalette, QColor, QGuiApplication


def set_dark_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)


def set_light_mode(window):
    # Reset to the default palette for light mode
    window.setPalette(QGuiApplication.palette())

def set_solarized_dark_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(0, 43, 54))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(7, 54, 66))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0, 43, 54))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(0, 43, 54))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(38, 139, 210))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(38, 139, 210))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)


def set_gruvbox_dark_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 34))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 34))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(40, 40, 34))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(181, 137, 0))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(181, 137, 0))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)


def set_nord_dark_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(46, 52, 64))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(46, 52, 64))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(59, 66, 82))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(46, 52, 64))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(124, 179, 225))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(124, 179, 225))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)

def set_abyss_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 38))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(18, 18, 24))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 38))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(30, 30, 38))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)


def set_monokai_mode(window):
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(39, 40, 34))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Base, QColor(39, 40, 34))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 45, 37))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Text, QColor("white"))
    palette.setColor(QPalette.ColorRole.Button, QColor(39, 40, 34))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
    palette.setColor(QPalette.ColorRole.Link, QColor(166, 122, 63))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(166, 122, 63))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))
    window.setPalette(palette)
