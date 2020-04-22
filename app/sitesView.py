from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView

class PickSite(commonView.CommonView):
    """docstring for PickMailbox"""
    def __init__(self, siteList):
        super(PickSite, self).__init__()

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(siteList)
        label = commonView.PlainLabel("Select Site")
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
        label = commonView.PlainLabel("New Name")
        self.layout.addLayout(commonView.horizontalPair(label, self.newName))

        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.messages = commonView.PlainLabel(" ")
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

        dataLabel = commonView.PlainLabel("Data block")
        self.data = QtWidgets.QTextEdit()

        self.layout.addLayout(commonView.horizontalPair(dataLabel, self.data))

        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.messages = commonView.PlainLabel(" ")

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

class DisplaySite(commonView.CommonView):
    """docstring for DisplaySite"""
    def __init__(self, name, endpoint, identifier, address):
        super(DisplaySite, self).__init__()

        self.show("Name", name)
        self.show("Endpoint", endpoint)
        self.show("Identifier", identifier)
        self.show("Address", address)

        commonView.button(self.layout, "Close", self.close)

    def show(self, label, data):
        labelWidget = commonView.PlainLabel(label)
        dataWidget = commonView.PlainLabel(data)

        self.layout.addLayout(commonView.horizontalPair(labelWidget, dataWidget))

        self.layout.insertStretch(-1)



class SitesView(commonView.CommonView):
    """Buttons to select mailbox editing actions"""
    def __init__(self, controller, picker):
        super(SitesView, self).__init__()

        self.controller = controller
        self.picker = picker
        
        commonView.button(self.layout, "Add Site", self.addSite)
        commonView.button(self.layout, "Rename Site", self.renameSite)
        commonView.button(self.layout, "Delete Site", self.deleteSite)
        commonView.button(self.layout, "Display Site", self.displaySite)
        commonView.button(self.layout, "Close", self.close)

        self.messages = commonView.PlainLabel(" ")
        self.layout.addLayout(commonView.horizontal(self.messages))
        self.layout.insertStretch(-1)

    def addSite(self):
        add = AddSite(self.controller, self.picker)
        add.exec()

    def renameSite(self):
        pick = PickSite(self.controller.getSiteList())
        if pick.exec():
            if self.controller.siteExists(pick.picked):
                data = self.controller.getSite(pick.picked)
                rename = RenameSite(self.controller, self.picker, data[1])
                rename.exec()
            else:
                self.messages.setText(pick.picked + " does not exist")

    def deleteSite(self):
        pick = PickSite(self.controller.getSiteList())
        if pick.exec():
            if self.controller.siteExists(pick.picked):
                toDelete = pick.picked
                self.controller.deleteSite(toDelete)
                self.picker.deleteSite(toDelete)
            else:
                self.messages.setText(pick.picked + " does not exist")

    def displaySite(self):
        pick = PickSite(self.controller.getSiteList())
        if pick.exec():
            if self.controller.siteExists(pick.picked):
                siteId, name, endpoint, identifier, address = self.controller.getSite(pick.picked)
                display = DisplaySite(name, endpoint, identifier, address)
                display.exec()
            else:
                self.messages.setText(pick.picked + " does not exist")



def display(controller, picker):
    sites = SitesView(controller, picker)
    sites.exec()

