from PySide2 import QtCore, QtWidgets

class ConnectWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.title = QtWidgets.QLabel("Connect")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.passwordLabel = QtWidgets.QLabel("Password")

        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.connectButton = QtWidgets.QPushButton("Connect")

        self.passwordBox = QtWidgets.QHBoxLayout()
        self.passwordBox.addWidget(self.passwordLabel)
        self.passwordBox.addWidget(self.password)
        self.passwordBox.addWidget(self.connectButton)

        self.passwordBox.insertStretch(0)
        self.passwordBox.insertStretch(-1)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.passwordBox)

        self.setLayout(self.layout)

