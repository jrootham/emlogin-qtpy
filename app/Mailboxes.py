#
#       Mailboxes.py
#
#       Mailboxes mailboxes
#

import common

class Mailboxes(object):
    """Access class for mailboxes"""

    def __init__(self, connection):
        """Fill in local mailboxes from mailbox table"""

        self.connection = connection
        self.mailboxes = {}

        cursor = self.connection.cursor()

        for data in cursor.execute("SELECT mailbox_id, address, host, user_name FROM mailboxes;"):
            mailboxId, address, host, userName = data
            self.mailboxes[address] = (mailboxId, host, userName)


    def exists(self, address):
        return address in self.mailboxes

    def getMailboxList(self):
        """Get the list of addreses for the dropdown """

        return sorted(self.mailboxes)

    def getMailbox(self, address):
        """Get data for a mailbox"""

        mailboxId, host, userName = self.mailboxes[address]
        return (mailboxId, address, host, userName)


    def addMailbox(self, address, host, userName):
        """Add valid new mailbox to local mailboxes and database mailboxes"""

        messages = self.addBoxValidation(address, host, userName)
        if 0 == len(messages):
            
            cursor = self.connection.cursor()

            insert = "INSERT INTO mailboxes (address, host, user_name) VALUES (?, ?, ?);"
            cursor.execute(insert, (address, host, userName))
            
            cursor.execute("SELECT mailbox_id FROM mailboxes WHERE address=?;", (address,))
            mailboxId, = cursor.fetchone()

            self.mailboxes[address] = (mailboxId, host, userName)

            self.connection.commit()

            return ""

        else:
            return messages

    def updateMailbox(self, mailboxId, address, host, userName):
        """Update valid mailbox in local mailboxes and database mailboxes"""

        messages = self.updateBoxValidation(mailboxId, address, host, userName)
        if 0 == len(messages):
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT address FROM mailboxes WHERE mailbox_id=?", (mailboxId,))
            oldAddress, = cursor.fetchone()

            update = "UPDATE mailboxes SET address=?, host=?, user_name=? WHERE mailbox_id=?;"
            cursor.execute(update, (address, host, userName, mailboxId))

            del self.mailboxes[oldAddress]
            self.mailboxes[address] = (mailboxId, host, userName)

            self.connection.commit()
            
            return ""
        else:
            return messages

    def deleteMailbox(self, address):
        """Delete existing mailbox"""
        messages = common.notExists(address, self.mailboxes)
        if (0 == len(messages)):
            mailboxId, host, userName = self.mailboxes[address]

            del self.mailboxes[address]

            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM mailboxes WHERE mailbox_id=?;", (mailboxId,))
            self.connection.commit()

            return ""
        else:
            return messages

    def addBoxValidation(self, address, host, userName):
        """
        Confirm no mailbox data is empty
        Confirm unique address for new mailbox
        """
        messages = self.boxValidation(address, host, userName)
        messages += common.exists(address, self.mailboxes)

        return messages

    def updateBoxValidation(self, mailboxId, address, host, userName):
        """
        Confirm no mailbox data is empty
        Confirm new name does not exist
        """

        messages = self.boxValidation(address, host, userName)

        if address in self.mailboxes:
            target = self.mailboxes[address]
            if target[0] != mailboxId:
                messages += common.exists(address, self.mailboxes)
                
        return messages

    def boxValidation(self, address, host, userName):
        """Confirm no mailbox data is empty"""
        messages = common.empty("Address", address)
        messages += common.empty("Host", host)
        messages += common.empty("User name", userName)

        return messages

