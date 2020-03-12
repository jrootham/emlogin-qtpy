from PySide2 import QtCore, QtWidgets

class MailboxesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.title = QtWidgets.QLabel("Mailboxes")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.__pick__()
        self.__values__()
        self.__buttons__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.pickBox)
        self.layout.addLayout(self.outerValuesBox)
        self.layout.addLayout(self.buttonBox)

        self.setLayout(self.layout)

    def __pick__(self):

        self.pick = QtWidgets.QComboBox()
        self.load = QtWidgets.QPushButton("Load")

        self.pickBox = QtWidgets.QHBoxLayout()
        self.pickBox.addWidget(self.pick)
        self.pickBox.addWidget(self.load)
        self.pickBox.insertStretch(0)
        self.pickBox.insertStretch(-1)

    def __values__(self):
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

    def __buttons__(self):

        self.new = QtWidgets.QPushButton("New")
        self.save = QtWidgets.QPushButton("Save")

        self.buttonBox = QtWidgets.QHBoxLayout()
        self.buttonBox.addWidget(self.new)
        self.buttonBox.addWidget(self.save)
        self.buttonBox.insertStretch(0)
        self.buttonBox.insertStretch(-1)

#        self.button.clicked.connect(self.magic)
