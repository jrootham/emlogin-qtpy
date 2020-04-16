from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView

class PickSite(commonView.CommonView):
    """docstring for PickMailbox"""
    def __init__(self, siteList):
        super(PickSite, self).__init__()

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(siteList)
        label = QtWidgets.QLabel("Select Site")
        self.layout.addLayout(commonView.horizontalPair(label, self.pick))
        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

    def save(self):
        self.picked = self.pick.currentText()
        self.accept()

class RenameSiteBase(commonView.CommonView):
    """Rename a site"""
    def __init__(self):
        super(RenameSiteBase, self).__init__()

        self.newName = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel("New Name")
        self.layout.addLayout(commonView.horizontalPair(label, self.newName))

        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.messages = QtWidgets.QLabel(" ")
        self.layout.addLayout(commonView.horizontal(self.messages))
        self.layout.insertStretch(-1)

class NewSiteName(RenameSiteBase):
    """docstring for RenameSite"""
    def __init__(self, controller, oldName):
        super(NewSiteName, self ).__init__()
        self.controller = controller
        self.oldName = oldName
        self.name = ""

        self.messages.setText(oldName + " already exists")
        
    def save(self):
        self.name = self.newName.text()

        if not self.controller.siteExists(self.name):
            self.accept()

        else:
            self.messages.setText(self.name + " already exists")


class RenameSite(RenameSiteBase):
    """docstring for RenameSite"""
    def __init__(self, controller, picker, oldName):
        super(RenameSite, self).__init__()
        self.controller = controller
        self.picker = picker
        self.oldName = oldName
        
    def save(self):
        newName = self.newName.text()
        messages = self.controller.renameSite(self.oldName, newName)

        if len(messages) == 0:
            self.picker.deleteSite(self.oldName)
            self.picker.addSite(newName)
            self.accept()
        else:
            self.messages.setText(messages)        

class AddSite(commonView.CommonView):
    """docstring for AddSite"""
    def __init__(self, controller, picker):
        super(AddSite, self).__init__()
        self.controller = controller
        self.picker = picker

        dataLabel = QtWidgets.QLabel("Data block")
        self.data = QtWidgets.QTextEdit()

        self.layout.addLayout(commonView.horizontalPair(dataLabel, self.data))

        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.messages = QtWidgets.QLabel(" ")

        self.layout.addLayout(commonView.horizontal(self.messages))
        self.layout.insertStretch(-1)

    def save(self):
        text = self.data.toPlainText()
        name, endpoint, identifier, address = text.split("\n")
        
        if not self.controller.siteExists(name):
            messages = self.controller.addSite(name, endpoint, identifier, address)
            if len(messages) == 0:
                self.picker.addSite(name)
                self.accept()
            else:
                self.messages.setText(messages)
        else:
            newName = NewSiteName(self.controller, name)
            if newName.exec():
                messages = self.controller.addSite(newName.name, endpoint, identifier, address)
                if len(messages) == 0:
                    self.picker.addSite(newName.name)
                    self.accept()
                else:
                    self.messages.setText(messages)
            else:
                self.reject()


class SitesView(commonView.CommonView):
    """Buttons to select mailbox editing actions"""
    def __init__(self, controller, picker):
        super(SitesView, self).__init__()

        self.controller = controller
        self.picker = picker
        
        commonView.button(self.layout, "Add Site", self.addSite)
        commonView.button(self.layout, "Rename Site", self.renameSite)
        commonView.button(self.layout, "Delete Site", self.deleteSite)
        commonView.button(self.layout, "Close", self.exit)


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
            toDelete = pick.picked
            self.controller.deleteSite(toDelete)
            self.picker.deleteSite(toDelete)

    def exit(self):
        self.close()

def display(controller, picker):
    sites = SitesView(controller, picker)
    sites.exec()

