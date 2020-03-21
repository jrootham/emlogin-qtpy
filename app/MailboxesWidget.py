from PySide2 import QtCore, QtWidgets

class MailboxesWidget(QtWidgets.QWidget):
    """Container for mailbox UI """

    def __init__(self, mailboxes):
        super().__init__()

        self.mailboxes = mailboxes

        self.title = QtWidgets.QLabel("Mailboxes")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.messages = QtWidgets.QLabel("")
        self.messages.setAlignment(QtCore.Qt.AlignCenter)

        self.pick(self.mailboxes.getNames())
        self.values()
        self.buttons()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.pickBox)
        self.layout.addLayout(self.outerValuesBox)
        self.layout.addLayout(self.buttonBox)
        self.layout.addWidget(self.messages)

        self.setLayout(self.layout)
        

    def pick(self, nameList):

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(nameList)

        self.load = QtWidgets.QPushButton("Load")
        self.load.clicked.connect(lambda:self.loadData())

        self.pickBox = QtWidgets.QHBoxLayout()
        self.pickBox.addWidget(self.pick)
        self.pickBox.addWidget(self.load)
        self.pickBox.insertStretch(0)
        self.pickBox.insertStretch(-1)
        
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
        self.update.clicked.connect(lambda:self.updateBox())
        self.delete.clicked.connect(lambda:self.deleteBox())

#
#   functions connected to buttons to do things
#

    def loadData(self):
        self.messages.setText("")
        
        name, host, userName = self.mailboxes.getMailbox(self.pick.currentText())

        self.name.setText(name)
        self.host.setText(host)
        self.userName.setText(userName)

    def clearData(self):
        self.messages.setText("")

        self.name.setText("")
        self.host.setText("")
        self.userName.setText("")

    def newBox(self):
        self.messages.setText("")
        
        name = self.name.text()
        host = self.host.text()
        userName = self.userName.text()

        messages = self.mailboxes.addMailbox(name, host, userName)

        if 0 == len(messages):
            self.pick.addItem(self.name.text())
            self.pick.model().sort(0)
            self.messages.setText("Add successful")

        else:
            self.messages.setText(messages)

    def updateBox(self):
        self.messages.setText("")
        
        name = self.name.text()
        host = self.host.text()
        userName = self.userName.text()

        messages = self.mailboxes.updateMailbox(name, host, userName)

        if 0 == len(messages):
            self.messages.setText("Update successful")

        else:
            self.messages.setText(messages)

    def deleteBox(self):
        self.messages.setText("")
        
        name = self.name.text()

        messages = self.mailboxes.deleteMailbox(name)

        if 0 == len(messages):
            self.clearData()
            self.pick.removeItem(self.pick.currentIndex())

            self.messages.setText("Delete successful")

        else:
            self.messages.setText(messages)
