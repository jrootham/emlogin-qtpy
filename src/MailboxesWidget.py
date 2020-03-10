from PySide2 import QtCore, QtWidgets

class MailboxesWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


#        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Mailboxes")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
#        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

#        self.button.clicked.connect(self.magic)




