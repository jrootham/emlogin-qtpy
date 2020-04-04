from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView

class PickSite(QtWidgets.QDialog):
    """docstring for PickMailbox"""
    def __init__(self, siteList):
        super(PickSite, self).__init__()

        layout = QtWidgets.QVBoxLayout()

        layout.insertStretch(0)

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(siteList)
        label = QtWidgets.QLabel("Select Site")
        layout.addLayout(commonView.horizontalPair(label, self.pick))
        layout.insertStretch(-1)

        buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
        QtCore.Qt.Horizontal, self)
        layout.addWidget(buttons)
        layout.insertStretch(-1)

        self.setLayout(layout)

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

    def save(self):
        self.picked = self.pick.currentText()
        self.accept()

class AddSite(QtWidgets.QDialog):
    """docstring for AddSite"""
    def __init__(self, controller, picker):
        super(AddSite, self).__init__()
        self.controller = controller
        self.picker = picker

        layout = QtWidgets.QVBoxLayout()

        layout.insertStretch(0)

        dataLabel = QtWidgets.QLabel("Data block")
        self.data = QtWidgets.QTextEdit()

        layout.addLayout(commonView.horizontalPair(dataLabel, self.data))

        layout.insertStretch(-1)

        buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
        QtCore.Qt.Horizontal, self)
        layout.addWidget(buttons)
        layout.insertStretch(-1)

        self.setLayout(layout)

        self.messages = QtWidgets.QLabel(" ")
        layout.addLayout(commonView.horizontal(self.messages))
        layout.insertStretch(-1)

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

    def save(self):
        text = self.data.toPlainText()
        name, endpoint, identifier = text.split("\n")
        
        messages = self.controller.addSite(name, endpoint, identifier)
        if len(messages) == 0:
            self.picker.addSite(name)
            self.accept()
        else:
            self.messages.setText(messages)
        
class RenameSite(QtWidgets.QDialog):
    """docstring for AddSite"""
    def __init__(self, controller, picker, oldName):
        super(RenameSite, self).__init__()
        self.controller = controller
        self.picker = picker
        self.oldName = oldName

        layout = QtWidgets.QVBoxLayout()

        layout.insertStretch(0)

        self.newName = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel("New Name")
        layout.addLayout(commonView.horizontalPair(label, self.newName))

        layout.insertStretch(-1)

        buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
        QtCore.Qt.Horizontal, self)
        layout.addWidget(buttons)
        layout.insertStretch(-1)

        self.messages = QtWidgets.QLabel(" ")
        layout.addLayout(commonView.horizontal(self.messages))
        layout.insertStretch(-1)

        self.setLayout(layout)

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

    def save(self):
        newName = self.newName.text()
        messages = self.controller.renameSite(self.oldName, newName)

        if len(messages) == 0:
            self.picker.deleteSite(self.oldName)
            self.picker.addSite(newName)
            self.accept()
        else:
            self.messages.setText(messages)        

class SitesView(QtWidgets.QDialog):
    """Buttons to select mailbox editing actions"""
    def __init__(self, controller, picker):
        super(SitesView, self).__init__()

        self.controller = controller
        self.picker = picker
        
        layout = QtWidgets.QVBoxLayout()
        layout.insertStretch(0)

        commonView.button(layout, "Add Site", self.addSite)
        commonView.button(layout, "Rename Site", self.renameSite)
        commonView.button(layout, "Delete Site", self.deleteSite)
        commonView.button(layout, "Close", self.exit)

        self.setLayout(layout)


    def addSite(self):
        add = AddSite(self.controller, self.picker)
        add.exec()

    def renameSite(self):
        pick = PickSite(self.controller.getSiteList())
        if pick.exec():
            data = self.controller.getSite(pick.picked)
            rename = RenameSite(self.controller, self.picker, data[1])
            rename.exec()

    def deleteSite(self):
        pick = PickSite(self.controller.getSiteList())
        if pick.exec():
            self.controller.deleteSite(pick.picked)

    def exit(self):
        self.close()

def display(controller, picker):
    sites = SitesView(controller, picker)
    sites.exec()

