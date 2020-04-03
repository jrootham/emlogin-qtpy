from PySide2 import QtWidgets
from PySide2 import QtCore
import commonView
from EditMailbox import EditMailbox

class PickMailbox(QtWidgets.QDialog):
    """docstring for PickMailbox"""
    def __init__(self, addressList):
        super(PickMailbox, self).__init__()

        layout = QtWidgets.QVBoxLayout()

        layout.insertStretch(0)

        self.pick = QtWidgets.QComboBox()
        self.pick.addItems(addressList)
        label = QtWidgets.QLabel("Select Mailbox")
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


class MailboxesView(QtWidgets.QDialog):
    """Buttons to select mailbox editing actions"""
    def __init__(self, controller):
        super(MailboxesView, self).__init__()

        self.controller = controller
        
        layout = QtWidgets.QVBoxLayout()
        layout.insertStretch(0)

        commonView.button(layout, "Add Mailbox", self.addMailbox)
        commonView.button(layout, "Edit Mailbox", self.editMailbox)
        commonView.button(layout, "Delete Mailbox", self.deleteMailbox)
        commonView.button(layout, "Close", self.exit)

        self.setLayout(layout)


    def addMailbox(self):
        add = EditMailbox("Add Mailbox", AddAction(self.controller), "", "", "")
        add.exec()

    def editMailbox(self):
        pick = PickMailbox(self.controller.getMailboxList())
        if pick.exec():
            mailboxId, address, host, userName = self.controller.getMailbox(pick.picked)
            action = EditAction(self.controller, mailboxId)
            edit = EditMailbox("Edit Mailbox", action, address, host, userName)
            edit.exec()

    # def editMailbox(self):
    #     pass

    def deleteMailbox(self):
        pick = PickMailbox(self.controller.getMailboxList())
        if pick.exec():
            self.controller.deleteMailbox(pick.picked)


    def exit(self):
        self.close()

def display(controller):
    boxes = MailboxesView(controller)
    boxes.exec()

