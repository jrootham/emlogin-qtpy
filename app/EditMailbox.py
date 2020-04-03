from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView

class EditMailbox(QtWidgets.QDialog):
    """UI for adding mailboxes"""
    def __init__(self, title, action, address, host, userName):
        super(EditMailbox, self).__init__()
        self.action = action

        layout = QtWidgets.QVBoxLayout(self)
        
        layout.insertStretch(0)

        layout.addLayout(commonView.horizontal(QtWidgets.QLabel(title)))
        layout.insertStretch(-1)

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

        layout.addLayout(valuesBox)
        layout.insertStretch(-1)


        buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
        QtCore.Qt.Horizontal, self)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout.insertStretch(-1)

        self.messages = QtWidgets.QLabel(" ")
        layout.addWidget(self.messages)
        layout.insertStretch(-1)

        self.setLayout(layout)


    def save(self):
        address = self.addressEdit.text()
        host = self.hostEdit.text()
        userName = self.userNameEdit.text()

        messages = self.action.save(address, host, userName)

        if 0 == len(messages):
            self.close()
        else:
            self.messages.setText(messages)
