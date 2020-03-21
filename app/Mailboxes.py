#
#       Mailboxes.py
#
#       Mailboxes mailboxes
#

import common

class Mailboxes(object):
    """Access class for mailboxes"""

    def __init__(self, connection):
        """Fill in local mailboxes from mailboxesbase"""

        self.connection = connection
        self.mailboxes = {}

        cursor = self.connection.cursor()

        for row in cursor.execute("SELECT name, host, user_name FROM mailboxes;"):
            name, host, userName = row
            self.mailboxes[name] = (host, userName)


    def getNames(self):
        """Get the list of names for the dropdown """

        return sorted(self.mailboxes)

    def getMailbox(self, name):
        """Get data for a mailbox"""

        host, userName = self.mailboxes[name]
        return (name, host, userName)


    def addMailbox(self, name, host, userName):
        """Add valid new mailbox to local mailboxes and database mailboxes"""

        messages = self.addBoxValidation(name, host, userName)
        if 0 == len(messages):
            self.mailboxes[name] = (host, userName)
            
            insert = "INSERT INTO mailboxes (name, host, user_name) VALUES (?, ?, ?);"
            cursor = self.connection.cursor()
            cursor.execute(insert, (name, host, userName))
            self.connection.commit()

            return ""
        else:
            return messages

    def updateMailbox(self, name, host, userName):
        """Update valid mailbox in local mailboxes and database mailboxes"""

        messages = self.updateBoxValidation(name, host, userName)
        if 0 == len(messages):
            self.mailboxes[name] = (host, userName)
            
            update = "UPDATE mailboxes SET host=?, user_name=? WHERE name=?;"
            cursor = self.connection.cursor()

            cursor.execute(update, (host, userName, name))
            self.connection.commit()
            
            return ""
        else:
            return messages

    def deleteMailbox(self, name):
        """Delete existing mailbox"""
        messages = common.notExists(name, self.mailboxes)
        if (0 == len(messages)):
            del self.mailboxes[name]

            cursor = self.connection.cursor()
            delete = "DELETE FROM mailboxes WHERE name=?;"

            cursor.execute(delete, (name,))
            self.connection.commit()

            return ""
        else:
            return messages

    def addBoxValidation(self, name, host, userName):
        """
        Confirm no mailbox data is empty
        Confirm unique name for new mailbox
        """
        messages = self.boxValidation(name, host, userName)
        messages += common.exists(name, self.mailboxes)

        return messages

    def updateBoxValidation(self, name, host, userName):
        """
        Confirm no mailbox data is empty
        Confirm name exists
        """
        messages = self.boxValidation(name, host, userName)
        messages += common.notExists(name, self.mailboxes)

        return messages

    def boxValidation(self, name, host, userName):
        """Confirm no mailbox data is empty"""
        messages = common.empty("Name", name)
        messages += common.empty("Host", host)
        messages += common.empty("User name", userName)

        return messages

