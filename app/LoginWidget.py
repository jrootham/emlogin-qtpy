from PySide2 import QtCore, QtWidgets
import secrets
import requests

class LoginWidget(QtWidgets.QWidget):
    def __init__(self, mailboxes, sites):
        super().__init__()

        self.mailboxes = mailboxes
        self.sites = sites

        self.token = ""

        title = QtWidgets.QLabel("Login")
        title.setAlignment(QtCore.Qt.AlignCenter)

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(self.sites.getNames())

        login = QtWidgets.QPushButton("Login")
        login.clicked.connect(self.requestLogin)

        loginBox = QtWidgets.QHBoxLayout()
        loginBox.addWidget(self.pick)
        loginBox.addWidget(login)
        loginBox.insertStretch(0)
        loginBox.insertStretch(-1)

        self.messages = QtWidgets.QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(loginBox)
        layout.addWidget(self.messages)

        self.setLayout(layout)

    def requestLogin(self):
        self.token = secrets.token_hex(16)
        siteName = self.pick.currentText()
        if self.sites.exists(siteName):
            name, endpoint, identifier = self.sites.getSite(siteName)
            payload = {"identifier": identifier, "token": self.token}
            response = requests.get(endpoint, payload)
            if response.status_code == requests.codes.ok:
                self.readEmail()
            else:
                self.messages.setText(response.text)
                # Errors
        else:
            self.messages.setText(siteName + " does not exist")

    def readEmail(self):
        pass