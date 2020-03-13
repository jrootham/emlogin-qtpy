from PySide2 import QtCore, QtWidgets

class MailboxesWidget(QtWidgets.QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model

        self.title = QtWidgets.QLabel("Mailboxes")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.errors = QtWidgets.QLabel("")
        self.errors.setAlignment(QtCore.Qt.AlignCenter)

        self.pick()
        self.values()
        self.buttons()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.pickBox)
        self.layout.addLayout(self.outerValuesBox)
        self.layout.addLayout(self.buttonBox)
        self.layout.addWidget(self.errors)

        self.setLayout(self.layout)
        
        return

    def pick(self):

        self.pick = QtWidgets.QComboBox()
        self.load = QtWidgets.QPushButton("Load")

        self.pickBox = QtWidgets.QHBoxLayout()
        self.pickBox.addWidget(self.pick)
        self.pickBox.addWidget(self.load)
        self.pickBox.insertStretch(0)
        self.pickBox.insertStretch(-1)
        
        return

    def values(self):
        self.nameLabel = QtWidgets.QLabel("Mailbox name")
        self.name = QtWidgets.QLineEdit()

        self.hostLabel = QtWidgets.QLabel("Host")
        self.host = QtWidgets.QLineEdit()

        self.userNameLabel = QtWidgets.QLabel("User name")
        self.userName = QtWidgets.QLineEdit()

        self.valuesBox = QtWidgets.QGridLayout()
        self.valuesBox.addWidget(self.nameLabel, 0, 0)
        self.valuesBox.addWidget(self.name, 0, 1)
        self.valuesBox.addWidget(self.hostLabel, 1, 0)
        self.valuesBox.addWidget(self.host, 1, 1)
        self.valuesBox.addWidget(self.userNameLabel, 2, 0)
        self.valuesBox.addWidget(self.userName, 2, 1)

        self.outerValuesBox = QtWidgets.QHBoxLayout()
        self.outerValuesBox.addLayout(self.valuesBox)
        self.outerValuesBox.insertStretch(0)
        self.outerValuesBox.insertStretch(-1)

        return

    def buttons(self):

        self.clear = QtWidgets.QPushButton("Clear")
        self.new = QtWidgets.QPushButton("New")
        self.update = QtWidgets.QPushButton("Update")
        self.delete = QtWidgets.QPushButton("Delete")

        self.buttonBox = QtWidgets.QHBoxLayout()
        self.buttonBox.addWidget(self.clear)
        self.buttonBox.addWidget(self.new)
        self.buttonBox.addWidget(self.update)
        self.buttonBox.addWidget(self.delete)
        self.buttonBox.insertStretch(0)
        self.buttonBox.insertStretch(-1)

        self.clear.clicked.connect(lambda:self.clearData())
        self.new.clicked.connect(lambda:self.newBox())

        return

    def clearData(self):
        self.errors.setText("")

        self.name.setText("")
        self.host.setText("")
        self.userName.setText("")

        return

    def newBox(self):
        self.errors.setText("")
        errors = self.model.addMailbox(self.name.text(), self.host.text(), self.userName.text())
        self.errors.setText(errors)

        return