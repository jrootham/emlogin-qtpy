from PySide2 import QtWidgets
from PySide2 import QtCore

def horizontal(widget):
    layout = QtWidgets.QHBoxLayout()
    layout.insertStretch(0)
    layout.addWidget(widget)
    layout.insertStretch(-1)
    return layout

def horizontalPair(widget1, widget2):
    layout = QtWidgets.QHBoxLayout()
    layout.insertStretch(0)
    layout.addWidget(widget1)
    layout.addWidget(widget2)
    layout.insertStretch(-1)
    return layout

def button(layout, text, action):
    button = QtWidgets.QPushButton(text)
    button.clicked.connect(action)
    layout.addLayout(horizontal(button))
    layout.insertStretch(-1)

def buttons(widget, layout, save):
    buttons = QtWidgets.QDialogButtonBox(
    QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, widget)
    layout.addWidget(buttons)
    layout.insertStretch(-1)

    buttons.accepted.connect(save)
    buttons.rejected.connect(widget.reject)

class PlainLabel(QtWidgets.QLabel):
    """docstring for PlainLabel"""
    def __init__(self, text = " "):
        super(PlainLabel, self).__init__(text)
        self.setTextFormat(QtCore.Qt.PlainText)
        
class CommonView(QtWidgets.QDialog):
    """Base class for dialogues """
    def __init__(self):
        super(CommonView, self).__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.insertStretch(0)

        self.setWindowTitle("EMail Login")

        self.setLayout(self.layout)
