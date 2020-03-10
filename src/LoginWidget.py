from PySide2 import QtCore, QtWidgets

class LoginWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.title = QtWidgets.QLabel("Login")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.pick = QtWidgets.QComboBox()
        self.login = QtWidgets.QPushButton("Login")

        self.loginBox = QtWidgets.QHBoxLayout()
        self.loginBox.addWidget(self.pick)
        self.loginBox.addWidget(self.login)
        self.loginBox.insertStretch(0)
        self.loginBox.insertStretch(-1)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.loginBox)

        self.setLayout(self.layout)

