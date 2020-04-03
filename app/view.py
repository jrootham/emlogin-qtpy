import sys
from PySide2 import QtWidgets
import commonView
import mailboxesView
import sitesView

class NoPasswordWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()

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
        pass

    def deleteSite(self, name):
        pass

    def login(self):
        if self.pickSite.currentText() != "":
            print(self.pickSite.currentText())
        else:
            self.messages.setText("No site available")

    def exit(self):
        self.close()


def run(controller):
    app = QtWidgets.QApplication()

    widget = NoPasswordWidget(controller)
    widget.resize(200, 200)
    widget.show()

    sys.exit(app.exec_())

