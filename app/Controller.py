import secrets
import requests

from Mailboxes import Mailboxes
from Sites import Sites

import database
import view

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
        self.passwords = {}



    def getMailboxList(self):
        return self.mailboxes.getMailboxList()

    def getMailbox(self, address):
        return self.mailboxes.getMailbox(address)

    def addMailbox(self, address, host, userName):
        return self.mailboxes.addMailbox(address, host, userName)

    def updateMailbox(self, mailboxId, address, host, userName):
        return self.mailboxes.updateMailbox(mailboxId, address, host, userName)

    def deleteMailbox(self, address):
        return self.mailboxes.deleteMailbox(address)



    def getSiteList(self):
        return self.sites.getSiteList()

    def getSite(self, name):
        return self.sites.getSite(name)

    def addSite(self, name, endpoint, identifier):
        print(name, endpoint, identifier)
        return self.sites.addSite(name, endpoint, identifier)

    def renameSite(self, oldName, newName):
        return self.sites.renameSite(oldName, newName)

    def deleteSite(self, name):
        return self.sites.deleteSite(name)



    def login(self, name):
        self.token = secrets.token_hex(16)
        if self.sites.exists(name):
            siteId, name, endpoint, identifier = self.sites.getSite(name)
            payload = {"identifier": identifier, "token": self.token}
            response = requests.get(endpoint, payload)
            if response.status_code == requests.codes.ok:
                self.readEmail()
            else:
                return response.text
                # Errors
        else:
            return name + " does not exist"
