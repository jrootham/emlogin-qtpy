from PySide2 import QtCore, QtWidgets

class AddRegisterDialogue(QtWidgets.QDialog):
    """AddRegisterDialog is the add registration popup"""
    def __init__(self, parent, sites):
        super(AddRegisterDialogue, self).__init__(parent)
        self.sites = sites
        self.name = ""
        self.endpoint = ""
        self.identifier = ""

        layout = QtWidgets.QVBoxLayout(self)

        dataLabel = QtWidgets.QLabel("Data block")
        self.data = QtWidgets.QTextEdit()
        parseButton = QtWidgets.QPushButton("Parse block")
        parseButton.clicked.connect(self.parse)

        parseBox = QtWidgets.QHBoxLayout()
        parseBox.addWidget(dataLabel)
        parseBox.addWidget(self.data)
        parseBox.addWidget(parseButton)
        parseBox.insertStretch(0)
        parseBox.insertStretch(-1)

        layout.addLayout(parseBox)

        nameLabel = QtWidgets.QLabel("Site name")
        self.nameEdit = QtWidgets.QLineEdit()

        endpointLabel = QtWidgets.QLabel("Endpoint")
        self.endpointValue = QtWidgets.QLabel("")

        identifierLabel = QtWidgets.QLabel("identifier")
        self.identifierValue = QtWidgets.QLabel("")

        valuesBox = QtWidgets.QGridLayout()
        valuesBox.addWidget(nameLabel, 0, 0)
        valuesBox.addWidget(self.nameEdit, 0, 1)
        valuesBox.addWidget(endpointLabel, 1, 0)
        valuesBox.addWidget(self.endpointValue, 1, 1)
        valuesBox.addWidget(identifierLabel, 2, 0)
        valuesBox.addWidget(self.identifierValue, 2, 1)

        outerValuesBox = QtWidgets.QHBoxLayout()
        outerValuesBox.addLayout(valuesBox)
        outerValuesBox.insertStretch(0)
        outerValuesBox.insertStretch(-1)

        layout.addLayout(outerValuesBox)

        self.messages = QtWidgets.QLabel("")
        layout.addWidget(self.messages)

        # OK and Cancel buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def parse(self):
        text = self.data.toPlainText()
        self.name, self.endpoint, self.identifier = text.split("\n")
        self.nameEdit.setText(self.name)
        self.endpointValue.setText(self.endpoint)
        self.identifierValue.setText(self.identifier)


    def save(self):
        if not self.sites.exists(self.name):
            self.sites.addSite(self.name, self.endpoint, self.identifier)
            self.accept()
        else:
            self.messages.setText(self.name + " already exists")
        
