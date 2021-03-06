from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView
from EditMailbox import EditMailbox

class PickMailbox(commonView.CommonView):
    """docstring for PickMailbox"""
    def __init__(self, addressList):
        super(PickMailbox, self).__init__()

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(addressList)
        label = commonView.PlainLabel("Select Mailbox")
        self.layout.addLayout(commonView.horizontalPair(label, self.pick))
        self.layout.insertStretch(-1)

        commonView.buttons(self, self.layout, self.save)

        self.setLayout(self.layout)

    def save(self):
        self.picked = self.pick.currentText()
        self.accept()

class ActionBase(object):
    """docstring for ActionBase"""
    def __init__(self, controller):
        super(ActionBase, self).__init__()
        self.controller = controller

    def save(self, address, host, userName):
        return ""

class AddAction(ActionBase):
    """docstring for ClassName"""
    def __init__(self, controller):
        super(AddAction, self).__init__(controller)
                        
    def save(self, address, host, userName):
        return self.controller.addMailbox(address, host, userName)

class EditAction(ActionBase):
    """docstring for ClassName"""
    def __init__(self, controller, mailboxId):
        super(EditAction, self).__init__(controller)
        self.mailboxId = mailboxId
        
    def save(self, address, host, userName):
        return self.controller.updateMailbox(self.mailboxId, address, host, userName)


class MailboxesView(commonView.CommonView):
    """Buttons to select mailbox editing actions"""
    def __init__(self, controller):
        super(MailboxesView, self).__init__()

        self.controller = controller
        
        commonView.button(self.layout, "Add Mailbox", self.addMailbox)
        commonView.button(self.layout, "Edit Mailbox", self.editMailbox)
        commonView.button(self.layout, "Delete Mailbox", self.deleteMailbox)
        commonView.button(self.layout, "Close", self.exit)

        self.messages = commonView.PlainLabel(" ")
        self.layout.addLayout(commonView.horizontal(self.messages))
        self.layout.insertStretch(-1)

    def addMailbox(self):
        add = EditMailbox("Add Mailbox", AddAction(self.controller), "", "", "")
        add.exec()

    def editMailbox(self):
        pick = PickMailbox(self.controller.getMailboxList())
        if pick.exec():
            if self.controller.mailboxExists(pick.picked):
                mailboxId, address, host, userName = self.controller.getMailbox(pick.picked)
                action = EditAction(self.controller, mailboxId)
                edit = EditMailbox("Edit Mailbox", action, address, host, userName)
                edit.exec()
            else:
                self.messages.setText(pick.picked + " does not exist")

    # def editMailbox(self):
    #     pass

    def deleteMailbox(self):
        pick = PickMailbox(self.controller.getMailboxList())
        if pick.exec():
            if self.controller.mailboxExists(pick.picked):
                self.controller.deleteMailbox(pick.picked)
            else:
                self.messages.setText(pick.picked + " does not exist")


    def exit(self):
        self.close()

def display(controller):
    boxes = MailboxesView(controller)
    boxes.exec()

