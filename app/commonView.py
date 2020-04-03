from PySide2 import QtWidgets

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

