from PySide2 import QtCore, QtWidgets

class ConnectWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        title = QtWidgets.QLabel("Connect")
        title.setAlignment(QtCore.Qt.AlignCenter)

        passwordLabel = QtWidgets.QLabel("Password")

        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        connectButton = QtWidgets.QPushButton("Connect")
        connectButton.clicked.connect(self.doConnect)

        passwordBox = QtWidgets.QHBoxLayout()
        passwordBox.addWidget(passwordLabel)
        passwordBox.addWidget(self.password)
        passwordBox.addWidget(connectButton)

        passwordBox.insertStretch(0)
        passwordBox.insertStretch(-1)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(passwordBox)

        self.setLayout(layout)

    def doConnect(self):
        self.controller.doConnect()
