import time
import secrets
import requests
from imaplib import IMAP4_SSL
import mailparser
from html.parser import HTMLParser
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
            print(attributes)
            if ('name', 'np-target') in attributes:
                pairList = [pair for pair in attributes if 'content' in pair]
                self.link = pairList.pop()[1]


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

    def login(self, name):
        token = secrets.token_hex(16)
        if self.sites.exists(name):
            siteId, name, endpoint, identifier, address = self.sites.getSite(name)
            payload = {"identifier": identifier, "token": token}
            response = requests.get(endpoint, payload)
            if response.status_code == requests.codes.ok:
                return self.readEmail(token, address)
            else:
                return response.text

        else:
            return name + " does not exist"


    def readEmail(self, token, address):
        mailboxId, address, host, userName = self.getMailbox(address)

        if address in self.passwordDict:
            password = self.passwordDict[address]
        else:
            password = view.getPassword()
            if 0 != len(password):
                self.passwordDict[address] = password
            else:
                return ""  # User cancelled the prompt

        imap = IMAP4_SSL(host=host)        
        imap.login(userName, password)

        imap.select()

        subject = '"[#! nopassword {}]"'.format(token)

        num = b''
        count = 0
        delay = 1

        while 0 == len(num):
            error, result = imap.search(None, "SUBJECT " + subject)
            num = result[0]
            print('Try')
            time.sleep(delay)
            delay *= 2
            count += 1
            if 6 < count:
                break

        if 0 != len(num):
            if b' ' not in num:
                typ, data = imap.fetch(num, '(RFC822)')
                mail = mailparser.parse_from_bytes(data[0][1])
                htmlParser = ParseLink()
                htmlParser.feed(mail.body)

                url = htmlParser.link
                if 0 != len(url):
                    QDesktopServices.openUrl(url)

                    imap.store(num, '+FLAGS', '\\Deleted')
                    imap.expunge()                    
                    imap.close()
                    imap.logout()

                    return ""
                else:
                    imap.close()
                    imap.logout()
                    return "URL not found in mail"

            else:
                imap.close()
                imap.logout()
                return "More than one email"

        else:
            imap.close()
            imap.logout()
            return "Email not found"

