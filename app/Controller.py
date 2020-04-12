import time
import secrets
import requests
import socket
import imaplib
import mailparser
from html.parser import HTMLParser
from PySide2 import QtCore
from PySide2.QtGui import QDesktopServices

from Mailboxes import Mailboxes
from Sites import Sites
import database
import view

class ParseLink(HTMLParser):
    """docstring for ParseLink"""
    def __init__(self):
        super(ParseLink, self).__init__()

        self.link = ""
        
    def handle_starttag(self, start, attributes):
        if "meta" == start:
            if ('name', 'np-target') in attributes:
                pairList = [pair for pair in attributes if 'content' in pair]
                self.link = pairList.pop()[1]


class Login(object):
    """docstring for Login"""
    def __init__(self, app, host, userName, password, token):
        super(Login, self).__init__()
        
        self.app = app
        self.host = host
        self.userName = userName
        self.password = password
        self.token = token

        self.errorList = ""

        self.subject = '"[#! nopassword {}]"'.format(token)


    def search(self):
        try:
            imap = imaplib.IMAP4_SSL(host=self.host)        
            imap.login(self.userName, self.password)

            imap.select()
            error, searchResult = imap.search(None, "SUBJECT " + self.subject)
            num = searchResult[0]

            if 0 != len(num):
                self.found = True
              
                if b' ' not in num:  
                    typ, data = imap.fetch(num, '(RFC822)')
                    mail = mailparser.parse_from_bytes(data[0][1])
                    htmlParser = ParseLink()
                    htmlParser.feed(mail.body)

                    url = htmlParser.link
                    if 0 != len(url):
                        QDesktopServices.openUrl(url)

                        imap.store(num, '+FLAGS', '\\Deleted')

                        self.errorList = ""

                    else:
                        self.errorList = "URL not found in mail"

                else:
                    self.errorList = "More than one email found, possible attack"

            else:
                self.errorList = "Email not found"

            imap.close()
            imap.logout()

        except socket.gaierror as error:
            code, self.errorList = error.args
            self.found = True

        except imaplib.IMAP4.error as error:
            reason, = error.args
            self.errorList = reason.decode()
            self.found = True
            
        self.done = True
 
    def login(self, display):
        count = 1
        delay = 1000
        self.found = False

        while not self.found:

            self.done = False
            display.display("Launching search try {}\nDelaying {} seconds".format(count, delay/1000))
            QtCore.QTimer.singleShot(delay, self.search)

            while not self.done:
                self.app.processEvents()

            delay *= 2
            count += 1
            if 8 <= count:
                break

        return self.errorList

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
        self.passwordDict = {}



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

    def addSite(self, name, endpoint, identifier, address):
        return self.sites.addSite(name, endpoint, identifier, address)

    def renameSite(self, oldName, newName):
        return self.sites.renameSite(oldName, newName)

    def deleteSite(self, name):
        return self.sites.deleteSite(name)

    def login(self, app, display, name):
        token = secrets.token_hex(16)
        if self.sites.exists(name):
            siteId, name, endpoint, identifier, address = self.sites.getSite(name)
            payload = {"identifier": identifier, "token": token}
            display.display("Making request")
            response = requests.get(endpoint, payload)
            if response.status_code == requests.codes.ok:
                display.display("Reading mail")
                return self.readEmail(app, display, token, address)
            else:
                return response.text

        else:
            return name + " does not exist"


    def readEmail(self, app, display, token, address):
        mailboxId, address, host, userName = self.getMailbox(address)

        if address in self.passwordDict:
            password = self.passwordDict[address]
        else:
            password = view.getPassword()
            if 0 != len(password):
                self.passwordDict[address] = password
            else:
                return ""  # User cancelled the prompt

        login = Login(app, host, userName, password, token)
        result = login.login(display)
        
        del login

        return result
