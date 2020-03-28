
from Mailboxes import Mailboxes
from Sites import Sites

import database

class Controller(object):
    """
    Controller contains the models and the database connection
    Models get the database connection passed to them
    Models are exposed to the Views
    """
    def __init__(self, filename):
        self.connection = database.makeConnection(filename)

        self.mailboxes = Mailboxes(self.connection)
        self.sites = Sites(self.connection)

        self.host = ""
        self.userName = ""

    def getMailboxes(self):
        return self.mailboxes


    def getSites(self):
        return self.sites

    def setCurrentMailbox(self, host, userName):
        self.host = host
        self.userName = userName

    def doConnect():
        pass
        