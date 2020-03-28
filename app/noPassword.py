import sys
import sqlite3
from PySide2 import QtWidgets

from Controller import Controller
from Mailboxes import Mailboxes
from MailboxesWidget import MailboxesWidget
from ConnectWidget import ConnectWidget
from RegisterWidget import RegisterWidget
from LoginWidget import LoginWidget

"""
noPassword is an applicatioin designed to make it easier to login to sites that support the noPassword 
protocal.


"""
def fileName():
    """File name constant"""
    return "nopassword.sqlite"

class NoPasswordWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()

        self.mailboxes = MailboxesWidget(controller.getMailboxes())
        self.connect = ConnectWidget(controller.getMailboxes())
        self.register = RegisterWidget(controller.getSites())
        self.login = LoginWidget(controller.getMailboxes(), controller.getSites())

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.mailboxes)
        self.layout.addWidget(self.register)
        self.layout.addWidget(self.connect)
        self.layout.addWidget(self.login)
        
        self.layout.insertStretch(-1)

        self.setLayout(self.layout)

        return
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()

    widget = NoPasswordWidget(Controller(fileName()))
    widget.resize(600, 800)
    widget.show()

    sys.exit(app.exec_())
