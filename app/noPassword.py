#
#       noPassword.py
#
#       noPassword mainline
#

import sys
import sqlite3
from PySide2 import QtWidgets

from Model import Model
from MailboxesWidget import MailboxesWidget
from ConnectWidget import ConnectWidget
from RegisterWidget import RegisterWidget
from LoginWidget import LoginWidget

def fileName():
    return "nopassword.sqlite"

class NoPasswordWidget(QtWidgets.QWidget):
    def __init__(self, model):
        super().__init__()

        self.mailboxes = MailboxesWidget(model)
        self.connect = ConnectWidget()
        self.register = RegisterWidget()
        self.login = LoginWidget()

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.mailboxes)
        self.layout.addWidget(self.connect)
        self.layout.addWidget(self.register)
        self.layout.addWidget(self.login)
        
        self.layout.insertStretch(-1)

        self.setLayout(self.layout)


if __name__ == "__main__":
    model = Model(fileName())
    app = QtWidgets.QApplication()

    widget = NoPasswordWidget(model)
    widget.resize(600, 800)
    widget.show()

    sys.exit(app.exec_())
