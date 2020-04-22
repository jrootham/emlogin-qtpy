import sys
from PySide2 import QtWidgets
import commonView
import mailboxesView
import sitesView

class Password(commonView.CommonView):
    """docstring for Password"""
    def __init__(self, address):
        super(Password, self).__init__()

        self.password = ""

        self.layout.addLayout(commonView.horizontal(commonView.PlainLabel(address)))

        passwordLabel = commonView.PlainLabel("Password")
        self.passwordEdit = QtWidgets.QLineEdit()
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.layout.addLayout(commonView.horizontalPair(passwordLabel, self.passwordEdit))
        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

    def save(self):
        self.password = self.passwordEdit.text()
        self.accept()

def getPassword(address):
    widget = Password(address)
    widget.passwordEdit.setFocus()
    if widget.exec():
        return widget.password
    else:
        return ""


        
class EMLoginWidget(commonView.CommonView):
    def __init__(self, app, controller):
        super().__init__()

        self.app = app
        self.controller = controller

        commonView.button(self.layout, "Edit Mailboxes", self.editMailboxes)
        commonView.button(self.layout, "Edit Sites", self.editSites)
        
        self.pickSite = QtWidgets.QComboBox()
        self.layout.addLayout(commonView.horizontal(self.pickSite))
        self.pickSite.addItems(self.controller.getSiteList())
        self.layout.insertStretch(-1)

        commonView.button(self.layout, "Login", self.login)
        commonView.button(self.layout, "Exit", self.exit)

        self.messages = commonView.PlainLabel()
        self.layout.addLayout(commonView.horizontal(self.messages))
        self.messages.setText(" ")
        self.layout.insertStretch(-1)

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

    widget = EMLoginWidget(app, controller)
    widget.resize(250, 200)
    widget.show()

    sys.exit(app.exec_())

