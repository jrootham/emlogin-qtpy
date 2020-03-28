from PySide2 import QtCore, QtWidgets

class MailboxesWidget(QtWidgets.QWidget):
    """Container for mailbox UI """

    def __init__(self, mailboxes):
        super().__init__()

        self.mailboxes = mailboxes

        title = QtWidgets.QLabel("Mailboxes")
        title.setAlignment(QtCore.Qt.AlignCenter)

        self.messages = QtWidgets.QLabel("")
        self.messages.setAlignment(QtCore.Qt.AlignCenter)

        pickBox = self.pick(self.mailboxes.getNames())
        valuesBox = self.values()
        buttonBox = self.buttons()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(pickBox)
        layout.addLayout(valuesBox)
        layout.addLayout(buttonBox)
        layout.addWidget(self.messages)

        self.setLayout(layout)
        

    def pick(self, nameList):

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(nameList)

        load = QtWidgets.QPushButton("Load")
        load.clicked.connect(lambda:self.loadData())

        pickBox = QtWidgets.QHBoxLayout()
        pickBox.addWidget(self.pick)
        pickBox.addWidget(load)
        pickBox.insertStretch(0)
        pickBox.insertStretch(-1)

        return pickBox
        
    def values(self):
        nameLabel = QtWidgets.QLabel("Mailbox name")
        self.name = QtWidgets.QLineEdit()

        hostLabel = QtWidgets.QLabel("Host")
        self.host = QtWidgets.QLineEdit()

        userNameLabel = QtWidgets.QLabel("User name")
        self.userName = QtWidgets.QLineEdit()

        valuesBox = QtWidgets.QGridLayout()
        valuesBox.addWidget(nameLabel, 0, 0)
        valuesBox.addWidget(self.name, 0, 1)
        valuesBox.addWidget(hostLabel, 1, 0)
        valuesBox.addWidget(self.host, 1, 1)
        valuesBox.addWidget(userNameLabel, 2, 0)
        valuesBox.addWidget(self.userName, 2, 1)

        outerValuesBox = QtWidgets.QHBoxLayout()
        outerValuesBox.addLayout(valuesBox)
        outerValuesBox.insertStretch(0)
        outerValuesBox.insertStretch(-1)

        return outerValuesBox

    def buttons(self):

        clear = QtWidgets.QPushButton("Clear")
        new = QtWidgets.QPushButton("New")
        update = QtWidgets.QPushButton("Update")
        delete = QtWidgets.QPushButton("Delete")

        buttonBox = QtWidgets.QHBoxLayout()
        buttonBox.addWidget(clear)
        buttonBox.addWidget(new)
        buttonBox.addWidget(update)
        buttonBox.addWidget(delete)
        buttonBox.insertStretch(0)
        buttonBox.insertStretch(-1)

        clear.clicked.connect(self.clearData)
        new.clicked.connect(self.newBox)
        update.clicked.connect(self.updateBox)
        delete.clicked.connect(self.deleteBox)

        return buttonBox
#
#   functions connected to buttons to do things
#

    def loadData(self):
        self.messages.setText("")
        
        name = self.pick.currentText()

        if self.mailboxes.exists(name):
            name, host, userName = self.mailboxes.getMailbox(name)

            self.name.setText(name)
            self.host.setText(host)
            self.userName.setText(userName)
        else:
            self.messages.setText(name + " does not exist")

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

        if self.mailboxes.exists(name):
            messages = self.mailboxes.updateMailbox(name, host, userName)

            if 0 == len(messages):
                self.messages.setText("Update successful")

            else:
                self.messages.setText(messages)
        else:
            self.messages.setText(name + " does not exist")


    def deleteBox(self):
        self.messages.setText("")
        
        name = self.name.text()

        if self.mailboxes.exists(name):
            messages = self.mailboxes.deleteMailbox(name)

            if 0 == len(messages):
                self.clearData()
                self.pick.removeItem(self.pick.currentIndex())

                self.messages.setText("Delete successful")

            else:
                self.messages.setText(messages)
        else:
            self.messages.setText(name + " does not exist")
