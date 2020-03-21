from PySide2 import QtCore, QtWidgets

from AddRegisterDialogue import AddRegisterDialogue

class RegisterWidget(QtWidgets.QWidget):
    def __init__(self, sites):
        super().__init__()

        self.sites = sites
        
        title = QtWidgets.QLabel("Register")
        title.setAlignment(QtCore.Qt.AlignCenter)

        valuesBox = self.values()
        buttonBox = self.buttons()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(valuesBox)
        layout.addLayout(buttonBox)
        
        self.setLayout(layout)


    def values(self):
        nameLabel = QtWidgets.QLabel("Website name")
        name = QtWidgets.QLineEdit()

        valuesBox = QtWidgets.QGridLayout()
        valuesBox.addWidget(nameLabel, 0, 0)
        valuesBox.addWidget(name, 0, 1)

        outerValuesBox = QtWidgets.QHBoxLayout()
        outerValuesBox.addLayout(valuesBox)
        outerValuesBox.insertStretch(0)
        outerValuesBox.insertStretch(-1)

        return outerValuesBox

    def buttons(self):

        new = QtWidgets.QPushButton("New")
        rename = QtWidgets.QPushButton("Rename")
        delete = QtWidgets.QPushButton("Delete")

        buttonBox = QtWidgets.QHBoxLayout()
        buttonBox.addWidget(new)
        buttonBox.addWidget(rename)
        buttonBox.addWidget(delete)
        buttonBox.insertStretch(0)
        buttonBox.insertStretch(-1)

        new.clicked.connect(self.openNew)

        return buttonBox

    def openNew(self):
        add = AddRegisterDialogue(self, self.sites)
        add.exec()
