from PySide2 import QtCore, QtWidgets

class RegisterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.title = QtWidgets.QLabel("Register")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.__message__()
        self.__values__()
        self.__buttons__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.messageBox)
        self.layout.addLayout(self.outerValuesBox)
        self.layout.addLayout(self.buttonBox)
        
        self.setLayout(self.layout)

    def __message__(self):
        self.tagLabel = QtWidgets.QLabel("Email tag")

        self.tag = QtWidgets.QLineEdit()

        self.messageButton = QtWidgets.QPushButton("Read email")

        self.messageBox = QtWidgets.QHBoxLayout()
        self.messageBox.addWidget(self.tagLabel)
        self.messageBox.addWidget(self.tag)
        self.messageBox.addWidget(self.messageButton)
        self.messageBox.insertStretch(0)
        self.messageBox.insertStretch(-1)



    def __values__(self):
        self.nameLabel = QtWidgets.QLabel("Website name")
        self.name = QtWidgets.QLineEdit()

        self.hostLabel = QtWidgets.QLabel("Endpoint")
        self.host = QtWidgets.QLabel("")

        self.userNameLabel = QtWidgets.QLabel("Website user name")
        self.userName = QtWidgets.QLabel("")

        self.valuesBox = QtWidgets.QGridLayout()
        self.valuesBox.addWidget(self.nameLabel, 0, 0)
        self.valuesBox.addWidget(self.name, 0, 1)
        self.valuesBox.addWidget(self.hostLabel, 1, 0)
        self.valuesBox.addWidget(self.host, 1, 1)
        self.valuesBox.addWidget(self.userNameLabel, 2, 0)
        self.valuesBox.addWidget(self.userName, 2, 1)

        self.outerValuesBox = QtWidgets.QHBoxLayout()
        self.outerValuesBox.addLayout(self.valuesBox)
        self.outerValuesBox.insertStretch(0)
        self.outerValuesBox.insertStretch(-1)

    def __buttons__(self):

        self.new = QtWidgets.QPushButton("Cancel")
        self.save = QtWidgets.QPushButton("Save")

        self.buttonBox = QtWidgets.QHBoxLayout()
        self.buttonBox.addWidget(self.new)
        self.buttonBox.addWidget(self.save)
        self.buttonBox.insertStretch(0)
        self.buttonBox.insertStretch(-1)
