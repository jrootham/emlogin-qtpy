import sys
from PySide2 import QtWidgets

from MailboxesWidget import MailboxesWidget
# import connectWidget as connect
# import registerWidget as register
# import loginWidget as login

class NoPasswordWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.mailboxes = MailboxesWidget()
        # self.connect = connect.Connect()
        # self.register = register.Register()
        # self.login = login.Login()

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.mailboxes)
        # self.layout.addWidget(self.connect)
        # self.layout.addWidget(self.register)
        # self.layout.addWidget(self.login)
        
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = NoPasswordWidget()
    widget.resize(600, 800)
    widget.show()

    sys.exit(app.exec_())
