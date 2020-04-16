from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView

class EditMailbox(commonView.CommonView):
    """UI for adding mailboxes"""
    def __init__(self, title, action, address, host, userName):
        super(EditMailbox, self).__init__()
        self.action = action

        self.layout.addLayout(commonView.horizontal(QtWidgets.QLabel(title)))
        self.layout.insertStretch(-1)

        self.addressEdit = QtWidgets.QLineEdit(address)
        self.hostEdit = QtWidgets.QLineEdit(host)
        self.userNameEdit = QtWidgets.QLineEdit(userName)

        valuesBox = QtWidgets.QGridLayout()
        valuesBox.addWidget(QtWidgets.QLabel("Email Address"), 0, 0)
        valuesBox.addWidget(self.addressEdit, 0, 1)
        valuesBox.addWidget(QtWidgets.QLabel("Host"), 1, 0)
        valuesBox.addWidget(self.hostEdit, 1, 1)
        valuesBox.addWidget(QtWidgets.QLabel("User Name"), 2, 0)
        valuesBox.addWidget(self.userNameEdit, 2, 1)

        self.layout.addLayout(valuesBox)
        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.messages = QtWidgets.QLabel(" ")
        self.layout.addWidget(self.messages)
        self.layout.insertStretch(-1)


    def save(self):
        address = self.addressEdit.text()
        host = self.hostEdit.text()
        userName = self.userNameEdit.text()

        messages = self.action.save(address, host, userName)

        if 0 == len(messages):
            self.close()
        else:
            self.messages.setText(messages)
