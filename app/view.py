import sys
from PySide2 import QtWidgets
import commonView
import mailboxesView
import sitesView

class Password(QtWidgets.QDialog):
    """docstring for Password"""
    def __init__(self):
        super(Password, self).__init__()

        self.password = ""

        layout = QtWidgets.QVBoxLayout()
        layout.insertStretch(0)

        passwordLabel = QtWidgets.QLabel("Password")
        self.passwordEdit = QtWidgets.QLineEdit()
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        layout.addLayout(commonView.horizontalPair(passwordLabel, self.passwordEdit))
        layout.insertStretch(-1)

        commonView.buttons(self, layout, self.save)

        self.setLayout(layout)

    def save(self):
        self.password = self.passwordEdit.text()
        self.accept()

def getPassword():
    widget = Password()
    widget.passwordEdit.setFocus()
    if widget.exec():
        return widget.password
    else:
        return ""


        
class NoPasswordWidget(QtWidgets.QWidget):
    def __init__(self, app, controller):
        super().__init__()

        self.app = app
        self.controller = controller

        layout = QtWidgets.QVBoxLayout()
        layout.insertStretch(0)

        title = QtWidgets.QLabel("No Password")
        
        layout.addLayout(commonView.horizontal(title))
        layout.insertStretch(-1)

        commonView.button(layout, "Edit Mailboxes", self.editMailboxes)
        commonView.button(layout, "Edit Sites", self.editSites)
        
        self.pickSite = QtWidgets.QComboBox()
        layout.addLayout(commonView.horizontal(self.pickSite))
        self.pickSite.addItems(self.controller.getSiteList())
        layout.insertStretch(-1)

        commonView.button(layout, "Login", self.login)
        commonView.button(layout, "Exit", self.exit)

        self.messages = QtWidgets.QLabel()
        layout.addLayout(commonView.horizontal(self.messages))
        self.messages.setText(" ")
        layout.insertStretch(-1)

        self.setLayout(layout)


    def editMailboxes(self):
        mailboxesView.display(self.controller)

    def editSites(self):
        sitesView.display(self.controller, self)

    def addSite(self, name):
        self.pickSite.addItem(name)
        self.pickSite.model().sort(0)

    def deleteSite(self, name):
        self.pickSite.removeItem(self.pickSite.findText(name))

    def login(self):
        if self.pickSite.currentText() != "":
            errors = self.controller.login(self.app, self, self.pickSite.currentText())
            self.messages.setText(errors)
        else:
            self.messages.setText("No site available")

    def display(self, message):
        self.messages.setText(message)
        self.app.processEvents()

    def exit(self):
        self.close()


def run(controller):
    app = QtWidgets.QApplication()

    widget = NoPasswordWidget(app, controller)
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec_())

